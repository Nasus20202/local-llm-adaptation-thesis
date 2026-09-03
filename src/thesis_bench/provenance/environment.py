from __future__ import annotations

import platform

from .. import __version__
from .models import RuntimeEnvironment


def capture_environment() -> RuntimeEnvironment:
    return RuntimeEnvironment(
        platform=platform.platform(),
        machine=platform.machine(),
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
        package_version=__version__,
    )
