import os
from pybuilder.core import task, description, depends
from pybuilder_django_enhanced_plugin.tasks.common import get_django_path, run_project_command

__author__ = 'Mirko Rossini'


def run_django_generate_command(project, logger, command_name, args):
    """
    Runs a django-admin command to start a project
    """
    django_module_name = project.get_mandatory_property("django_project")
    logger.info("Running Django command for %s", django_module_name)
    result = run_project_command(project, logger, command_name, args, 'django-admin')
    return result


def generate_project(project, logger, django_project, base_path):
    if os.path.exists(base_path + '/' + django_project):
        logger.info("Django project {} already exists in directory {}, skip".format(django_project, base_path))
    else:
        args = ['startproject', django_project, base_path]
        logger.info("Generating django project {}".format(django_project))
        run_django_generate_command(project, logger, "startproject", args)


def generate_app(project, logger, app, base_path):
    if os.path.exists(base_path + '/' + app):
        logger.info("Django app {} already exists in directory {}, skip".format(app, base_path))
    else:
        args = ['startapp', app]
        logger.info("Generating django app {}".format(app))
        run_django_generate_command(project, logger, "startapp", args)


@task
@description("Starts the django project and applications")
@depends("prepare")
def django_generate(project, logger):
    django_apps = project.get_property("django_apps", [])
    django_project = project.get_mandatory_property("django_project")
    base_path = get_django_path(project)
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    generate_project(project, logger, django_project, base_path)
    cwd = os.getcwd()
    os.chdir(base_path)
    for app in django_apps:
        generate_app(project, logger, app, base_path)
    os.chdir(cwd)
