C2P2 - Simple markdown pages publisher
======================================

**C**ode -> **C**ommit -> **P**ush -> **P**ublish

Usage
-----

Init

.. code-block:: bash
    virtualenv venv --no-site-packages -p /usr/local/bin/python3.5
    source venv/bin/activate
    pip install c2p2
    python engine/main.py --DEFAULT_LABEL=blog

Production

Supervisor configuration:

.. code-block:: conf
    [program:blog]
    process_name=blog
    directory=/home/user/blog
    environment=C2P2_PORT=5000
    command=/home/user/envs/c2p2/bin/python /home/user/blog/engine/main.py
    user=user
    stdout_logfile=/var/log/blog/out.log
    stderr_logfile=/var/log/blog/err.log
    autostart=true
    autorestart=true

Nginx configuration:

.. code-block:: nginx
    upstream blog {
        server 127.0.0.1:5000;
    }

    server {
        listen   80;

        # If you need to restrict access
        # auth_basic "Restricted";
        # auth_basic_user_file /etc/nginx/.htpasswd;

        server_name mysite.com;

        location / {
            proxy_cache off;
            proxy_pass http://blog;
        }

        location ~* \.(?:css|png|jpe?g|gif|ico)$ {
            root /home/user/blog;
            log_not_found off;
        }
    }

Settings
--------

The application looks for settings in next sequence:
    - default settings (see ``c2p2/settings.py``)
    - environment variables with ``C2P2_`` prefix
    - command line arguments (``app.py --PORT=5000``)

Available settings:
    - ``DEBUG``: Enable debug mode
    - ``PORT``: Port app listening to
    - ``SOURCE_FOLDER``: Path to the folder contains pages source
    - ``DEFAULT_LABEL``: Default label (for index page)
    - ``WATCH``: Watch for changes in the source files
    - ``GITHUB_VALIDATE_IP``: Enable github ip validation
    - ``GITHUB_SECRET``: GitHub hooks secret, not required
    - ``GITHUB_BRANCH``: GitHub branch to watch

GitHub web hook
---------------

Executes ``<SOURCE_FOLDER>/pull.sh`` script:

.. code-block:: bash
    cd .. && git checkout master && git pull origin master

Requires permission:

.. code-block:: bash
    chmod +x pull.sh

Contribute
----------

If you want to contribute to this project, please perform the following steps:

..code-block:: bash
    # Fork this repository
    $ virtualenv .env --no-site-packages -p /usr/local/bin/python3.3
    $ source .env/bin/activate
    $ python setup.py install
    $ pip install -r requirements.txt

    $ git branch feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send me a pull request for your feature branch

Resources
---------

Resources used:
    - http://kevinburke.bitbucket.org/markdowncss/
    - https://github.com/richleland/pygments-css
