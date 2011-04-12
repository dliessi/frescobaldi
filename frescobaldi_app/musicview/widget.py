# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2011 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
The PDF preview panel widget.
"""

from __future__ import unicode_literals

import itertools
import os
import weakref

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import popplerqt4
import qpopplerview

import app
import icons
import textformats

from . import pointandclick


class MusicView(QWidget):
    def __init__(self, dockwidget):
        """Creates the Music View for the dockwidget."""
        super(MusicView, self).__init__(dockwidget)
        
        self._positions = weakref.WeakKeyDictionary()
        self._currentDocument = lambda: None
        self._highlightFormat = QTextCharFormat()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.view = qpopplerview.View(self)
        layout.addWidget(self.view)
        app.settingsChanged.connect(self.readSettings)
        self.readSettings()
        self.view.setViewMode(qpopplerview.FitWidth)
        self.view.surface().pageLayout().setDPI(self.physicalDpiX(), self.physicalDpiY())
        self.view.viewModeChanged.connect(self.slotViewModeChanged)
        self.view.surface().linkClicked.connect(self.slotLinkClicked)
        self.view.surface().linkHovered.connect(self.slotLinkHovered)
        self.view.surface().linkLeft.connect(self.slotLinkLeft)
        self.view.surface().setShowUrlTips(False)
        self.view.surface().linkHelpRequested.connect(self.slotLinkHelpRequested)
        self.slotViewModeChanged(self.view.viewMode())
        
        zoomer = self.parent().actionCollection.music_zoom_combo
        self.view.viewModeChanged.connect(zoomer.updateZoomInfo)
        self.view.surface().pageLayout().scaleChanged.connect(zoomer.updateZoomInfo)

    def sizeHint(self):
        """Returns the initial size the PDF (Music) View prefers."""
        return self.parent().mainwindow().size() / 2
        
    def slotViewModeChanged(self, viewmode):
        """Called when the view mode of the view changes."""
        ac = self.parent().actionCollection
        ac.music_fit_width.setChecked(viewmode == qpopplerview.FitWidth)
        ac.music_fit_height.setChecked(viewmode == qpopplerview.FitHeight)
        ac.music_fit_both.setChecked(viewmode == qpopplerview.FitBoth)

    def openDocument(self, doc):
        """Opens a documents.Document instance."""
        cur = self._currentDocument()
        if cur:
            self._positions[cur] = self.view.position()
            
        self._currentDocument = weakref.ref(doc)
        self._links = pointandclick.links(doc.document())
        self.view.load(doc.document())
        position = self._positions.get(doc, (0, 0, 0))
        self.view.setPosition(position)

    def clear(self):
        """Empties the view."""
        cur = self._currentDocument()
        if cur:
            self._positions[cur] = self.view.position()
        self._currentDocument = lambda: None
        self.view.clear()
        
    def readSettings(self):
        """Reads the settings from the user's preferences."""
        color = textformats.formatData('editor').baseColors['selectionbackground']
        color.setAlpha(128)
        self._highlightFormat.setBackground(color)
        qpopplerview.cache.options().setPaperColor(textformats.formatData('editor').baseColors['paper'])
        self.view.redraw()

    def slotLinkClicked(self, ev, page, link):
        """Called when the use clicks a link.
        
        If the links is a textedit link, opens the document and puts the cursor there.
        Otherwise, call the QDesktopServices to open the destination.
        
        """
        cursor = self._links.cursor(link, True)
        if cursor:
            self.parent().mainwindow().setTextCursor(cursor, findOpenView=True)
            self.slotLinkLeft() # hide possible highlighting
        elif ev.button() != Qt.RightButton and isinstance(link, popplerqt4.Poppler.LinkBrowse):
            QDesktopServices.openUrl(QUrl(link.url()))

    def slotLinkHovered(self, page, link):
        """Called when the mouse hovers a link.
        
        If the links points to the current editor document, the token(s) it points
        at are highlighted using a transparent selection color.
        
        The highlight shows for a few seconds but disappears when the mouse moves
        off the link or when the link is clicked.
        
        """
        cursor = self._links.cursor(link)
        if not cursor or cursor.document() != self.parent().mainwindow().currentDocument():
            return
        
        # highlight token(s) at this cursor
        import tokeniter
        import ly.tokenize.lilypond
        document = cursor.document()
        block = cursor.block()
        column = cursor.position() - block.position()
        tokens = tokeniter.TokenIterator(block)
        source, state = tokens.forward_state()
        # go to our column
        for token in source:
            if token.pos >= column or tokens.block != block:
                break
        else:
            return
        
        start = token.pos + block.position()
        cur = QTextCursor(document)
        cur.setPosition(start)
        cursors = [cur]
        
        if isinstance(token, ly.tokenize.lilypond.Direction):
            # a _, - or ^ is found; find the next token
            for token in source:
                if not isinstance(token, (ly.tokenize.Space, ly.tokenize.Comment)):
                    break
        end = token.end + block.position()
        if token == '\\markup':
            # find the end of the markup expression
            depth = len(state)
            for token in source:
                if len(state) < depth:
                    end = token.end + tokens.block.position()
                    break
        elif token == '"':
            # find the end of the string
            for token in source:
                if isinstance(token, ly.tokenize.StringEnd):
                    end = token.end + tokens.block.position()
                    break
        elif isinstance(token, ly.tokenize.MatchStart):
            # find the end of slur, beam. ligature, phrasing slur, etc.
            name = token.matchname
            nest = 1
            for token in source:
                if isinstance(token, ly.tokenize.MatchEnd) and token.matchname == name:
                    nest -= 1
                    if nest == 0:
                        cur2 = QTextCursor(document)
                        cur2.setPosition(token.pos + tokens.block.position())
                        cur2.setPosition(token.end + tokens.block.position(), QTextCursor.KeepAnchor)
                        cursors.append(cur2)
                        break
                elif isinstance(token, ly.tokenize.MatchStart) and token.matchname == name:
                    nest += 1
                    
        cur.setPosition(end, QTextCursor.KeepAnchor)
        
        view = self.parent().mainwindow().currentView()
        view.highlight(self._highlightFormat, cursors, 2, 5000)
    
    def slotLinkLeft(self):
        """Called when the mouse moves off a previously highlighted link."""
        view = self.parent().mainwindow().currentView()
        view.clearHighlight(self._highlightFormat)

    def slotLinkHelpRequested(self, pos, page, link):
        """Called when a ToolTip wants to appear above the hovered link."""
        if isinstance(link, popplerqt4.Poppler.LinkBrowse):
            text = link.url()
            cursor = self._links.cursor(link)
            m = pointandclick.textedit_match(link.url())
            if m:
                filename, line, column = pointandclick.readurl(m)
                text = "{0}  {1}:{2}".format(os.path.basename(filename), line, column)
            QToolTip.showText(pos, text, self.view.surface(), page.linkRect(link.linkArea()))

