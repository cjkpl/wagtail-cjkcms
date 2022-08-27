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