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

## [Unreleased]
### Added
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