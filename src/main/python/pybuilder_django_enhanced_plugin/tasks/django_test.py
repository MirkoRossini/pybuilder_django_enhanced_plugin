from pybuilder import BuildFailedException
from pybuilder.core import task, description, depends, after, use_plugin
from pybuilder_django_enhanced_plugin.tasks.common import get_test_command, run_django_manage_command

__author__ = 'Mirko Rossini'

use_plugin("python.core")
use_plugin("python.unittest")

@after(("run_unit_tests",), only_once=True)
def run_django_test(project, logger):
    django_test(project, logger)

@task
@description("Uses django test ")
@depends("prepare")
def django_test(project, logger):
    args = get_test_command(project)
    command_result = run_django_manage_command(project, logger, 'django_tests', args)
    if command_result.exit_code != 0:
        error_message = ''.join(command_result.error_report_lines)
        logger.error("Django tests failed: {}".format(error_message))
        raise BuildFailedException("Django tests failed")
    return command_result
