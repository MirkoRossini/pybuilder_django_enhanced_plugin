import sys
from pybuilder_django_enhanced_plugin.tasks.common import get_django_command_args

__author__ = 'Mirko Rossini'

from pybuilder.core import task, description, depends
from pybuilder_django_enhanced_plugin.external_command import EnhancedExternalCommandBuilder


@task
@description("Runs the django testserver")
@depends("prepare")
def django_runserver(project, logger):
    args = ['runserver']
    args += get_django_command_args(project)
    command = EnhancedExternalCommandBuilder('django-admin', project)
    for arg in args:
        command.use_argument(arg)
    try:
        command.run_with_output(logger, sys.stdout)
    except KeyboardInterrupt:
        logger.info("Stopping django server")
    command.stop_run()
