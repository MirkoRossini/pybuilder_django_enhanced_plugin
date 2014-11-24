import os

__author__ = 'Mirko Rossini'

import unittest
from integrationtest_support import IntegrationTestSupport
from common import BUILD_FILE_TEMPLATE


BUILD_FILE_TEMPLATE = """
from pybuilder.core import use_plugin, init

from pybuilder_django_enhanced_plugin import django_generate
use_plugin("python.core")


name = "integration-test"
default_task = ["django_generate"]

@init
def init (project):
    project.set_property('django_project', 'testproject')
    project.set_property('django_apps', {apps})

"""


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_django_test(self):
        os.makedirs(self.full_path('src/main/python/'))
        self.write_build_file(BUILD_FILE_TEMPLATE.format(apps=['app1', 'app2']))
        reactor = self.prepare_reactor()
        reactor.build()
        self.assert_directory_exists('src/main/python/testproject')
        self.assert_directory_exists('src/main/python/app1')
        self.assert_directory_exists('src/main/python/app2')


if __name__ == "__main__":
    unittest.main()
