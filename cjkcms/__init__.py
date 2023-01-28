VERSION = (23, 1, 1, "")

__version_info__ = VERSION
__version__ = ".".join(map(str, VERSION[:3])) + (f"-{VERSION[3]}" if VERSION[3] else "")

__author__ = "Grzegorz Król"
__license__ = "BSD-3-Clause"
__copyright__ = "Copyright 2021-2023 Grzegorz Król and contributors"
