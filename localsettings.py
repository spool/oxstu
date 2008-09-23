from os.path import abspath, dirname, join, split
from site import addsitedir
import sys
FILEROOT = '/Users/griff/src/django-hotclub/oxstu'
path = addsitedir(abspath(split(FILEROOT)[0]), set())
if path: sys.path = list(path) + sys.path
sys.path.insert(0, abspath(join(FILEROOT, 'libs')))
sys.path.insert(0, abspath(join(FILEROOT, 'apps')))
sys.path.insert(0, abspath(join(FILEROOT, 'external_apps')))

import settings

OXSTU_APPS = (
        'story',
        'issue',
        'mptt',
        'section',
        'typogrify',
        'oxnews',
        )

INSTALLED_APPS = settings.INSTALLED_APPS + OXSTU_APPS

# Uncomment/comment which one you want/don't want
ROOT_URLCONF = 'pinax.urls'
# ROOT_URLCONF = 'oxstu.urls'

OXSTU_TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(FILEROOT, 'templates'),
)

# Switch these to use pinax's default templates.
# TEMPLATE_DIRS = OXSTU_TEMPLATE_DIRS + settings.TEMPLATE_DIRS 
TEMPLATE_DIRS = settings.TEMPLATE_DIRS + OXSTU_TEMPLATE_DIRS

# Will be deprecated I hope...
PHOTOROOT = join(FILEROOT, "static", "photos")

# Comment out to get pinax defaults
#MEDIA_ROOT = join(FILEROOT, 'static', 'media')

# Comment out to get pinax defaults
#MEDIA_URL = '/media/'

#To make use of Django User profile stuff (see b-list.org: 'Extending the user model')
#AUTH_PROFILE_MODULE = 'oxnews.StaffUser'
