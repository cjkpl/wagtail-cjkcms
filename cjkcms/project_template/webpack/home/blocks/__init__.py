from .blocks import EventPresentationBlock  # noqa
from .blocks import HOME_CONTENT_STREAMBLOCKS, HOME_LAYOUT_STREAMBLOCKS  # noqa
#from otherapp.blocks import OTHERAPP_CONTENT_STREAMBLOCKS, OTHERAPP_LAYOUT_STREAMBLOCKS  # noqa


# add your own content block
PROJECT_CONTENT_STREAMBLOCKS = HOME_CONTENT_STREAMBLOCKS + [
    ("event_presentation", EventPresentationBlock()),
]

# add your own layout blocks
PROJECT_LAYOUT_STREAMBLOCKS = HOME_LAYOUT_STREAMBLOCKS + [
    # ("custom_block", CustomBlock()),
]
