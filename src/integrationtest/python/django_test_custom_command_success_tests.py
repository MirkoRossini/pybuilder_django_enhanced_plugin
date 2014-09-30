__author__ = 'Mirko Rossini'

import unittest
import shutil
from integrationtest_support import IntegrationTestSupport
from common import BUILD_FILE_TEMPLATE_CUSTOM_COMMAND


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_django_test(self):
        self.write_build_file(BUILD_FILE_TEMPLATE_CUSTOM_COMMAND.format(
            apps=['testapp'],
            commands=[['working_command', 'myarg']]
            ))
        shutil.copytree('src/integrationtest/resources/testproject/',
                        self.full_path('src/main/python/testproject/'))
        reactor = self.prepare_reactor()
        reactor.build()
        self.assert_directory_exists('target/reports')
        self.assert_file_exists('target/reports/django_management_command_working_command')
        self.assert_file_exists('target/reports/django_management_command_working_command.err')
        self.assert_file_contains('target/reports/django_management_command_working_command',
                                  "Command called with argument: myarg")



if __name__ == "__main__":
    unittest.main()
