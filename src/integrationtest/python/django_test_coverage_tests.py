__author__ = 'Mirko Rossini'

import unittest
import shutil
from integrationtest_support import IntegrationTestSupport
from pybuilder.errors import BuildFailedException
from common import BUILD_FILE_TEMPLATE_COVERAGE


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_django_test(self):
        # self.set_tmp_dir()
        self.write_build_file(BUILD_FILE_TEMPLATE_COVERAGE.format(apps=['goodapp']))
        shutil.copytree('src/integrationtest/resources/testproject/', self.full_path('src/main/python/testproject/'))
        reactor = self.prepare_reactor()
        reactor.build()
        self.assert_directory_exists('target/reports')
        self.assert_file_exists('target/reports/django_coverage')
        self.assert_file_exists('target/reports/django_coverage.err')
        self.assert_file_contains('target/reports/django_coverage', 'TOTAL')

if __name__ == "__main__":
    unittest.main()
