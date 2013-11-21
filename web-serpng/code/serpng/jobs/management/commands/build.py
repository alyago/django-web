from django.core.management.base import BaseCommand, CommandError
import os
import subprocess
from jobs.management.commands import *

class Command(BaseCommand):
    help = 'Builds SERP dependencies'

    def __init__(self):
        self.css_files = {
            'serp_tabs.min.css': (
                '../widgets/fancybox/jquery.fancybox-1.3.4.pack.css',
                '../bootstrap/css/bootstrap-sh.css',
                'tabs_common.css',
                'tabs_jobs.css',
                'tabs_results.css',
                'tabs.css',
                'jquery-ui-1.8.20.custom.css',
            ),
            'serp_tabs_ie6.min.css': (
                '../widgets/fancybox/jquery.fancybox-1.3.4.pack.css',
                '../bootstrap/css/bootstrap-sh.css',
                'tabs_common.css', 
                'tabs_jobs.css',
                'tabs_results_ie6.css',
                'tabs.css',
                'jquery-ui-1.8.20.custom.css'
            ),
            'serp_port.min.css': (
                'port_common.css',
                'port_jobs.css',
                'port_results.css'
            ),
            'serp_port_ie6.min.css': (
                'port_common.css',
                'port_jobs.css',
                'port_results_ie6.css'
            ),
        }

        self.js_files = {
            'serp.min.js': (
                'lib/json2.js',
                'lib/underscore.js',
                'lib/backbone.js',
                'django-csrf.js',
                'jquery-ui-1.8.20.custom.min.js',
                '../widgets/fancybox/jquery.fancybox-1.3.4.pack.js',
                'sh_common.js',
                'autocomplete.js',
                'serp_utils.js',
                'myjobs.js',
                'serp.js',
                'event-logging.js',
                '../bootstrap/js/bootstrap.js',
            )
        }

    def compile_css(self):
        for filename in os.listdir(CSS_PATH):
            if filename.endswith('.less'):
                less_filename = os.path.join(CSS_PATH, filename)
                css_filename = os.path.join(CSS_PATH, filename.replace('less', 'css'))
                cmd = '%s %s > %s' % (LESSC_CMD, less_filename, css_filename)
                self.stdout.write("Executing %s\n" % cmd)
                subprocess.call(cmd, shell=True)

    def minify_css(self):
        for minified_filename, input_files in self.css_files.items():
            cat_filename = '/tmp/' + minified_filename.replace('.min', '')
            cat_cmd = 'cat %s > %s' % (' '.join(os.path.join(CSS_PATH, filename) for filename in input_files), cat_filename)
            self.stdout.write("Executing %s\n" % cat_cmd)
            subprocess.call(cat_cmd, shell=True)

            full_minified_filename = os.path.join(CSS_PATH, minified_filename)
            cmd = '%s %s -o %s' % (MINIFY_CMD, cat_filename, full_minified_filename)
            self.stdout.write("Executing %s\n" % cmd)
            subprocess.call(cmd, shell=True)

    def minify_js(self):

        stripped_filenames = []
        for minified_filename, input_files in self.js_files.items():

            # Strip console.log() messages from each js file
            for input_file in input_files:
                js_filename = os.path.join(JS_PATH, input_file)
                stripped_filename = js_filename.replace('.js', '.stripped.js')
                cmd = "sed 's/console.log(.*//' %s > %s" % (js_filename, stripped_filename)
                self.stdout.write("Executing %s\n" % cmd)
                subprocess.call(cmd, shell=True)
                stripped_filenames.append(stripped_filename)

            cat_filename = '/tmp/' + minified_filename.replace('.min', '')
            cat_cmd = 'cat %s > %s' % (' '.join(stripped_filenames), cat_filename)
            self.stdout.write("Executing %s\n" % cat_cmd)
            subprocess.call(cat_cmd, shell=True)

            full_minified_filename = os.path.join(JS_PATH, minified_filename)
            cmd = '%s %s -o %s' % (MINIFY_CMD, cat_filename, full_minified_filename)
            self.stdout.write("Executing %s\n" % cmd)
            subprocess.call(cmd, shell=True)

    def handle(self, *args, **options):
        self.compile_css()
        self.minify_css()
        self.minify_js()
