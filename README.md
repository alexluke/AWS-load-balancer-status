AWS Load Balancer Status
========================
A status page for monitoring instances attached to an elastic load balancer.

Setup
=====
Create a `settings.cfg` file like the following:

```python
ACCESS_KEY = 'your_aws_access_key'
SECRET_KEY = 'your aws_secret_key'
# A list of load balancers you want to monitor
LOAD_BALANCERS = [
	'name_of_elb1',
	'name_of_elb2',
]
```

Create a virtualenv and install required packages:

```
$ virtualenv venv --distribute
$ pip -E venv install -r requirements.txt
```

Deploy
======

mod\_wsgi
---------

Create an `application.wsgi` file:

```python
activate_this = '/path/to/app/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_This))
from monitor import app as application
```

Create an apache vhost file:

```
<VirtualHost *>
	ServerName example.com

	WSGIDaemonProcess lb_monitor user=www-data group=www-data threads=5
	WSGIScriptAlias / /path/to/app/application.wsgi

	<Directory /path/to/app>
		WSGIProcessGroup lb_monitor
		WSGIApplicationGroup %{GLOBAL}
		WSGIScriptReloading On
		Order deny,allow
		Allow from all
	</Directory>
</VirtualHost>
```

See the [Flask deployment documentation](http://flask.pocoo.org/docs/deploying/) for other WSGI servers.
