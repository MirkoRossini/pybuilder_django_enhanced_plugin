from pybuilder_django_enhanced_plugin.external_command import EnhancedExternalCommandBuilder

__author__ = 'Mirko Rossini'


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
    django_module_name = project.get_mandatory_property("django_project")
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
    django_module_name = project.get_mandatory_property("django_project")
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
