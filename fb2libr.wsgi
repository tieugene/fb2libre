import os, sys, locale

locale.setlocale(locale.LC_TIME,'ru_RU.utf8')

sys.path.append('/usr/share/fb2libre')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
