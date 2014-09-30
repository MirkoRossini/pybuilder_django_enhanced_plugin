from pybuilder import BuildFailedException

__author__ = 'Mirko Rossini'

import unittest
import shutil
from integrationtest_support import IntegrationTestSupport
from common import BUILD_FILE_TEMPLATE_CUSTOM_COMMAND


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_django_test(self):
        self.write_build_file(BUILD_FILE_TEMPLATE_CUSTOM_COMMAND.format(
            apps=['testapp'],
            commands=[['failing_command', 'myarg']]
            ))
        shutil.copytree('src/integrationtest/resources/testproject/',
                        self.full_path('src/main/python/testproject/'))
        reactor = self.prepare_reactor()

        try:
            reactor.build()
            raise self.failureException("Build should fail due to django_tests, but it's successful")
        except BuildFailedException:
            # We know tests are failing
            pass
        self.assert_directory_exists('target/reports')
        self.assert_file_exists('target/reports/django_management_command_failing_command')
        self.assert_file_exists('target/reports/django_management_command_failing_command.err')
        self.assert_file_contains('target/reports/django_management_command_failing_command.err',
                                  "Command failed")



if __name__ == "__main__":
    unittest.main()
