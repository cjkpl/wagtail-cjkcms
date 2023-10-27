# Webpack support

## Setting up new project with Webpack support

Start with a new project, using the webpack template:

### Pre-config:
```bash
mkdir mysite
cd mysite
python3.11 -m venv env-mysite
source ./env-mysite/bin/activate
```

### Scaffolding of the new site:
```bash
pip install wagtail-cjkcms python-webpack-boilerplate # note additional package requirement
cjkcms mysite --template=webpack # change mysite to your project name
cd mysite
npm install
# ... continue with standard setup: migrate, createsuperuser:
python manage.py migrate
python manage.py createsuperuser
```

Starting a webpack-based website requires additional steps, compared to the standard CjkCMS setup.

1. In the scaffolding step above, you needed to additionally ```pip install python-webpack-boilerplate```.

2. For development, you will need two console windows open, rather than one:
```bash
npm start # terminal #1 - start first
./manage.py runserver # terminal #2
```

3. By default, the CMS is configured to use standard (CDN) Bootstrap 5.3. To switch to Webpack-based Bootstrap, you need to go to the admin interface (/backend) and in Settings->Layout->Theming -> change the source of your Bootstrap theme.

Then you can start developing your site. For example, try modifying the colors in ```frontend/src/styles/index.scss``` and see the changes in the browser:

```scss
$primary: rgb(201 136 79); // (no obvious change, as there is no element with primary color in default site content)
$light: rgb(132 201 140); // this will change e.g. the navbar background color, by default set to light.
```