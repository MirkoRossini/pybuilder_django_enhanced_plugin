__author__ = 'Mirko Rossini'

import unittest
import shutil
from integrationtest_support import IntegrationTestSupport
from common import BUILD_FILE_TEMPLATE_AUTO


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_django_test(self):
        self.write_build_file(BUILD_FILE_TEMPLATE_AUTO.format(apps=['goodapp']))
        shutil.copytree('src/integrationtest/resources/testproject/',
                        self.full_path('src/main/python/testproject/'))
        reactor = self.prepare_reactor()
        reactor.build()
        self.assert_directory_exists('target/reports')
        self.assert_file_exists('target/reports/django_tests')
        self.assert_file_exists('target/reports/django_tests.err')


if __name__ == "__main__":
    unittest.main()
