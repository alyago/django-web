import os
from django.conf import settings

TOOLS_DIR = os.path.abspath(os.path.join(settings.SITE_ROOT_PATH, 'tools'))
LESSC_CMD = 'PATH=%s/nodejs:${PATH} && %s' % (TOOLS_DIR, os.path.join(TOOLS_DIR, 'less/bin/lessc'))
MINIFY_CMD = 'java -jar %s/deploy-tools/yuicompressor-2.4.7/build/yuicompressor-2.4.7.jar' % TOOLS_DIR

CSS_PATH = os.path.abspath(settings.SITE_ROOT_PATH + 'jobs/static/jobs/css')
JS_PATH = os.path.abspath(settings.SITE_ROOT_PATH + 'jobs/static/jobs/js')
TEMPLATE_PATH = os.path.abspath(settings.SITE_ROOT_PATH + 'jobs/templates')
