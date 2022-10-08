## Rationale

CjkCMS is based on a fork of another CMS system, Wagtail CMS / CRX.

While the original system is a great tool as a standalone Wagtail project, CjkCMS aims to be a lightweight alternative, installable as a Django/Wagtail application into any existing Wagtail project.


The rationale behind CjkCMS and the key differences between CjkCMS and CRX are:
- CjkCMS can be installed as a new app onto an existing Wagtail website. CRX expects you to set up a new Wagtail site with the CMS support enabled.
- CjkCMS removed from CRX some features that we do not find useful (i.e. features that we have not used even once over the last 18+ months), for example: Content Walls, Locations, Events, FlexForms.
- CjkCMS adds new features not present in CRX, e.g. support for protected (domain-locked) Vimeo files, support for both plain [Bootstrap5](https://getbootstrap.com/) and [MDBootstrap5](https://mdbootstrap.com/), as well as [Django-Webpack-Boilerplate](https://github.com/AccordBox/python-webpack-boilerplate)

[Wagtail CMS/CRX](https://docs.coderedcorp.com/wagtail-crx/) is a fantastic piece of software, with great documentation, and our modified fork would not be possible without it. Thank you, dev team! 
