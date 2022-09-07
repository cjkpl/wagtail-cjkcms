![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-cjkcms)
[![GitHub license](https://img.shields.io/github/license/cjkpl/django-cjkcms)](https://github.com/cjkpl/django-cjkcms/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/cjkpl/django-cjkcms)](https://github.com/cjkpl/django-cjkcms/issues) 

CMS system for Wagtail 3.x (4.x starting with v.0.2.0) forked from and based on [Wagtail CRX](https://github.com/coderedcorp/coderedcms) - an excellent CMS by [CodeRed](https://www.coderedcorp.com/).

## Note for versions 0.2.x

Until Codered's packages wagtail-seo and wagtail-cache are updated for compatibility with Wagtail 4, the cjkcms switches to forked versions of these packages. You will need to install them manually with:
```
pip install git+https://github.com/cjkpl/wagtail-cache.git
pip install git+https://github.com/cjkpl/wagtail-seo.git
```

## Summary

Out of the box, CjkCMS provides your project with generic, reusable pages:
`ArticleIndex`, `Article`, `WebPage` which you can use in your project, or extend with additional functionality. CjkCMS pages provide you with a generic "body" section and, using `wagtail-seo` package, a basic SEO functionality.

## Documentation
Documentation is a work in progress. See here: [Docs](https://github.com/cjkpl/django-cjkcms/blob/main/docs/index.md)

For a quick overview, see the [quick start guide](https://github.com/cjkpl/django-cjkcms/blob/main/docs/quick-start.md)

For detailed installation instructions, see the [installation guide](https://github.com/cjkpl/django-cjkcms/blob/main/docs/installation.md)

## Contact & support
Please use [Github's Issue Tracker](https://github.com/cjkpl/django-cjkcms/issues) to report bugs, request features, or request support.