# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008, 2009, 2010 by Wilbert Berendsen
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

from __future__ import unicode_literals

"""
Manages marked lines (bookmarks) for a Document.

A mark is simply a QTextCursor that maintains its position in the document.

"""

import bisect
import weakref

from PyQt4.QtGui import QTextCursor

import signals

types = (
    'bookmark',
    'error',
)


class Bookmarks(object):
    
    marksChanged = signals.Signal()
    
    def __init__(self, document):
        self.document = weakref.proxy(document)
        self._marks = dict((type, []) for type in types)
        
    def marks(self, type=None):
        return self._marks[type] if type else self._marks
    
    def setMark(self, linenum, type):
        nums = [mark.blockNumber() for mark in self._marks[type]]
        if linenum in nums:
            return
        index = bisect.bisect_left(nums, linenum)
        mark = QTextCursor(self.document.findBlockByNumber(linenum))
        try:
            # only available in very recent PyQt4 versions
            mark.setKeepPositionOnInsert(True)
        except AttributeError:
            pass
        self._marks[type].insert(index, mark)
        self.marksChanged()
        
    def unsetMark(self, linenum, type):
        nums = [mark.blockNumber() for mark in self._marks[type]]
        if linenum in nums:
            # remove double occurrences
            while True:
                index = bisect.bisect_left(nums, linenum)
                del self._marks[type][index]
                del nums[index]
                if linenum not in nums:
                    break
            self.marksChanged()
        
    def toggleMark(self, linenum, type):
        nums = [mark.blockNumber() for mark in self._marks[type]]
        index = bisect.bisect_left(nums, linenum)
        if linenum in nums:
            # remove double occurrences
            while True:
                del self._marks[type][index]
                del nums[index]
                if linenum not in nums:
                    break
                index = bisect.bisect_left(nums, linenum)
        else:
            mark = QTextCursor(self.document.findBlockByNumber(linenum))
            try:
                # only available in very recent PyQt4 versions
                mark.setKeepPositionOnInsert(True)
            except AttributeError:
                pass
            self._marks[type].insert(index, mark)
        self.marksChanged()

    def clear(self, type=None):
        if type is None:
            for type in types:
                self._marks[type] = []
        else:
            self._marks[type] = []
        self.marksChanged()


