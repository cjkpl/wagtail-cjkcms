# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/).

Pre-2023/08-15 changelog is available in [CHANGELOG_old.md](CHANGELOG_old.md), it will be gradually 
migrated to this file.

## [Unreleased]
### Added
- Personal snippet listing display options: optional column visibility and rows
  per page, stored per user/listing without modifying project user models.
  Enabled for CMS snippets, with reusable viewset/mixin support for project snippets.
  Changes save automatically and refresh the listing in place, without an Apply button.
  Deployment requires migrations and collectstatic.
- Built-in Draftail character and word counters, adapted from `wagtail-character-counter`.
  The standalone app takes precedence while it remains in `INSTALLED_APPS`, avoiding duplicate counters.
### Changed
- Theme CSS/JS and Font Awesome loaded from CDNs now carry Subresource Integrity hashes,
  listed by URL in the new `CJKCMS_ASSET_INTEGRITY` setting. Theme URLs overridden in
  `CJKCMS_THEME_FILES` are loaded as before, without a check. Projects overriding
  `frontend_assets.html` or `frontend_scripts.html` are not affected.
- The search page loads at most `CJKCMS_SEARCH_MAX_RESULTS` results per searchable model
  (default 1000), so a very broad query can no longer exhaust memory. Result counts still
  report every match. Set it to `None` to restore loading all matches. Models with fewer
  matches than the limit now also need one query instead of two.
- The image gallery block and the favicon links load their image renditions with one
  query each, instead of two per gallery image and four for the favicon. The
  `get_pictures` tag accepts a `renditions` argument listing the image filters a
  customised gallery template uses, and returns no pictures for a deleted collection
  instead of raising an error. Projects overriding the `favicon` block are not affected.
- `body_preview` is computed once per page instance and body. An article without a search
  description or caption used to render its whole body three more times per page view,
  once for each meta description tag, repeating all queries of its blocks.
- Navbar items set to show child pages check for a live child with an `EXISTS` query
  instead of loading every child page on each page view.
- Blocks hidden by their visibility settings are skipped before their template context
  is built, saving the queries of e.g. a hidden "Latest Pages" block.
- `CjkcmsPage.get_site()` now looks the site up once per page instance, and the new
  `CjkcmsPage.get_layout_settings()` does the same for the site's layout settings.
  Rendering a page no longer repeats these queries for each SEO property
  (an empty web page went from 41 to 22 queries).
### Fixed
- Isolated page template and child-page ordering choices per page/form instance,
  preventing intermittent validation errors when different page types are instantiated.
  Existing template settings and stored values are unchanged; no migration is needed.
