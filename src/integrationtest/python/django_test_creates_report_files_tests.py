__author__ = 'Mirko Rossini'

import unittest
import shutil
from integrationtest_support import IntegrationTestSupport
from pybuilder.errors import BuildFailedException
from common import BUILD_FILE_TEMPLATE


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_django_test(self):
        # self.set_tmp_dir()
        self.write_build_file(BUILD_FILE_TEMPLATE.format(apps=['testapp']))
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
