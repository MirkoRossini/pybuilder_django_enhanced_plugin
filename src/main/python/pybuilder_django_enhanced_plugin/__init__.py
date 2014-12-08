__author__ = 'Mirko Rossini'

from pybuilder_django_enhanced_plugin.tasks import django_test, django_run_management_commands, django_coverage, \
    django_e2e_tests, verify_django_coverage, run_django_test, django_generate, django_testserver, django_runserver, \
    django_makemigrations, django_migrate, django_syncdb
from pybuilder_django_enhanced_plugin.init import init

__all__ = [django_test, init, django_run_management_commands, django_coverage, django_e2e_tests,
           verify_django_coverage, run_django_test, django_generate, django_testserver, django_runserver,
           django_migrate, django_makemigrations, django_syncdb]
