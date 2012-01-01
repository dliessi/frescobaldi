#! python

# Python midifile package -- parse, load and play MIDI files.
# Copyright (c) 2011 - 2012 by Wilbert Berendsen
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
The midifile package allows you to load MIDI files and play them.

The goal is to have simple and very fast access to MIDI files using a pure
Python api. This package consists of several modules that can interact but also
be used separate from each other:

- parser:       load midi files or streams
- event:        very simple named tuples representing events
- song:         structure loaded data into a Song, with timing and tempo map
- player:       can play a Song with settable tempo and output
- output:       abstract class representing a MIDI output port

This package works with Python 2.6 and 2.7, but can easily be adapted for
Python 3.

"""
