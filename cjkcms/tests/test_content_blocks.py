import pytest
from wagtail import blocks

from cjkcms.blocks.content_blocks import CardBlock


@pytest.mark.parametrize(
    "context",
    [
        None,
        {},
        {"id": "card-id"},
        {"self": None},
        {"self": object()},
        {"self": {}},
        {"self": {"default_card_template": ""}},
        {"self": {"default_card_template": None}},
    ],
)
def test_card_uses_default_template_without_grid_template(context):
    assert CardBlock().get_template(context=context) == "cjkcms/blocks/card_foot.html"


def test_card_uses_parent_grid_template():
    context = {"self": {"default_card_template": "cjkcms/blocks/card_head.html"}}

    assert CardBlock().get_template(context=context) == "cjkcms/blocks/card_head.html"


def test_card_stream_child_renders_without_context():
    stream_block = blocks.StreamBlock([("card", CardBlock())])
    stream = stream_block.to_python(
        [{"type": "card", "value": {"title": "Standalone card"}, "id": "card-id"}]
    )

    html = stream[0].render()

    assert '<h5 class="card-title">Standalone card</h5>' in html
    assert '<div class="card-footer">' in html
