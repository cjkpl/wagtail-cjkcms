# CjkCMS management commands

## Oembed custom finder
If you created embeds before adding the custom finder, or if vimeo does not display protected videos, run following command to remove instances of Embed model (otherwise the old embeds will not work)
```
./manage.py clear-embeds
```

## Optional initialization of collections
If you tend to re-initialize the same set of collections on your websites, you can simplify the task by running the follwing command:
```
./manage.py init-collections.py
```
It will add the following collections:

["Covers", "Logos", "Resources", "People", "Articles", "Cards", "Icons"]

