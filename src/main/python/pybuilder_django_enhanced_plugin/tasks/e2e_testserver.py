from time import sleep
import sys
from pybuilder_django_enhanced_plugin.tasks.common import get_django_path, get_django_command_args, run_project_command

__author__ = 'Mirko Rossini'

from pybuilder.core import task, description, depends
from pybuilder.errors import BuildFailedException
from pybuilder_django_enhanced_plugin.external_command import EnhancedExternalCommandBuilder


def get_testserver_args(project):
    fixtures = project.get_mandatory_property('django_fixtures')
    django_base_path = get_django_path(project)
    fixtures = [fixture.format(django_base_path=django_base_path) for fixture in fixtures]
    args = ['testserver'] + fixtures
    args += get_django_command_args(project)
    return args


@task
@description("Runs the django testserver")
@depends("prepare")
def django_testserver(project, logger):
    args = get_testserver_args(project)
    command = EnhancedExternalCommandBuilder('django-admin', project)
    for arg in args:
        command.use_argument(arg)
    command.run_with_output(logger, sys.stdout)


@task
@description("Runs the django testserver in a background process and executes commands/tasks")
@depends("prepare")
def django_e2e_tests(project, logger):
    args = get_testserver_args(project)
    command_list = project.get_mandatory_property('django_e2e_test_commands')
    command = EnhancedExternalCommandBuilder('django-admin', project)
    for arg in args:
        command.use_argument(arg)
    command.run_in_parallel(logger, 'django_e2e_tests_server')

    while 1:
        logger.info("Waiting for Django testserver startup")
        sleep(1)
        if command.process.poll() is not None:
            logger.warn("Django testserver stopped unexpectedly.")
            with open(command.report_file.name) as report_file:
                serverlog = report_file.read()
            with open(command.error_report_file.name) as error_report_file:
                serverlog += error_report_file.read()
            logger.warn(serverlog)
            raise BuildFailedException("Django e2e tests failed")
        with open(command.report_file.name) as report_file:
            serverlog = report_file.read()
        if 'Quit the server' in serverlog:
            logger.info("Django testserver up and running")
            break
    for args in command_list:
        if len(args) == 0:
            raise BuildFailedException("Commands in django_e2e_test_commands must have at least 2 args "
                                       "(the first being the name of the command)")
        command_name = "django_e2e_test_command_" + args[0]
        command_result = run_project_command(project, logger, command_name, args[2:], args[1])
        if command_result.exit_code != 0:
            error_message = ''.join(command_result.error_report_lines)
            logger.error("Django management {} command failed: {}".format(command_name, error_message))
            command_result = command.stop_run()
            raise BuildFailedException("Django commands failed: {}".format(command_result))
    logger.info("Stopping Django testserver")
    command_result = command.stop_run()
    print(command_result.error_report_file)

    if command_result.exit_code != 0:
        error_message = ''.join(command_result.error_report_lines)
        logger.error("Django e2e tests failed: {}".format(error_message))
        raise BuildFailedException("Django e2e tests failed failed")
    return command_result
