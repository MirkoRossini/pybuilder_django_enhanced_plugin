__author__ = 'Mirko Rossini'

import unittest
import shutil
from integrationtest_support import IntegrationTestSupport
from common import BUILD_FILE_TEMPLATE_MIGRATION


class DjangoEnhancedPluginTest(IntegrationTestSupport):
    def test_django_coverage(self):
        self.write_build_file(BUILD_FILE_TEMPLATE_MIGRATION.format(apps=['goodapp']))
        shutil.copytree('src/integrationtest/resources/testproject/', self.full_path('src/main/python/testproject/'))
        reactor = self.prepare_reactor()
        reactor.build()
        self.assert_directory_exists('target/reports')
        self.assert_file_exists('target/reports/django_makemigrations')
        self.assert_file_exists('target/reports/django_makemigrations.err')
        self.assert_file_exists('target/reports/django_migrate')
        self.assert_file_exists('target/reports/django_migrate.err')
        self.assert_file_not_empty('target/reports/django_migrate')
        self.assert_file_not_empty('target/reports/django_makemigrations')


if __name__ == "__main__":
    unittest.main()
