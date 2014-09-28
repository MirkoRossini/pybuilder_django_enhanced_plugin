__author__ = 'Mirko Rossini'

import unittest
import shutil
from integrationtest_support import IntegrationTestSupport
from pybuilder.errors import BuildFailedException


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_something(self):
        self.write_build_file("""
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import django_test
use_plugin("python.core")


name = "integration-test"
default_task = ["django_test"]

@init
def init (project):
    project.set_property('django_module', 'testproject')
    project.set_property('django_apps', ['testapp'])
    project.set_property('django_subpath', 'testproject')

""")
        shutil.copytree('src/integrationtest/resources/testproject/', self.full_path('src/main/python/testproject/'))
        reactor = self.prepare_reactor()
        try:
            reactor.build()
            raise self.failureException("Build should fail due to django_tests, but it's successful")
        except BuildFailedException:
            # We know tests are failing
            pass
        self.assert_directory_exists('target/reports')
        self.assert_file_exists('target/reports/django_tests')
        self.assert_file_exists('target/reports/django_tests.err')
        self.assert_file_contains('target/reports/django_tests.err', 'FAIL')
        self.assert_file_contains('target/reports/django_tests.err', 'AssertionError: 1 != 2')


if __name__ == "__main__":
    unittest.main()
