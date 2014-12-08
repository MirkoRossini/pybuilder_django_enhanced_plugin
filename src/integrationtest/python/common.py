__author__ = 'Mirko Rossini'

BUILD_FILE_TEMPLATE = """
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import django_test
use_plugin("python.core")


name = "integration-test"
default_task = ["django_test"]

@init
def init (project):
    project.set_property('django_project', 'testproject')
    project.set_property('django_apps', {apps})
    project.set_property('django_subpath', 'testproject')

"""

BUILD_FILE_TEMPLATE_AUTO = """
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import run_django_test
use_plugin("python.core")


name = "integration-test"
default_task = ["run_unit_tests"]

@init
def init (project):
    project.set_property('django_project', 'testproject')
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
    project.set_property('django_project', 'testproject')
    project.set_property('django_apps', {apps})
    project.set_property('django_subpath', 'testproject')
    project.set_property('django_management_commands', {commands})

"""

BUILD_FILE_TEMPLATE_COVERAGE = """
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import django_coverage
use_plugin("python.core")


name = "integration-test"
default_task = ["django_coverage"]

@init
def init (project):
    project.set_property('django_project', 'testproject')
    project.set_property('django_apps', {apps})
    project.set_property('django_subpath', 'testproject')
"""


BUILD_FILE_TEMPLATE_MIGRATION = """
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import django_migrate, django_makemigrations
use_plugin("python.core")


name = "integration-test"
default_task = ["django_makemigrations", "django_migrate"]

@init
def init (project):
    project.set_property('django_project', 'testproject')
    project.set_property('django_apps', {apps})
    project.set_property('django_subpath', 'testproject')
"""


BUILD_FILE_TEMPLATE_SYNCDB = """
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import django_syncdb
use_plugin("python.core")


name = "integration-test"
default_task = ["django_syncdb"]

@init
def init (project):
    project.set_property('django_project', 'testproject')
    project.set_property('django_apps', {apps})
    project.set_property('django_subpath', 'testproject')
"""


BUILD_FILE_TEMPLATE_COVERAGE_AUTO = """
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import verify_django_coverage
use_plugin("python.core")


name = "integration-test"
default_task = ["analyze"]

@init
def init (project):
    project.set_property('django_project', 'testproject')
    project.set_property('django_apps', {apps})
    project.set_property('django_subpath', 'testproject')
"""

BUILD_FILE_E2E = """
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import django_e2e_tests
use_plugin("python.core")


name = "integration-test"
default_task = ["django_e2e_tests"]

@init
def init (project):
    project.set_property('django_project', 'testproject')
    project.set_property('django_apps', {apps})
    project.set_property('django_subpath', 'testproject')
    project.set_property('django_fixtures', ['{{django_base_path}}/goodapp/fixtures/myfixture.json'])
    project.set_property('django_e2e_test_commands', [['curl_test', 'curl', '127.0.0.1:8000']])
"""