import shutil
import stat
import sys
import os
import urllib2
import urlparse
import xml.sax.saxutils
from paste.script import templates, command
from paste.script.templates import NoDefault
from datashackleproject.utils import run_buildout
from datashackleproject.utils import ask_var
from datashackleproject.utils import get_boolean_value_for_option
from datashackleproject.utils import get_ssha_encoded_string
from datashackleproject.utils import create_buildout_default_file
from datashackleproject.utils import exist_buildout_default_file

GROK_RELEASE_URL = 'http://grok.zope.org/releaseinfo/'

class DatashackleProject(templates.Template):
    _template_dir = 'template'
    summary = "A datashackle project"
    required_templates = []
    vars = [
        ask_var('app_type', 'Should I create a pyramid or grok application?',
                default=NoDefault, should_ask=True),
        ask_var(
            'user', 'Name of an initial administrator user',
            default=NoDefault),
        ask_var(
            'passwd', 'Password for the initial administrator user',
            default=NoDefault),
        ask_var(
            'db_user', 'Name of the database user', default=NoDefault
            ),
        ask_var(
            'db_password', 'Password of the database user', default=NoDefault
            ),
        ask_var(
            'db_name', 'Name of the database', default=NoDefault
            ),
        ask_var(
            'db_host', 'Name of the database host', default=NoDefault
            ),
        ask_var(
            'newest', 'Check for newer versions of packages',
            default='false', should_ask=False,
            getter=get_boolean_value_for_option),
        ask_var(
            'run_buildout', (
            "After creating the project area, run the buildout."),
            default=False, should_ask=False,
            getter=get_boolean_value_for_option),
        ask_var(
            'use_distribute',
            "Use Distribute instead of setuptools for this project.",
            default=False, should_ask=False,
            getter=get_boolean_value_for_option),
        ask_var(
            'eggs_dir',
            'Location where zc.buildout will look for and place packages',
            default='', should_ask=False),
        ]

    def check_vars(self, vars, cmd):
        if vars['package'] in ('grok', 'zope'):
            print
            print "Error: The chosen project name results in an invalid " \
                  "package name: %s." % vars['package']
            print "Please choose a different project name."
            sys.exit(1)

        explicit_eggs_dir = vars.get('eggs_dir')

        skipped_vars = {}
        for var in list(self.vars):
            if not var.should_ask:
                skipped_vars[var.name] = var.getter(vars, var)
                self.vars.remove(var)

        expect_vars = self.read_vars(cmd)
        converted_vars = {}
        unused_vars = vars.copy()
        errors = []
        for var in expect_vars:
            if var.name not in unused_vars:
                if cmd.interactive:
                    prompt = 'Enter %s' % var.full_description()
                    while True:
                        response = cmd.challenge(prompt, var.default, var.should_echo)
                        if var.name == 'app_type' and response not in ['pyramid', 'grok']:
                            print "Error: Please enter 'pyramid' OR 'grok'. This way I can create " \
                                   "an appropriate application skeleton for you."
                        else:
                            break
                    converted_vars[var.name] = response
                elif var.default is command.NoDefault:
                    errors.append('Required variable missing: %s'
                                  % var.full_description())
                else:
                    converted_vars[var.name] = var.default
            else:
                converted_vars[var.name] = unused_vars.pop(var.name)
        if errors:
            raise command.BadCommand(
                'Errors in variables:\n%s' % '\n'.join(errors))
        converted_vars.update(unused_vars)
        vars.update(converted_vars)
        
        for name in skipped_vars:
            vars[name] = skipped_vars[name]

        vars['passwd'] = get_ssha_encoded_string(vars['passwd'])
        for var_name in ['user', 'passwd']:
            # Escape values that go in site.zcml.
            vars[var_name] = xml.sax.saxutils.quoteattr(vars[var_name])
        vars['app_class_name'] = vars['project'].capitalize()
        vars['project_lowercase'] = vars['project'].lower()

        # Handling the version.cfg file.
        version_url = vars.get('version_url')
        find_links_url = ''
        if version_url is None:
            print "Determining current grok version..."
            # If no version URL was specified, we look up the current
            # version first and construct a URL.
            current_info_url = urlparse.urljoin(GROK_RELEASE_URL, 'current')
            version = self.download(current_info_url).strip().replace(
                    'grok-', '').replace('.cfg', '')
            version_url = GROK_RELEASE_URL + version + '/versions.cfg'
            find_links_url = GROK_RELEASE_URL + version + '/eggs'

        vars['find_links_url'] = find_links_url
        vars['version_info_url'] = version_url

        buildout_default = exist_buildout_default_file()
        if explicit_eggs_dir:
            # Put explicit_eggs_dir in the vars; used by the post command.
            vars['explicit_eggs_dir'] = explicit_eggs_dir
            vars['eggs_dir'] = (
                '# Warning: when you share this buildout.cfg with friends\n'
                '# please remove the eggs-directory line as it is hardcoded.\n'
                'eggs-directory = %s') % explicit_eggs_dir
        elif buildout_default:
            vars['eggs-dir'] = ''
        else:
            create_buildout_default_file()

        vars['package_directory'] = os.path.abspath(os.path.join(
                os.getcwd(), vars['project']))

        include_site_packages = vars.get('include_site_packages')
        if include_site_packages is None:
            vars['include_site_packages'] = 'false'

        return vars

    def download(self, url):
        """Downloads a file and returns the contents.

        If an error occurs, we abort, giving some information about
        the reason.
        """
        contents = None
        try:
            contents = urllib2.urlopen(url).read()
        except urllib2.HTTPError:
            # Some 404 or similar happened...
            print "Error: cannot download required %s" % url
            print "Maybe you specified a non-existing version?"
            sys.exit(1)
        except IOError, e:
            # Some serious problem: no connect to server...
            print "Error: cannot download required %s" % url
            print "Server may be down.  Please try again later."
            sys.exit(1)
        return contents

    def post(self, command, output_dir, vars):
        path = os.path.join(os.getcwd(), vars['project'])
        path = os.path.join(path, 'bin')
        path = os.path.join(path, 'pidproxy.py')
        mode = os.stat(path)[stat.ST_MODE]
        mode |= stat.S_IXUSR
        os.chmod(path, mode)  


        if vars['app_type'] == 'pyramid':
            src = os.path.sep.join([vars['package_directory'], 'src'])
            # remove grok application skeleton
            shutil.rmtree(os.path.sep.join([src, 'grok']))
            # move pyramid application up one dir
            dst = os.path.sep.join([src, vars['package']])
            target = os.path.sep.join([src, 'pyramid', vars['package']])
            os.rename(target, dst)
            shutil.rmtree(os.path.sep.join([src, 'pyramid']))
        elif vars['app_type'] == 'grok':
            src = os.path.sep.join([vars['package_directory'], 'src'])
            # remove pyramid application skeleton
            shutil.rmtree(os.path.sep.join([src, 'pyramid']))
            # move pyramid application up one dir
            dst = os.path.sep.join([src, vars['package']])
            target = os.path.sep.join([src, 'grok', vars['package']])
            os.rename(target, dst)
            shutil.rmtree(os.path.sep.join([src, 'grok']))

        if not vars['run_buildout']:
            return
        original_dir = os.getcwd()
        os.chdir(vars['project'])
        run_buildout(command.verbose, vars['use_distribute'])
        os.chdir(original_dir)
