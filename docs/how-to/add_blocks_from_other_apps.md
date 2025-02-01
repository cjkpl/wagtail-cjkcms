# Using blocks from other apps

Page models inheriting from cjkcms (CjkcmsWebPage, CjkcmsArticlePage or CjkcmsIndexPage) in a given project may require inclusion of blocks from several apps into the list of blocks available in the "Body" section of the page model, or for use in custom fields.

The order in INSTALLED_APPS doesn't effect when the models are created. Django figures out that certain models depend on others and runs them in the correct order. 

## Layout blocks and content blocks
CJKCMS defines two sets of blocks:
* layout blocks, e.g. grid of columns (rowcols), grid of cards, or custom html blocks.
* content blocks, typically allowed inside layout blocks, or in pages with simple layout structure, like "ArticlePage".

Some standard cms blocks are used in more than one place:
* HTML blocks are part of both layout and content blocks
* card blocks are used as content blocks, and as element of card grid layout block.

When creating your own blocks, decide whether it should be allowed at the layout level, at the content level. You can use any content block inside a layout, by putting it inside "RowCol"->"Column". 

## Project-specific page models

If we want to ensure that blocks from apps A, B, C are available for standard page models in a given project, the typical solution is to override CMS models in your "home" app, including into the new models blocks collected from other apps (A, B, C).

Check out the home app in the project templates (basic or webpack) in the cjkcms repository for full code example.
Modify the home app, importing blocks from your own apps.

```python
# home/blocks/__init__.py

from appa.blocks import APPA_CONTENT_BLOCKS, APPA_LAYOUT_BLOCKS  # noqa
from appb.blocks import APPB_CONTENT_BLOCKS, APPB_LAYOUT_BLOCKS  # noqa
from appc.blocks import APPC_CONTENT_BLOCKS, APPC_LAYOUT_BLOCKS  # noqa
from .blocks import HOME_CONTENT_STREAMBLOCKS, HOME_LAYOUT_STREAMBLOCKS  # noqa

# add your own content block
PROJECT_CONTENT_STREAMBLOCKS = HOME_CONTENT_STREAMBLOCKS + APPA_CONTENT_BLOCKS +  APPB_CONTENT_BLOCKS + APPC_CONTENT_BLOCKS

# add your own layout blocks
PROJECT_LAYOUT_STREAMBLOCKS = HOME_LAYOUT_STREAMBLOCKS + APPA_LAYOUT_BLOCKS + APPB_LAYOUT_BLOCKS + APPC_LAYOUT_BLOCKS
```

Once you have extra blocks added to your project configuration, 
they will be picked up by the three standard page models defined in
`home/models/cms_models.py`, as follows:

```python
from home.blocks import (
    PROJECT_CONTENT_STREAMBLOCKS,
    PROJECT_LAYOUT_STREAMBLOCKS,
)

ALL_CONTENT_STREAMBLOCKS = CONTENT_STREAMBLOCKS + PROJECT_CONTENT_STREAMBLOCKS
ALL_LAYOUT_STREAMBLOCKS = LAYOUT_STREAMBLOCKS + PROJECT_LAYOUT_STREAMBLOCKS

[...]

    # Override to CjkcmsStreamField to get rid of migration issues
    # when modifying LAYOUT_STREAMBLOCKS.
    body = CjkcmsStreamField(
        ALL_LAYOUT_STREAMBLOCKS, null=True, blank=True, use_json_field=True
    )
```

You may also define new fields in your models, using ALL_LAYOUT_STREAMBLOCKS or ALL_CONTENT_STREAMBLOCKS.

## Using blocks from APPA in APPB

The setup is similar if you want to use blocks from application A in application B. You need to add block definitions from APPA in your APPB, and use the new set of blocks in your APPB page models, or override the definition of the "body" field in your APPB page model. 

The only caveat is that you need to avoid circular import problem, so you cannot use `PROJECT\_\*\_STREAMBLOCKS` in `APPB\_\*\_STREAMBLOCKS`, and at the same time add `APPB\_\*\_STREAMBLOCKS` into your `PROJECT\_\*\_STREAMBLOCKS`