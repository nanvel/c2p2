# C2P2 - Simple markdown pages publisher

**C**ode
**C**ommit
**P**ush
**P**ublish

Usage
-----

Environment:
```bash
virtualenv venv --no-site-packages -p /usr/local/bin/python3.5
source venv/bin/activate
pip install -r requirements.txt
```

Example page, just run:
```bash
python app.py
```
and open ```localhost:5000```.

Custom settings:
```bash
EXPORT C2P2_SOURCE_FOLDER=/path/to/source/folder
EXPORT C2P2_PORT=5000
python venv/bin/python app.py
```

Supervisor configuration:
```conf
[program:app-docs]
process_name=app-docs
directory=/home/user/c2p2
environment=C2P2_PORT=5000,C2P2_SOURCE_FOLDER=/home/user/c2p2/docs
command=/home/user/c2p2/venv/bin/python app.py
user=user
stdout_logfile=/var/log/c2p2/out.log
stderr_logfile=/var/log/c2p2/err.log
autostart=true
autorestart=true
```

Nginx configuration:
```nginx
upstream c2p2-app {
    server 127.0.0.1:5000;
}

server {
    listen   80;

    auth_basic "Restricted";
    auth_basic_user_file /etc/nginx/.htpasswd;

    server_name docs.myproject.com;

    location / {
        proxy_cache off;
        proxy_pass http://c2p2-app;
    }

    location ~* \.(?:css|png|jpe?g|gif|ico)$ {
        root /home/user/myproject/docs;
        log_not_found off;
    }
}
```

Settings
--------

It looks for settings in next sequence:
- default settings (see ```c2p2/settings.py```)
- environment variables with ```C2P2_``` prefix
- command line arguments (```app.py --PORT=5000```)

Available settings:
- ```DEBUG```: Enable debug mode
- ```PORT```: Port app listening to
- ```SITE_NAME```: Site name, show in title
- ```BASE_URL```: Site base url, uses in sitemap.xml
- ```SOURCE_FOLDER```: Relative or absolute path to the folder contains pages source
- ```DEFAULT_LABEL```: Default label (for index page)
- ```THEME```: Theme name
- ```WATCH```: Watch for changes in the source files

GitHub web hook
---------------

```bash
chmod +x pull.sh
```

Tests
-----

```python
python -m unittest c2p2.tests
```

Contribute
----------

If you want to contribute to this project, please perform the following steps:
```bash
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
```

Resources
---------

Themes used:
- http://kevinburke.bitbucket.org/markdowncss/
- https://github.com/richleland/pygments-css
