# Webpack support

## Setting up new project with Webpack support

Start with a new project, using the webpack template:

```
mkdir mysite
cd mysite
python3.11 -m venv env-mysite
source ./env-mysite/bin/activate
pip install wagtail-cjkcms
cjkcms mysite --template=webpack

cd mysite
npm install

# you will need two console windows open:
npm start # terminal #1
./manage.py runserver # terminal #2
```