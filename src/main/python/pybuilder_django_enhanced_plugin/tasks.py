__author__ = 'Mirko Rossini'

from pybuilder.core import task, description, depends
from pybuilder.errors import BuildFailedException
from pybuilder_django_enhanced_plugin.external_command import EnhancedExternalCommandBuilder


def get_test_command(project):
    django_apps = project.get_mandatory_property("django_apps")
    args = ['test', ] + django_apps
    return args


def get_django_path(project):
    django_subpath = project.get_property("django_subpath", "")
    base_path = project.expand_path("$dir_source_main_python")
    base_path = base_path + '/' + django_subpath
    return base_path


def get_django_command_args(project):
    django_module_name = project.get_mandatory_property("django_module")
    args = []
    settings_module_name = "{0}.settings".format(django_module_name)
    base_path = get_django_path(project)
    args.append('--pythonpath={}'.format(base_path))
    args.append('--settings={}'.format(settings_module_name))
    return args


def run_django_manage_command(project, logger, command_name, args):
    django_module_name = project.get_mandatory_property("django_module")
    logger.info("Running Django command for %s", django_module_name)
    args += get_django_command_args(project)
    result = run_project_command(project, logger, command_name, args, 'django-admin')
    return result


def run_project_command(project, logger, command_name, args, command):
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
