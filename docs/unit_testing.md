# Testing

## Character counter browser tests

From the repository root, run `python -m http.server 8765` and open
`http://localhost:8765/cjkcms/tests/js/character-counter.html` in a browser.
The page reports passing checks and any error. It tests initial counts, edits,
empty content, dynamically inserted editors, delayed editor initialization, and
block reinsertion using real DOM mutation observers. No JavaScript dependencies
are needed.

## Introduction

Unit Tests for cjkcms are stored in `cjkcms/tests` folder.

## Running tests

You can run the tests from multiple locations in the folder structure. The following assumes a more complex folder structure, where the wagtail project is located in a separate folder, e.g. 'devsite', and the repository with the cjkcms app is located at the same level, and installed with `pip -e .` 

Example folder structure:
```
env-cms # virtual environment
devsite # wagtail project
wagtail-cjkcms # cjkcms repository downloaded using git-clone
```

### running `pytest` from `devsite` folder:
```
pytest ../wagtail-cjkcms/cjkcms/tests
```
### running `pytest` from `wagtail-cjkcms` (repository root folder):
```
pytest cjkcms
```
### using `load_tests` function in repository root folder:
```
python load_tests.py
```

See [this page](https://github.com/cjkpl/cjkcms-testproject) for additional information on how test projects are set up. CjkCMS uses setups #1 and #3.
