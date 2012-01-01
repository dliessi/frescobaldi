# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2012 by Wilbert Berendsen
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
Prints a PDF (or Poppler) document.

On Mac OS X and Linux, the document is just sent to lpr
(via a dialog).

On Windows, another command can be configured or bitmaps of the poppler document
can be printed.
"""

from __future__ import unicode_literals


import os
import subprocess

from PyQt4.QtCore import pyqtSignal, QTemporaryFile, Qt, QThread
from PyQt4.QtGui import QMessageBox, QPrinter, QPrintDialog, QProgressDialog

import app
import fileprinter
import qpopplerview.printer


def print_(doc, filename=None, widget=None):
    """Prints the popplerqt4.Poppler.Document.
    
    The filename is used in the dialog and print job name.
    If the filename is not given, it defaults to a translation of "PDF Document".
    The widget is a widget to use as parent for the print dialog etc.
    
    """
    cmd = fileprinter.lprCommand()
    if not cmd and QMessageBox.information(widget, _("Warning"), _(
        "No print command to print a PostScript file could be found.\n\n"
        "Therefore the document will be printed using raster images at {resolution} DPI. "
        "It is recommended to print using a dedicated PDF viewer.\n\n"
        "Do you want to continue?").format(resolution=300),
        QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
        return # cancelled
        
    filename = os.path.basename(filename) if filename else _("PDF Document")
    
    printer = QPrinter()
    printer.setDocName(filename)
    
    dlg = QPrintDialog(printer, widget)
    dlg.setMinMax(1, doc.numPages())
    dlg.setOption(QPrintDialog.PrintToFile, False)
    dlg.setWindowTitle(app.caption(_("Print {filename}").format(filename=filename)))
    
    result = dlg.exec_()
    if widget:
        dlg.deleteLater() # because it has a parent
    if not result:
        return # cancelled
    
    if cmd:
        # make a PostScript file with the desired paper size
        ps = QTemporaryFile()
        if ps.open() and qpopplerview.printer.psfile(doc, printer, ps):
            ps.close()
            # let all converted pages print
            printer.setPrintRange(QPrinter.AllPages)
            command = fileprinter.printCommand(cmd, printer, ps.fileName())
            if not subprocess.call(command):
                return # success!
        QMessageBox.warning(widget, _("Printing Error"),
            _("Could not send the document to the printer."))
    else:
        # Fall back printing of rendered raster images.
        # It is unsure if the Poppler ArthurBackend ever will be ready for
        # good rendering directly to a painter, so we'll fall back to using
        # 300DPI raster images.
        
        p = Printer()
        p.setDocument(doc)
        p.setPrinter(printer)
        p.setResolution(300)
        
        d = QProgressDialog()
        d.setModal(True)
        d.setMinimumDuration(0)
        d.setRange(0, len(p.pageList()) + 1)
        d.canceled.connect(p.abort)
        
        def progress(num, total, page):
            d.setValue(num)
            d.setLabelText(_("Printing page {page} ({num} of {total})...").format(
                page=page, num=num, total=total))
                
        def finished():
            p.deleteLater()
            d.deleteLater()
            d.hide()
            if not p.success and not p.aborted():
                QMessageBox.warning(widget, _("Printing Error"),
                    _("Could not send the document to the printer."))
            
        p.finished.connect(finished)
        p.printing.connect(progress)
        p.start()


class Printer(QThread, qpopplerview.printer.Printer):
    """Simple wrapper that prints the raster images in a background thread."""
    printing = pyqtSignal(int, int, int)
    
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        qpopplerview.printer.Printer.__init__(self)
        self.success = None
        
    def run(self):
        self.success = self.print_()
        
    def progress(self, num, total, page):
        self.printing.emit(num, total, page)


def printDocument(document, widget=None):
    """Prints the document described by the popplertools.Document.
    
    The widget is a widget to use as parent for the print dialog etc.
    
    """
    print_(document.document(), document.filename(), widget)


