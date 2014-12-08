from pybuilder.core import task, description, depends, use_plugin
from pybuilder_django_enhanced_plugin.tasks.common import get_django_command_args

__author__ = 'Mirko Rossini'

use_plugin("python.core")


def run_django_syncdb(project, logger):
    django_syncdb(project, logger)


@task
@description("Runs django syncdb")
@depends("prepare")
def django_syncdb(project, logger):
    args = ['syncdb']
    args += get_django_command_args(project)
    from django.core.management import execute_from_command_line
    logger.info("Running django syncdb {} ".format(args))
    execute_from_command_line([''] + args)
