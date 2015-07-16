from pybuilder import BuildFailedException

__author__ = 'Mirko Rossini'

import unittest
import shutil
from integrationtest_support import IntegrationTestSupport
from common import BUILD_FILE_TEMPLATE_COVERAGE


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_django_coverage(self):
        self.write_build_file(BUILD_FILE_TEMPLATE_COVERAGE.format(apps=['goodapp']))
        shutil.copytree('src/integrationtest/resources/testproject/', self.full_path('src/main/python/testproject/'))
        reactor = self.prepare_reactor()
        try:
            reactor.build()
            raise self.failureException("Build should fail due to project missing, but it's successful")
        except BuildFailedException as e:
            # We know tests are failing
            self.assertIn("Coverage too low", e.message)
            pass
        self.assert_directory_exists('target/reports')
        self.assert_file_exists('target/reports/django_coverage')
        self.assert_file_exists('target/reports/django_coverage.err')
        self.assert_file_contains('target/reports/django_coverage', 'TOTAL')
        self.assert_file_contains('target/reports/django_coverage', 'testapp/views')

if __name__ == "__main__":
    unittest.main()
