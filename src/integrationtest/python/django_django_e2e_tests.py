__author__ = 'Mirko Rossini'

import unittest
import shutil
from integrationtest_support import IntegrationTestSupport
from common import BUILD_FILE_E2E


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_django_e2e_test(self):
        # self.set_tmp_dir()
        self.write_build_file(BUILD_FILE_E2E.format(apps=['goodapp']))
        shutil.copytree('src/integrationtest/resources/testproject/', self.full_path('src/main/python/testproject/'))
        reactor = self.prepare_reactor()
        reactor.build()
        self.assert_directory_exists('target/reports')
        self.assert_file_exists('target/reports/django_e2e_tests_server')
        self.assert_file_exists('target/reports/django_e2e_tests_server.err')
        self.assert_file_contains('target/reports/django_e2e_tests_server', 'Quit the server with CONTROL-C.')
        self.assert_file_contains('target/reports/django_e2e_tests_server.err', '"GET / HTTP/1.1" 200')

if __name__ == "__main__":
    unittest.main()
