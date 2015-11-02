# -*- coding: utf-8 -*-
'''
urls
fb2libre 0.0.1
'''

from django.conf import settings

def	common_context(context):
	'''
	our context processor. Add to dict vars to send in ALL templates.
	'''
	return {
		'LOGIN_URL' : settings.LOGIN_URL,
		'path': 'apps.core'
	}
