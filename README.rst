===
apitester
===

Installation
============

Install all necessary packages with::

    pip install -r requirements.txt

Create `local_settings.py` file. (Use `local_settings.py.def` as a template)

Run::

    python manage.py syncdb --noinput
    python manage.py runserver

You should be good to go.
