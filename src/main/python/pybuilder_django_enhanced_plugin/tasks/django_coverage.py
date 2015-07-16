import re
from pybuilder import BuildFailedException
from pybuilder.core import after, task, description, depends, use_plugin
from pybuilder_django_enhanced_plugin.tasks.common import get_test_command, get_django_command_args, get_django_path, \
    run_project_command

__author__ = 'Mirko Rossini'

use_plugin("python.core")
use_plugin("analysis")

REMOVE_INITIAL_DOT_REGEX = re.compile(r'^\.')


@after(("analyze", "verify"), only_once=True)
def verify_django_coverage(project, logger):
    django_coverage(project, logger)


def path_to_module(path, project):
    django_path = get_django_path(project)
    module_name = path.replace(django_path, '')
    module_name = module_name.replace('/', '.')
    module_name = module_name.replace('.private', '')
    module_name = REMOVE_INITIAL_DOT_REGEX.sub('', module_name)
    return module_name


def run_coverage(logger, project):
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


def run_report(logger, project):
    args = ['report', '-m']
    logger.info("Running coverage report")
    command_result = run_project_command(project, logger, 'django_coverage', args, 'coverage')
    if command_result.exit_code != 0:
        error_message = ''.join(command_result.error_report_lines)
        logger.error("Django coverage report run failed: {}".format(error_message))
        raise BuildFailedException("Django coverage report failed")
    return command_result


class CoverageReport(object):
    def __init__(self, module_name, statements, miss, cover, missing=""):
        self.module_name = module_name
        self.statements = statements
        self.miss = miss
        self.cover = cover
        self.missing = missing

    @staticmethod
    def from_coverage_report_line(line):
        split_line = line.split()
        if len(split_line) < 4:
            return None
        coverage_report = CoverageReport(*split_line)
        if coverage_report.module_name == 'TOTAL':
            return None
        return coverage_report


@task
@description("Calculates coverage for the django project")
@depends("prepare")
def django_coverage(project, logger):
    run_coverage(logger, project)
    command_result = run_report(logger, project)
    threshold = project.get_property("coverage_threshold_warn", 70)
    exceptions = project.get_property("coverage_exceptions", [])
    coverage_too_low = False
    percentages = []
    for line in command_result.report_lines[1:]:

        coverage_report = CoverageReport.from_coverage_report_line(line)
        if coverage_report is None:
            continue
        cover_percentage = int(coverage_report.cover.replace('%', ''))
        percentages.append(cover_percentage)
        module_name = path_to_module(coverage_report.module_name, project)

        should_ignore_module = module_name in exceptions

        if cover_percentage < threshold:
            msg = "Test coverage below {}% for {}: {}%".format(threshold, module_name, cover_percentage)
            if not should_ignore_module:
                logger.warn(msg)
                coverage_too_low = True
            else:
                logger.info(msg)
    total_coverage = float(sum(percentages))/len(percentages) if len(percentages) > 0 else float('nan')
    if total_coverage < threshold:
        msg = "Total Test coverage below {}%: {}%".format(threshold, total_coverage)

        logger.warn(msg)
        coverage_too_low = True

    if coverage_too_low and project.get_property("coverage_break_build", False):
        raise BuildFailedException("Coverage too low in django project")
    return 0
