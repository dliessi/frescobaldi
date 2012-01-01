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
Wood wind part types.
"""

from __future__ import unicode_literals

import __builtin__

from . import _base
from . import register


class WoodWindPart(_base.SingleVoicePart):
    """Base class for wood wind part types."""
    
    
class Flute(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Flute")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Flute", "Fl.")

    midiInstrument = 'flute'

    
class Piccolo(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Piccolo")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Piccolo", "Pic.")

    midiInstrument = 'piccolo'
    transposition = (1, 0, 0)


class BassFlute(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Bass flute")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Bass flute", "Bfl.")

    midiInstrument = 'flute'
    transposition = (-1, 4, 0)


class Oboe(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Oboe")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Oboe", "Ob.")

    midiInstrument = 'oboe'


class OboeDAmore(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Oboe d'amore")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Oboe d'amore", "Ob.d'am.")

    midiInstrument = 'oboe'
    transposition = (-1, 5, 0)


class EnglishHorn(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("English horn")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for English horn", "Eng.h.")

    midiInstrument = 'english horn'
    transposition = (-1, 3, 0)


class Bassoon(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Bassoon")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Bassoon", "Bn.")

    midiInstrument = 'bassoon'
    clef = 'bass'
    octave = -1


class ContraBassoon(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Contrabassoon")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Contrabassoon", "C.Bn.")

    midiInstrument = 'bassoon'
    transposition = (-1, 0, 0)
    clef = 'bass'
    octave = -1


class Clarinet(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Clarinet")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Clarinet", "Cl.")

    midiInstrument = 'clarinet'
    transposition = (-1, 6, -1)


class SopraninoSax(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Sopranino Sax")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Sopranino Sax", "SiSx.")
    
    midiInstrument = 'soprano sax'
    transposition = (0, 2, -1)    # es'


class SopranoSax(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Soprano Sax")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Soprano Sax", "SoSx.")
    
    midiInstrument = 'soprano sax'
    transposition = (-1, 6, -1)   # bes


class AltoSax(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Alto Sax")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Alto Sax", "ASx.")
    
    midiInstrument = 'alto sax'
    transposition = (-1, 2, -1)   # es


class TenorSax(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Tenor Sax")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Tenor Sax", "TSx.")
    
    midiInstrument = 'tenor sax'
    transposition = (-2, 6, -1)   # bes,


class BaritoneSax(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Baritone Sax")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Baritone Sax", "BSx.")
    
    midiInstrument = 'baritone sax'
    transposition = (-2, 2, -1)   # es,


class BassSax(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Bass Sax")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Bass Sax", "BsSx.")
    
    midiInstrument = 'baritone sax'
    transposition = (-3, 6, -1)   # bes,,


class SopranoRecorder(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Soprano recorder")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Soprano recorder", "S.rec.")
    
    midiInstrument = 'recorder'
    transposition = (1, 0, 0)


class AltoRecorder(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Alto recorder")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Alto recorder", "A.rec.")
    
    midiInstrument = 'recorder'


class TenorRecorder(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Tenor recorder")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Tenor recorder", "T.rec.")
    
    midiInstrument = 'recorder'


class BassRecorder(WoodWindPart):
    @staticmethod
    def title(_=__builtin__._):
        return _("Bass recorder")
    
    @staticmethod
    def short(_=__builtin__._):
        return _("abbreviation for Bass recorder", "B.rec.")
    
    midiInstrument = 'recorder'
    clef = 'bass'
    octave = -1



register(
    lambda: _("Woodwinds"),
    [
        Flute,
        Piccolo,
        BassFlute,
        Oboe,
        OboeDAmore,
        EnglishHorn,
        Bassoon,
        ContraBassoon,
        Clarinet,
        SopraninoSax,
        SopranoSax,
        AltoSax,
        TenorSax,
        BaritoneSax,
        BassSax,
        SopranoRecorder,
        AltoRecorder,
        TenorRecorder,
        BassRecorder,
    ])
