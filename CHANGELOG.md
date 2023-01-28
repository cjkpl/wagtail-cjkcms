# 0.1.1 (2022-08-14)
* Updated the README.md

# 0.1.2 (2022-08-14)
* Updated the README.md

# 0.1.3 (2022-08-15)
* added config for mkdocs
* moved docs folder one level up
* started basic documentation and updated readme
* updated pyproject.toml and added requirements to setup.cfg

# 0.1.4 (2022-08-15)
* fixed broken docs links in readme

# 0.1.5 (2022-08-15)
* fixed missing folders in the install package (modified manifest file)

# 0.1.6 (2022-08-25)
* Added import of `BaseBlock` to cjkcms.blocks for compatibility with other apps using the block
* Fixed missing InlinePanel allowing choosing default site navbar in Settings -> Layout
* Removed models/cms_models_legacy.py as it was crashing doctests due to duplicate model names
* extracted get_panels() method from Cjkcmspage get_edit_handler() to simplify overriding admin panels in subclasses. (as per suggestion of @FilipWozniak)

# 0.1.7 (2022-08-27)
* Added missing InlinePanel allowing choosing footers for the website in Settings -> Layout

# 0.1.8 (2022-08-27)
* Fixed missing search template in CjkcmsMeta (for backward compatibility)
* Fixed broken Advanced Settings in admin panel (hooks adding js/css were missing)

# 0.1.9.x (2022-09-01)
* Fixed broken get_panels() call preventing display of body panels in backend editor
* Removed useless debug/print entries in page_models

# 0.2.0 (2022-09-03)
* NON-COMPATIBLE with Wagtail<4.0! 
* Added missing attribute `use_json_field=True` in StreamField in several models - new migration.
* Removed unused block ada_skip in base page template.

# 0.2.1 (2022-09-03)
* Changed dependencies wagtail-seo i wagtail-cache to forked versions, which allow Wagtail 4.0.

# 0.2.2 (2022-09-03)
* Added cms_models to models/_init__.py, as they are already part of migration 0001, so they are not optional. Updated docs to reflect this.

# 0.2.3 (2022-09-06)
* Added label_format attribute for all content and layout blocks, to ensure correct display in collapsed admin view
* Added new test for article index / article page

# 0.2.4 (2022-09-07)
* Added new test to verify fixing a bug with ArticleIndexPage (details below)
* Fixed bug in ArticleIndexPage which prevented creation of an ArticleIndexPage under WebPage
* Fixed a broken test in test_articlepages introduced in 0.2.3.

# 0.2.5 (2022-09-07)
* Added a management command: init-website (replaces default HP with a custom, cms based one)
* Added a management command: init-navbar (adds a new Navbar and sets it as default for the website)

# 0.2.6 (2022-09-14)
* Added flags show_covers, show_dates and show_authors to the LatestPages block and its' templates

# 0.2.7 (2022-10-09)
* Fixed image formatting options in the RichtextBlock, to work with Bootstrap5. 
* Registered new image formats: left-thumb and right-thumb
* Introduced CI with CircleCI: flake8, codespell and unit tests

# 0.2.8 (2022-11-05)
* Added default_card_template to CardGrid to allow overriding default card template in a whole CardGrid
* Restored pypi requirements for wagtail-seo and wagtail-cache

# 0.2.8.1 (2022-11-06)
* Restored an aliast to SearchableHTMLBlock in cjkcms.blocks.searchable_html_blocks for backward compatibility

# 0.2.8.2 (2022-11-10)
* Fixed broken card template file name in settings.py

# 22.11.1 (2022-11-12)
* Renamed package to wagtail-cjkcms
* Changed versioning to calendar versioning (YY.MM.X)

# 22.11.2 (2022-11-27)
* Added two new quote styles and fixed formatting for the default quote template
* Added LayoutSettings to control default visibility of article author and publication date
* Removed unneeded stuff from testproject
* Updated setup configuration and gitignore. Added tox.ini config.
* Fixed broken reference to default image in card_landing* templates. Fixed accordion to work with B5 and MDB5.

# 22.11.3 (2022-11-30)
* Added new templatetag library (auth_extras) with a filter has_group to check if a user is in a group

# 22.11.4 (2022-11-30)
* Added custom handler for external links in RichText - any external link ending with ?_blank will open in a new tab
* Added missing static file (quote.svg)

# 22.11.5 (2022-11-30)
* Added responsive embeds CSS to work with WAGTAILEMBEDS_RESPONSIVE_HTML = True setting. 
* Fixed quote_block_leftbar malformed tag.
* Fixed broken .gitignore which was blockig any images subfolder, while it should only ignore /images/ folder in the root of the repository.

# 23.1.1 (2023-01-28)
* Updated MDB and Bootstrap (CDN) libs to most recent. 
* Updated FontAwesome (CDN) to v6. 
* Added custom font in layout settings with default Roboto.
* Updated card_landing2.html style to something usable. It requires two images, and uses page cover_image as one of backgrounds
  