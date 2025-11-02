"""
QuranKit Components Package
"""

from .search import QuranSearchComponent
from .tree import QuranTreeComponent
from .morphology import QuranMorphologyComponent
from .display import QuranDisplayComponent
from .audio import QuranAudioComponent
from .bookmarks import QuranBookmarksComponent
from .theme import QuranThemeComponent

__all__ = [
    'QuranSearchComponent',
    'QuranTreeComponent',
    'QuranMorphologyComponent',
    'QuranDisplayComponent',
    'QuranAudioComponent',
    'QuranBookmarksComponent',
    'QuranThemeComponent'
]
