# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/).

Pre-2023/08-15 changelog is available in [CHANGELOG_old.md](CHANGELOG_old.md), it will be gradually 
migrated to this file.

## [Unreleased]
### Added
 - Added dynamic labels to all collapsed layout block types
### Changed
### Fixed
### Removed
 - Removed unused modeladmin imports (deprecated)


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