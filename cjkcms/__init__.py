VERSION = (2022, 8, 7, "dev", 0)

__version_info__ = VERSION
__version__ = ".".join(map(str, VERSION[:3])) + (
    "-{}{}".format(VERSION[3], VERSION[4] or "") if VERSION[3] != "final" else ""
)
__author__ = "Grzegorz Król"
__license__ = "BSD-3-Clause"
__copyright__ = "Copyright 2021-2022 Grzegorz Król and contributors"
