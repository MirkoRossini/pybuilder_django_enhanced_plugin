from pybuilder import BuildFailedException
from pybuilder.core import task, description, depends, use_plugin
from pybuilder_django_enhanced_plugin.tasks.common import run_django_manage_command

__author__ = 'Mirko Rossini'

use_plugin("python.core")


def run_django_makemigrations(project, logger):
    django_makemigrations(project, logger)


def run_django_migrate(project, logger):
    django_migrate(project, logger)


@task
@description("Runs django makemigrations")
@depends("prepare")
def django_makemigrations(project, logger):
    args = ['makemigrations']
    command_result = run_django_manage_command(project, logger, 'django_makemigrations', args)
    if command_result.exit_code != 0:
        error_message = ''.join(command_result.error_report_lines)
        logger.error("Django makemigrations failed: {}".format(error_message))
        raise BuildFailedException("Django makemigrations failed")
    return command_result


@task
@description("Runs django migrate")
@depends("prepare")
def django_migrate(project, logger):
    args = ['makemigrations']
    command_result = run_django_manage_command(project, logger, 'django_migrate', args)
    if command_result.exit_code != 0:
        error_message = ''.join(command_result.error_report_lines)
        logger.error("Django migrate failed: {}".format(error_message))
        raise BuildFailedException("Django migrate failed")
    return command_result
