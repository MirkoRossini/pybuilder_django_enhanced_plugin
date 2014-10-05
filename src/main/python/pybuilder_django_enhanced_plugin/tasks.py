from time import sleep
from pybuilder.utils import execute_command

__author__ = 'Mirko Rossini'

from pybuilder.core import task, description, depends
from pybuilder.errors import BuildFailedException
from pybuilder_django_enhanced_plugin.external_command import EnhancedExternalCommandBuilder


def get_test_command(project):
    """
    Returns the args to be passed to django-admin to run tests on all the apps
    :param project:
    :return:
    """
    django_apps = project.get_mandatory_property("django_apps")
    args = ['test', ] + django_apps
    return args


def get_django_path(project):
    """
    Gets the django base path for the project
    i.e. the directory containing the project and the manage.py script
    :param project:
    :return:
    """
    django_subpath = project.get_property("django_subpath", "")
    base_path = project.expand_path("$dir_source_main_python")
    base_path = base_path + '/' + django_subpath
    return base_path


def get_django_command_args(project):
    """
    Given a project, returns the args to set up django-admin correctly
    i.e. settings module and pythonpath
    :param project:
    :return:
    """
    django_module_name = project.get_mandatory_property("django_module")
    args = []
    settings_module_name = "{0}.settings".format(django_module_name)
    base_path = get_django_path(project)
    args.append('--pythonpath={}'.format(base_path))
    args.append('--settings={}'.format(settings_module_name))
    return args


def run_django_manage_command(project, logger, command_name, args):
    """
    Runs a django-manage command
    :param project: pybuilder project
    :param logger: pybuilder logger
    :param command_name: Name of the commands (used to generate report files)
    :param args: The args to be passed to django-admin
    :type args: list
    :return:
    """
    django_module_name = project.get_mandatory_property("django_module")
    logger.info("Running Django command for %s", django_module_name)
    args += get_django_command_args(project)
    result = run_project_command(project, logger, command_name, args, 'django-admin')
    return result


def run_project_command(project, logger, command_name, args, command):
    """
    Runs an external command for the current project
    :param project: pybuilder project
    :param logger: pybuilder logger
    :param command_name: The name of the command (will be used to create report files)
    :param args: command args
    :param command: The command to run
    :return:
    """
    command = EnhancedExternalCommandBuilder(command, project)
    for arg in args:
        command.use_argument(arg)
    result = command.run(logger, command_name)
    return result


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


@task
@description("Runs the django testserver in a background process and executes commands/tasks")
@depends("prepare")
def django_e2e_tests(project, logger):
    fixtures = project.get_mandatory_property('django_fixtures')
    django_base_path = get_django_path(project)
    fixtures = [fixture.format(django_base_path=django_base_path) for fixture in fixtures]
    command_list = project.get_mandatory_property('django_e2e_test_commands')
    args = ['testserver'] + fixtures
    args += get_django_command_args(project)
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
            raise BuildFailedException("Commands in django_e2e_test_commands must have at least 2 args")
        command_name = "django_e2e_test_command_" + args[0]
        #command_result = run_django_manage_command(project, logger, command_name, args)
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


@task
@description("Calculates coverage for the django project")
@depends("prepare")
def django_coverage(project, logger):
    args = get_test_command(project)
    args += get_django_command_args(project)
    django_path = get_django_path(project)
    coverage_args = ['run', '--source', django_path, django_path + '/manage.py']
    args = coverage_args + args
    logger.info("Running Django coverage")
    command_result = run_project_command(project, logger, 'django_coverage', args, 'coverage')
    if command_result.exit_code != 0:
        error_message = ''.join(command_result.error_report_lines)
        logger.error("Django coverage run failed: {}".format(error_message))
        raise BuildFailedException("Django coverage failed")
    args = ['report', '-m']
    logger.info("Running coverage report")
    command_result = run_project_command(project, logger, 'django_coverage', args, 'coverage')
    if command_result.exit_code != 0:
        error_message = ''.join(command_result.error_report_lines)
        logger.error("Django coverage report run failed: {}".format(error_message))
        raise BuildFailedException("Django coverage report failed")
    threshold = project.get_property("coverage_threshold_warn", 70)
    exceptions = project.get_property("coverage_exceptions", [])
    coverage_too_low = False
    for line in command_result.report_lines[1:]:
        res = line.split()
        missing = ""
        if len(res) == 5:
            module_name, statements, miss, cover, missing = res
        elif len(res) == 4:
            module_name, statements, miss, cover = res
        else:
            continue
        cover_percentage = int(cover.replace('%', ''))
        module_name = module_name.replace(django_path, '')
        module_name = module_name.replace('/private/', '')
        module_name = module_name.replace('/', '.')

        should_ignore_module = module_name in exceptions
        if cover_percentage < threshold:
            msg = "Test coverage below {}% for {}: {}%".format(threshold, module_name, cover_percentage)
            if not should_ignore_module:
                logger.warn(msg)
                coverage_too_low = True
            else:
                logger.info(msg)
    if coverage_too_low and project.get_property("coverage_break_build", False):
        raise BuildFailedException("Coverage too low in django project")
    return 0
