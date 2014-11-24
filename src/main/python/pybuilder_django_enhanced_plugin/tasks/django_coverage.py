from pybuilder import BuildFailedException
from pybuilder.core import after, task, description, depends, use_plugin
from pybuilder_django_enhanced_plugin.tasks.common import get_test_command, get_django_command_args, get_django_path, \
    run_project_command

__author__ = 'Mirko Rossini'

use_plugin("python.core")
use_plugin("analysis")


@after(("analyze", "verify"), only_once=True)
def verify_django_coverage(project, logger):
    django_coverage(project, logger)


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

