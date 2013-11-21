from django.core.management.base import BaseCommand, CommandError
import os
import subprocess
from jobs.management.commands import *

class Command(BaseCommand):
    args = '<on|off>'
    help = 'Updates SERP to use minified CSS and Javascript files'

    _CSS_TEMPLATE_FILENAME = 'external_css.html'
    _MINIFIED_CSS_TEMPLATE_FILENAME = 'external_css_min.html'

    _JS_TEMPLATE_FILENAME = 'external_js.html'
    _MINIFIED_JS_TEMPLATE_FILENAME = 'external_js_min.html'

    _BASE_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, 'serp_common/serp_base.html')

    def replace_string(self, filename, old, new):
            cmd = 'sed -i "s/%s/%s/" %s' % (old, new, filename)
            self.stdout.write("Executing %s\n" % cmd)
            subprocess.call(cmd, shell=True)

    def use_minified(self):
            self.replace_string(self._BASE_TEMPLATE_PATH, self._CSS_TEMPLATE_FILENAME, self._MINIFIED_CSS_TEMPLATE_FILENAME)
            self.replace_string(self._BASE_TEMPLATE_PATH, self._JS_TEMPLATE_FILENAME, self._MINIFIED_JS_TEMPLATE_FILENAME)

    def use_unminified(self):
            self.replace_string(self._BASE_TEMPLATE_PATH, self._MINIFIED_CSS_TEMPLATE_FILENAME, self._CSS_TEMPLATE_FILENAME)
            self.replace_string(self._BASE_TEMPLATE_PATH, self._MINIFIED_JS_TEMPLATE_FILENAME, self._JS_TEMPLATE_FILENAME)

    def handle(self, *args, **options):

        use_minified = None
        if args:
            mode = args[0].lower()
            if mode == 'on':
                use_minified = True
            if mode == 'off':
                use_minified = False
            
        if use_minified == True:
            self.use_minified()
        elif use_minified == False:
            self.use_unminified()
        else:
            raise CommandError('Please specify either "on" or "off"!\n')
