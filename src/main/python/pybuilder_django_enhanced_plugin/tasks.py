__author__ = 'Mirko Rossini'
import sys

from pybuilder.core import task, description, depends
from pybuilder.errors import PyBuilderException
from pybuilder.errors import BuildFailedException
from pybuilder_django_enhanced_plugin.external_command import EnhancedExternalCommandBuilder

@task
@description("Uses django test ")
@depends("prepare")
def django_test(project, logger):
    django_module_name = project.get_mandatory_property("django_module")
    django_apps = project.get_mandatory_property("django_apps")
    django_subpath = project.get_property("django_subpath", "")

    logger.info("Running Django tests for %s", django_module_name)

    settings_module_name = "{0}.settings".format(django_module_name)
    base_path = project.expand_path("$dir_source_main_python")
    base_path = base_path + '/' + django_subpath
    command = EnhancedExternalCommandBuilder('django-admin', project)
    command.use_argument('test')
    for app in django_apps:
        command.use_argument(app)

    command.use_argument('--pythonpath={}'.format(base_path))
    command.use_argument('--settings={}'.format(settings_module_name))
    result = command.run(logger, 'django_tests')
    if result.exit_code != 0:
        error_message = ''.join(result.error_report_lines)
        raise BuildFailedException(error_message)

    return result
