__author__ = 'Mirko Rossini'

import unittest
from integrationtest_support import IntegrationTestSupport
from pybuilder.errors import BuildFailedException
from common import BUILD_FILE_TEMPLATE


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


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_django_test(self):
        self.write_build_file(BUILD_FILE_TEMPLATE.format(apps=['testapp']))
        reactor = self.prepare_reactor()
        try:
            reactor.build()
            raise self.failureException("Build should fail due to project missing, but it's successful")
        except BuildFailedException:
            # We know tests are failing
            pass
            # self.rm_tmp_dir()



if __name__ == "__main__":
    unittest.main()
