__author__ = 'Mirko Rossini'

from pybuilder.core import task, description, depends
from pybuilder.errors import BuildFailedException
from pybuilder_django_enhanced_plugin.external_command import EnhancedExternalCommandBuilder


def run_django_manage_command(project, logger, command_name, args):
    django_module_name = project.get_mandatory_property("django_module")

    django_subpath = project.get_property("django_subpath", "")

    logger.info("Running Django command for %s", django_module_name)
    settings_module_name = "{0}.settings".format(django_module_name)
    base_path = project.expand_path("$dir_source_main_python")
    base_path = base_path + '/' + django_subpath
    args.append('--pythonpath={}'.format(base_path))
    args.append('--settings={}'.format(settings_module_name))
    command = EnhancedExternalCommandBuilder('django-admin', project)
    for arg in args:
        command.use_argument(arg)
    result = command.run(logger, command_name)
    return result


@task
@description("Uses django test ")
@depends("prepare")
def django_test(project, logger):
    django_apps = project.get_mandatory_property("django_apps")
    args = ['test', ] + django_apps
    command_result = run_django_manage_command(project, logger, 'django_tests', args)
    if command_result.exit_code != 0:
        error_message = ''.join(command_result.error_report_lines)
        logger.error("Django tests failed: {}".format(error_message))
        raise BuildFailedException("Django tests failed")
    return command_result


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
