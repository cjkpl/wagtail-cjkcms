# Testing

## Introduction

Unit Tests for cjkcms are stored in two locations:

1. `tests` folder in the cjkcms folder. This folder contains all tests that do not require a testproject with additional page types, not defined in the cjkcms package.
2. `tests` folder in the testproject folder. This folder contains all tests (currently one - for PublicEvent block) that require  additional page types, not defined in the cjkcms package. These page types (with new blocks) are defined in `testproject/testapp/models.py`.

## Running tests

You can run the tests from multiple locations in the folder structure. The following assumes a more complex folder structure, where the wagtail project is located in a separate folder, e.g. 'devsite', and the repository with the cjkcms app is located at the same level, and installed with `pip -e .` 

Example folder structure:
```
env-cms # virtual environment
devsite # wagtail project
wagtail-cjkcms # cjkcms repository downloaded using git-clone
```

### running pytest from devsite folder:
```
pytest ../wagtail-cjkcms/cjkcms --ds=devsite.settings.dev
```
Note: replace the settings folder with your wagtail project name.

### running pytest from wagtail-cjkcms/testproject folder, excluding project_template folder:
```
pytest ../cjkcms tests --ds=testproject.settings.dev --ignore=../cjkcms/project_template
```


### running pytest from wagtail-cjkcms/testproject folder, excluding project_template folder, with extra options:
```
pytest ../cjkcms tests --ds=testproject.settings.dev --doctest-modules --durations=0 --ignore=../cjkcms/project_template
```
Explanation:

Start in wagtail-cjkcms/testproject folder.
Use pytest to run all tests from ../cjkcms folder, and any tests from tests folder in the current (testproject) folder.
`--ds=` uses testproject.settings.dev as the settings file. Uses `--ignore` to ignore the project_template folder, as it is not a part of the cjkcms package and contains a template code that would cause parse errors. `--doctest-modules` runs also doctests. `--durations=0` shows the time it took to run each test.

## Testing "external" blocks 
which are not added to any page type defined in the application, but are intended to be used by other apps in your projects.

An example block of this kind is described below.

### PublicEvent block
Defined in `cjkcms/blocks/content/events.py`.
T0 test this block, you need to use a testproject with a page type that uses the block. The cjkcms package includes a testproject, which has an application called `testapp`, with three new page types: `ProjectArticle`, `ProjectArticleIndexPage` and `ProjectPage`. The `ProjectArticle` page type uses the PublicEvent block as a content block, and two other page types redefine their layout blocks, also including the PublicEvent content block.

In the `testproject/tests` folder there is a sample test for the PublicEvent block. To execute just the tests in this folder, start in `testproject` and run:
```
pytest tests --ds=testproject.settings.dev
```