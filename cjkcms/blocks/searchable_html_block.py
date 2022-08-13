from wagtail.core.blocks import RawHTMLBlock
from wagtail.core.rich_text import get_text_for_indexing
from django.utils.encoding import force_str

### CMS1 legacy - full file to be removed by 12/2022 ###


class SearchableHTMLBlock(RawHTMLBlock):
    """RawHTMLBlock extended with basic search support"""

    def get_searchable_content(self, value):
        # Strip HTML tags to prevent search backend from indexing them
        source = force_str(value)
        return [get_text_for_indexing(value)]
