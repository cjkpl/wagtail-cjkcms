## Add Cjkcms embed finder
You can use Cjkcms embed finder which make sure that [**Referer**](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer "**Referer**") is defined in request header and iframe [**referrerpolicy**](https://www.geeksforgeeks.org/html-iframe-referrerpolicy-attribute/ "**referrerpolicy**") attribute is set to origin. This make sure that everything will work for example if you want to embed vimeo video on specific websites.

- Make sure that BASE_URL in your settings is set properly
```
BASE_URL = 'http://your.website.com'
```

- To change default embed finder go to your settings and add:
```
WAGTAILEMBEDS_FINDERS = [
    {
        'class': 'apps.cjkcms.finders.oembed.OEmbedFinderWithReferer',
    }
]
```
- If you want to change finder for specific provider (for example vimeo)
```
from wagtail.embeds.oembed_providers import vimeo
WAGTAILEMBEDS_FINDERS = [
	# Use Cjkcms embed finder for vimeo
    {
        'class': 'cjkcms.finders.oembed.OEmbedFinderWithReferer',
        'providers': [vimeo],
    },
    # Handles all other oEmbed providers the default way
    {
        'class': 'wagtail.embeds.finders.oembed',
    }
]
```
For more information about wagtail embeds check [**this site**](https://docs.wagtail.org/en/stable/advanced_topics/embeds.html "**this**").

- If you create embeds before, run following command to remove instances of Embed model (otherwise the old embeds will not work)
```
python manage.py clear-embeds
```
