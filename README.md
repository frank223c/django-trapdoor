# Django Trapdoor
## Build Status
[![Build Status](https://travis-ci.org/MikaSoftware/django-trapdoor.svg?branch=master)](https://travis-ci.org/MikaSoftware/django-trapdoor)
[![PyPI version fury.io](https://badge.fury.io/py/django-trapdoor.svg)](https://pypi.python.org/pypi/django-trapdoor)
[![Coverage Status](https://coveralls.io/repos/github/MikaSoftware/django-trapdoor/badge.svg?branch=master)](https://coveralls.io/github/MikaSoftware/django-trapdoor?branch=master)

## About
Automatically ban IP addresses requesting suspicious URL paths from your Django site.

## Supported Features
* Has record of [279 unique suspicious URL paths](https://github.com/MikaSoftware/django-trapdoor/blob/master/trapdoor/constants.py) used by malicious users to scan your django site.
* Automatic banning of IP addresses performing scanning attempts on your django site.
* The banning process attempts retrieving users real IP addresses, using the [django-ipware](https://github.com/un33k/django-ipware) library.

## Installation
### Requirements
* Python 3.6+ or Python 2.7
* Django 1.11+
* IPWare 1.1.6+

### Instructions
1. Clone the project.

  ```bash
  pip install django-trapdoor.git
  ```

2. Add ``trapdoor`` to your ``INSTALLED_APPS`` array in your **settings.py** file.

3. Add the following lines of code to your ``MIDDLEWARE_CLASSES`` array in your **settings.py** file.

  ```python
  MIDDLEWARE = [
    ...
    'trapdoor.middleware.TrapdoorMiddleware',
    ...
  ]
  ```

4. Update your database by running the following in your console

  ```bash
  python manage.py migrate
  ```

## Usage
### Operation
Once you enable the ``TrapdoorMiddleware`` middleware in your django app, every GET request gets analyzed as follows:

1. Lookup the users real IP address and confirm it’s not blocked, if blocked a ``403`` error gets returned to the user.
2. Else if real IP address is not blocked, check to see if the requested URL path is considered [suspicious](https://github.com/MikaSoftware/django-trapdoor/blob/master/trapdoor/constants.py) and if the path is then block immediately.
3. Else if request URL path is not suspicious then do nothing

If you would like to know the IP address of the request then use the ``request.trapdoor`` variable in your code.

This library also integrates with ``django-admin`` and thus you can further control removing/adding IP address to ban there.

### Command Line
#### remove_banned_ip.py
This command is to be used to remove a specific IP address that you feel no longer should be banned from your django website.

#### remove_banned_ips_older_then_by_days.py
This command is used to remove banned ips which are older then a certain day count. This is a command useful for if you want to run a ``cronjob`` or ``background process`` to run periodically and remove banned IPs that are older then a certain day count.

### Environment Settings Variables
#### TRAPDOOR_DO_NOT_BAN_IP_ADDRESSES
This is an array of IP addresses which will not get banned if they lookup suspicious paths. This is a useful variable to set if you plan on performing your own security audit or have a third party perform a security audit without getting banned.

#### TRAPDOOR_EXTRA_SUSPICIOUS_PATHS
This is an array of URL paths which can be added by yourself as extra paths to be used for blocking criteria. This is a useful variable if you find this libray missing a path that should be blocked.

## Contributing
If you have a *suspicious URL path* you would like to add, please [create a new issue](https://github.com/MikaSoftware/django-trapdoor/issues/new) and we will add it in! If you are a **developer** who feels you can improve this library, please do! We have written a [contributing](https://github.com/MikaSoftware/django-trapdoor/blob/master/CONTRIBUTING.md) document to help you get started.

## License
This library is licensed under the **BSD** license. See [LICENSE.md](LICENSE.md) for more information.

## Common Issues
If you get self banned for whatever reason, this means your ``nginx``, ``apache`` or whatever web-server you are using is not properly configured.
