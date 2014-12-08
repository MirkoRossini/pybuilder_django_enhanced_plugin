__author__ = 'Mirko Rossini'

from pybuilder_django_enhanced_plugin.tasks.management_commands import django_run_management_commands
from pybuilder_django_enhanced_plugin.tasks.e2e_testserver import django_e2e_tests, django_testserver
from pybuilder_django_enhanced_plugin.tasks.django_coverage import verify_django_coverage, django_coverage
from pybuilder_django_enhanced_plugin.tasks.django_test import run_django_test, django_test
from pybuilder_django_enhanced_plugin.tasks.django_generate import django_generate
from pybuilder_django_enhanced_plugin.tasks.runserver import django_runserver
from pybuilder_django_enhanced_plugin.tasks.django_migrations import django_migrate, django_makemigrations
from pybuilder_django_enhanced_plugin.tasks.django_syncdb import django_syncdb


__all__ = [django_run_management_commands, django_e2e_tests, django_testserver, verify_django_coverage, django_coverage,
           run_django_test, django_test, django_generate, django_runserver, django_migrate, django_makemigrations,
           django_syncdb]
