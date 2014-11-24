from pybuilder import BuildFailedException
from pybuilder.core import task, description, depends
from pybuilder_django_enhanced_plugin.tasks.common import run_django_manage_command

__author__ = 'Mirko Rossini'


@task
@description("Runs custom django management commands")
@depends("prepare")
def django_run_management_commands(project, logger):
    command_list = project.get_mandatory_property("django_management_commands")
    for args in command_list:
        if len(args) == 0:
            raise BuildFailedException("Commands in django_management_commands must have at least 1 arg")
        command_name = "django_management_command_" + args[0]
        command_result = run_django_manage_command(project, logger, command_name, args)
        if command_result.exit_code != 0:
            error_message = ''.join(command_result.error_report_lines)
            logger.error("Django management {} command failed: {}".format(command_name, error_message))
            raise BuildFailedException("Django commands failed")
    return 0