- Removed the CSRF token from the navbar search forms. They submit over GET, so the token
  was never checked, but it leaked into search URLs and stopped the page cache from serving
  anonymous visitors. Warning! Sites with the navbar search box enabled will now really be
  served from the page cache: content rendered per request (e.g. blocks with "visible
  from/to" dates) stays as cached until the cache expires or a page/snippet is saved.
- Copying, aliasing or translating a page no longer resets "Show list of child pages",
  "Show list of related pages" and "Order child pages by" to the defaults of the page type.
  Values passed when constructing a page in code are kept as well. Pages copied before
  this fix are not corrected automatically.
- Mailchimp merge fields entered by editors are rendered with a bare template engine.
  They can still use form field variables and built-in filters, but can no longer load
  tag libraries (and through them read Django settings) or include other templates.
- `OEmbedFinderWithReferer` waits at most 10 seconds for a provider instead of
  indefinitely, and reports a video response without HTML as "embed not found"
  rather than failing with a server error.
- Ordering child pages by a classifier no longer fails on PostgreSQL ("more than one row
  returned by a subquery") when a child page has several terms of that classifier.
  Such a page is placed by the first of its terms.
- Carousel block markup: the indicator buttons were missing the end of their opening tag,
  slides got their custom ID prefixed with `#`, and the control labels had a stray quote.
- Several countdown blocks on one page no longer interfere with each other: every block
  started every countdown on the page. The element keeps `id="mycountdown"`, unless
  the block has a Custom ID, which is now used.
- The Google Analytics snippet no longer configures a second, empty property
  (`gtag('config', '')`), left over from the removed Universal Analytics ID.
- A page with an image gallery whose collection or tag has been deleted no longer fails
  with a server error. Without its collection the gallery is empty; without its tag it
  shows the whole collection. The editor is asked to choose again when the page is edited.
- `robots.txt` gives the sitemap as an absolute URL built from the Wagtail site
  (e.g. `https://www.example.com/sitemap.xml`), as crawlers require, instead of
  `/sitemap.xml`. Projects with their own `cjkcms/robots.txt` template are not affected.
- Page previews (`body_preview`, also used as the meta description of articles) no longer
  contain the JavaScript or CSS code of blocks such as the countdown or icon with text.
### Removed
- Dropped the `wagtail-color-panel` dependency; internal color fields now use native widgets.

## [25.1.3] - 2025-01-03
### Fixed
 - Fixed problems on some websites resulting from renaming navbar_search.html. Restored the previous template file name.

## [25.1.1] - 2025-01-01
### Fixed
 - Fixed regression bug causing menu items to be hidden. This required me to fully remove
 check for the deprecated menu items visibility options.

## [24.12.4] - 2024-12-31
### Removed
 - Removed deprecated menu visibility management via visible_for field in NavBlocks
CMS blocks are JSON-based, and ignored in migrations, so If we removed the field in block defintion, this would not cause the data in database disappear. As a result we might have blocks in various websites which are strangely invisible to users, even if nothing is set in the visible block definition. So for safety, a new setting has been added: CJKCMS_NAVBAR_SHOW_VISIBLE_FOR = False. Switch it to True to restore visibility of that block component, if you have problems with any websites. For security, implementation of the visibility checks in templates (can_show_item value.visible_for ) was NOT removed from code.
- Corrected issue with fixed top navbars. Important - this changed some implementation details (e.g. css styling), so check your site if it uses fixed navbar

## [24.12.2] - 2024-12-31
### Added
 - "countdown" content block using VincentLoy's library. See https://vincentloy.github.io/simplyCountdown.js/ for more info
 - added themes and tests for the "countdown" block


## [24.9.1] - 2024-09-02
### Added
 - Support for breadcrumbs per-page visibility
 - breadcrumb_title page property for all CMS pages, choosing new "breadcrumb_label" field or page title if new field empty
 - Added new templatetag with tests: first_not_empty which returns first not empty argument from the list, e.g. {% first_not_empty var1 var2 var3 %} 

## [24.8.1] - 2024-08-27
### Fixed
 - Update malformed robots.txt file

## [24.6.4] - 2024-06-28
### Changed
 - Update mdb-ui-kit version to 7.3.2

## [24.6.4] - 2024-06-26
### Fixed
 - Fixed responsiveness of the 404 template 

## [24.6.3] - 2024-06-25
### Added
 -  HighlightBlock, allows an element to stand out with the ability to change the colour of the background, border, text from the basic bootstrap colour palette also allows an icon to be added

## [24.6.2] - 2024-06-02
### Added
 - API endpoint to allow remote monitoring of software component versions. Disabled by default. See /docs/api/version_monitor.md for details

## [24.6.1] - 2024-06-01
### Changed
 - MDBootstrap kit updated to 7.3.0
 - Restored availability of MDBootstrap CDN ich choice of Bootstrap themes
 - Updated dropdown init code in base_link_block to work with MDBootstrap 7.3.0+
### Fixed
 - Dark theme was incorrectly forced when MDB was in use; now respects the choice in backend->settings->layout

## [24.5.1] - 2024-05-01
### Added
 - Support for custom bs/mdb variables: when layout->theme set to "custom", loads /static/cjkcms/css/cjkcms-custom-theme.css. Define this file in your project using e.g. template copied from /static/cjkcms/css/cjkcms-custom-theme-disabled.css and redefine any css vars
 - Support for stretched-link in any Button Link, including in any card. To achieve a stretched link, add "stretched-link" to custom css classes in button's advanced settings. To achieve an invisible button link (e.g. image link), add "stretched-link zero-sized" to custom css of the button.


## [24.3.3] - 2024-03-21
### Added
 - Correct processing of theme_css and theme_js for both full URLs (https:...) and local static paths (local/path/to.css)
 - Support for client-side theme switching in both bootstrap and mdbootstrap
### Fixed
 - Problem with stretched-link not working in mdbootstrap when btn class used (required updating mdb-uikit to 7.x)
### Changed
 - MDB light and dark now packaged with the CMS, not loaded from CDN
 - !!! Breaking change: navbar_color_scheme setting renamed to color_scheme and used as data-mdb/bs-theme setting for theme switching
 - !!! Breaking configuration changes in Layout settings: navbar_collapse_mode, navbar_format, navbar_langselector and frontend_theme:
   changed choices in the model from None to [], this may result in re-setting these settings in Backend->Settings->Layout to defaults.
   Check each website after updating the CMS for layout of the HP, navbar collapse screen width, and theme layout.

## [24.3.2] - 2024-03-20
### Fixed
 - Renamed "libs" to "cjkcms_libs" in frontend scripts, to avoid name clash with htmx
 Note: turns out, this was a misdiagnosed issue, there was no clash. But, it is better to have a more specific variable name,
 rather than a generic "libs", so we'll keep this change.


## [24.3.1] - 2024-03-11
### Added
 - Missing social media fields in settings/social-media, and icons, including new X to replace Twitter
 - Updated fontawesome CDN call to v.6.5.1 to include new X icon.


## [24.2.7] - 2024-02-18
### Fixed
 - Rebuilt search box/button customisation for cleaner code and more flexibility


## [24.2.6] - 2024-02-18
### Fixed
 - Removed packages from pyproject.toml to rely on autodiscovery of setuptools


## [24.2.4] - 2024-02-18
### Fixed
 - Broken setup dependencies in pyproject.toml

## [24.2.4] - 2024-02-18
### Added
 - Customisable search box, with five different out-of-the-box display styles.
 - Updated setup configuration. Restored dependency on wagtail-seo and wagtail-cache which now support Wagtail 6.

# [24.2.1] - 2024-02-08
### Fixed
 - Ensured compatibility with Wagtail 6.0 and Django 5.0.x

## [24.1.1] - 2024-01-07
### Fixed
 - Code refactoring
 = Ensured compatibility with Wagtail 5.2.x and Django 5.0.x
### Added
 - Added some unit tests



## [23.12.2] - 2023-12-07
### Fixed
 - Fixed Vimeo oembed provider which was broken due to Vimeo API changes (there should be no www. in the oembed url)


## [23.12.1] - 2023-12-04
### Fixed
 - issue #7 resolved - unnecessary print statement
 - changed starge definition to STORAGES (req. Django 4.2+)

## [23.10.6]
### Added
 - default_seo_image in Settings->Layout->Branding, to be used in meta tags and social media cards when no image is specified for a page
### Fixed
 - in project templates, ALL_LAYOUT_STREAMBLOCKS now get properly updated with ALL_CONTENT_STREMBLOCKS.


## [23.10.5]
### Fixed
 - codespell related fixes
 - fixed broken webpack project template
 - started building docs for webpack project template

## [23.10.4]
### Added
 - Responsive images classes for text editor image blocks (centered, left, right)
### Changed
### Fixed
 - Missing sitemap app in base.py in project templates
 - Corrected broken EMAIL_BACKEND in base.py in webpack project template
### Removed

## [23.10.3] - 2023-10-07
### Added
 - 25 Bootswatch themes to choose from in the settings
### Changed
 - Rewritten inclusion of frontend CSS and JS assets to support new themes


## [23.10.2] - 2023-10-07
### Fixed
 - Search bar layout - vertical alignment
 - Full search form - fixed broken template

 ### Added
 - Breadcrumbs template snippet - needs to be activated in Settings->Layout
 - New section in the docs
 

## [23.10.1] - 2023-10-01
### Added
 - Added EventCalendar content block. Use snippets to create EventCalendars, and to display them on pages.


## [23.9.2] - 2023-09-07
### Added
 - AdvancedSettings for Page blocks and Navigation models supports conditional visibility: all, none, not-logged-in, logged-in, logged-in and in group(s), logged-in and not in group(s). Tests needed. 


## [23.9.1] - 2023-09-04
### Added
 - New template snippet: actionbar.html. This will further be developed to include customisable calls to action in the page header.

## [23.8.11] - 2023-08-22
### Fixed
 - broken icons in the backend


## [23.8.10] - 2023-08-21
### Added
 - Images in Snippet Index Views: ThumbnailColumn("image", width=50, classname="w-rounded") in SnippetViews. Requires Wagtail >=5.1

## [23.8.9] - 2023-08-21
### Added
 - Added dynamic labels to all collapsed layout block types
### Removed
 - Removed unused modeladmin imports (deprecated)

## [23.8.8] - 2023-08-20
### Fixed
 - broken requirements in pyproject.toml

## [23.8.7] - 2023-08-20
### Added
 - Added individual navigation bar alignment options, to allow some menu items to be aligned to the left and some to the right, working smoothly with social media icons display in menu position.
### Changed
 - Documentation uses material mkdocs theme
### Fixed
 - Social media icons include_block tag replaced with include tag
 - Fixed display of page, document and image names in collapsed navbar entries
 - Fixed template variable in social media icons template block

## [23.8.6] - 2023-08-19

### Added
- new changelog in a proper format (new changes at the top)
- Added aria-label to menubar logo and social media icons

### Changed
- dependencies updated to use cjkpl's forked pypi packages for wagtail-color-panel and wagtail-seo, as original packages do not yet have a Wagtail 5.x support

<!-- >
## [Unreleased]
### Added
### Changed
### Fixed
### Removed
< -->
