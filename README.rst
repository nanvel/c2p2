C2P2 - Simple markdown pages publisher
======================================

**C**\ ode
**C**\ ommit
**P**\ ush
**P**\ ublish

Installation
------------

.. code-block:: bash

    pip install c2p2

or

.. code-block:: bash

    pip install git+https://github.com/nanvel/c2p2.git

Usage
-----

Fork c2p2_template
~~~~~~~~~~~~~~~~~~

The easiest way to start is to fork this template: https://github.com/nanvel/c2p2-template.

Templates API
~~~~~~~~~~~~~

The application looks for templates inside SOURCE_FOLDER, so we need to add them.
Minimal list of files required is:

.. code-block:: text

    - site
        - engine
            - templates
                - 404.html
                - 500.html
                - index.html
                - page.html
                - label.html
                - sitemap.xml

``index.html``, ``page.html``, ``label.html`` and ``sitemap.xml`` receives, beside `tornado standart template context <http://www.tornadoweb.org/en/stable/guide/templates.html>`__,  
variable ``c``, that uses to access list of pages and labels, for example:

.. code-block:: django

    {{ c.page }}
    {{ c.page.title }}
    {{ c.page.labels }}
    {{ c.label }}
    {% for page in c.pages %}
    {{ c.pages['<page_slug>'] }}
    {{ c.pages.for_label('<label_slug>') }}

``c.page`` is available only in ``page.html``.
It returns current page object.

``Page`` object has next attributes:
    - uri
    - html
    - created
    - modified
    - title
    - meta
    - labels

``page.meta`` returns ``PageMeta`` object, where all variables specified in the top of the page is available.

.. code-block:: text

    // page.md
    created: 2015-10-10T00:00
    show_comments: true
    labels: Label1
            Label2

.. code-block:: django

    // page.html
    {{ c.page.meta.created }} -> '2015-10-10T00:00'
    {{ c.page.meta.created }} -> '2015-10-10T00:00'
    {{ c.page.meta.labels }} -> 'Label1'
    {{ c.page.meta.get('labels') }} -> 'Label1'
    {{ c.page.meta.get_list('labels') }} -> ['Label1', 'Label2']
    {{ c.page.meta.show_comments }} -> true
    {{ c.page.meta.not_exist }} -> None

``page.labels`` returns list of Label objects connected to the page:

.. code-block:: django

    {% for label in c.page.labels %}{{ label.title }}{% end %}

``Label`` object has next attributes:
    - title
    - slug

``c.pages`` returns an iterable that allows to get all pages list. In ``label.html`` it return only pages belong to the label.
You also can get any page by uri using ``c.pages``.

.. code-block:: django

    {% for page in c.pages %}{{ page.title }}{% end %}

    {{ c.pages['2010/09/blog-post'].html }}

    {{ c.pages.for_label('default') }}

Running the server
~~~~~~~~~~~~~~~~~~

To run the application use ``site/engine/app.py``:

.. code-block:: python

    import os.path

    from c2p2 import app
    from c2p2.settings import settings


    rel = lambda p: os.path.join(os.path.dirname(os.path.realpath(__file__)), p)


    if __name__ == '__main__':
        settings.SOURCE_FOLDER = rel('..')
        app.run()

Settings
--------

There are 4 ways to set settings:
    - default settings (see ``c2p2/settings.py``)
    - environment variables with ``C2P2_`` prefix: ``export C2P2_PORT=5000``
    - command line arguments (``app.py --PORT=5000``)
    - also you can change them directly ``settings.PORT = 5000`` in ``site/engine/app.py`` 

Available settings:
    - ``DEBUG``: Enable tornado debug mode
    - ``PORT``: Port the app listening to
    - ``SOURCE_FOLDER``: Path to folder that contains pages source
    - ``UPDATE_TIMEOUT``: Number of seconds to rescan source folder. 0 - disable
    - ``GITHUB_VALIDATE_IP``: Enable GitHub ip validation
    - ``GITHUB_SECRET``: GitHub web hook secret, optional
    - ``GITHUB_BRANCH``: GitHub branch to watch

Questions and Answers
---------------------

Run on work station
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cd site
    virtualenv venv --no-site-packages -p /usr/local/bin/python3.5
    source venv/bin/activate
    pip install c2p2
    python engine/app.py

Open ``http://localhost:5000`` in browser.

Update site if md file was changed without server restart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use UPDATE_TIMEOUT setting.

Update site on GitHub push
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create new GitHub hook for your repository:
    - url: ``http://mysite.com/pull``
    - secret: should be equal to GITHUB_SECRET setting value

Production configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Settings:
    - DEBUG=false
    - UPDATE_TIMEOUT=0
    - GITHUB_VALIDATE_IP=true
    - GITHUB_SECRET=<webhook secret>
    - GITHUB_BRANCH=master

Supervisor configuration:

.. code-block:: text

    [program:mysite]
    process_name=mysite
    directory=/home/deploy/mysite
    environment=C2P2_PORT=5100,C2P2_DEBUG=false,C2P2_UPDATE_TIMEOUT=0,C2P2_GITHUB_VALIDATE_ID=true,C2P2_GIHUB_SECRET=123xyz,C2P2_GITHUB_BRANCH=master
    command=/home/deploy/mysite/venv/bin/python engine/app.py
    user=deploy
    stdout_logfile=/var/log/mysite/out.log
    stderr_logfile=/var/log/mysite/err.log
    autostart=true
    autorestart=true

Nginx configuration:

.. code-block:: nginx

    upstream mysite {
        server 127.0.0.1:5100;
    }

    server {
        listen   80;

        # If you need to restrict access
        # auth_basic "Restricted";
        # auth_basic_user_file /etc/nginx/.htpasswd;

        server_name mysite.com;

        location / {
            proxy_cache off;
            proxy_pass http://mysite;
        }

        location ~* \.(?:css|png|jpe?g|gif|ico|zip|txt)$ {
            root /home/deploy/mysite;
            log_not_found off;
        }

        error_page 500 502 503 504 /home/deploy/mysite/engine/templates/500.html;
        error_page 400 402 403 404 /home/deploy/mysite/engine/templates/400.html;
    }

Favicon and robots.txt
~~~~~~~~~~~~~~~~~~~~~~

Just add favicon.ico and robots.txt to root folder of your site.

Custom md directives
~~~~~~~~~~~~~~~~~~~~

It is possible to register custom md directives:

.. code-block:: python

    from c2p2.utils import ExtensionsRegistry

    ExtensionsRegistry.register(extension=MyExtension)

Edit on GitHub link
~~~~~~~~~~~~~~~~~~~

.. code-block:: django

    <a href="https://github.com/nanvel/mysite/blob/master/{{ c.page.uri }}.md" target="_blank">Edit on GitHub</a>

Tests
-----

.. code-block:: bash

    python -m unittest c2p2.tests

Contribute
----------

If you want to contribute to this project, please perform the following steps:

.. code-block:: bash

    # Fork this repository
    $ virtualenv .env --no-site-packages -p /usr/local/bin/python3.5
    $ source .env/bin/activate
    $ python setup.py install
    $ pip install -r requirements.txt

    $ git branch feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send me a pull request for your feature branch
