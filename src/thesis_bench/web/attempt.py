from __future__ import annotations

from .fetch import _FetchOperationsMixin
from .search import _SearchOperationsMixin
from .state import _W1AttemptState


class W1Attempt(_SearchOperationsMixin, _FetchOperationsMixin, _W1AttemptState):
    pass
