# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/).

Pre-2023/08-15 changelog is available in [CHANGELOG_old.md](CHANGELOG_old.md), it will be gradually 
migrated to this file.

## [Unreleased]
### Added
### Changed
### Fixed
### Removed

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