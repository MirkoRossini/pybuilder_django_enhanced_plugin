__author__ = 'Mirko Rossini'
BUILD_FILE_TEMPLATE = """
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import django_test
use_plugin("python.core")


name = "integration-test"
default_task = ["django_test"]

@init
def init (project):
    project.set_property('django_module', 'testproject')
    project.set_property('django_apps', {apps})
    project.set_property('django_subpath', 'testproject')

"""

BUILD_FILE_TEMPLATE_CUSTOM_COMMAND = """
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import django_run_management_commands
use_plugin("python.core")


name = "integration-test"
default_task = ["django_run_management_commands"]

@init
def init (project):
    project.set_property('django_module', 'testproject')
    project.set_property('django_apps', {apps})
    project.set_property('django_subpath', 'testproject')
    project.set_property('django_management_commands', {commands})

"""