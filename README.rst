PyBuilder Django Enhanced Plugin 
================================

Plugin for pybuilder providing some useful tasks for django development

How to install pybuilder_django_enhanced_plugin
-----------------------------------------------

Add plugin dependency to your `build.py`::

    use_plugin('pypi:pybuilder_django_enhanced_plugin')


Configure the plugin within your `init` function::

    @init
    def init(project):
        project.set_property('django_project', 'myproject')
        project.set_property('django_apps', ['myapp', 'myotherapp'])
        # you can store your django project and apps in a nested directory under the project src base
        project.set_property('django_subpath', 'nested/dir')
        project.set_property('django_fixtures', ['{{django_base_path}}/goodapp/fixtures/myfixture.json'])
        project.set_property('django_management_commands', [['custom_command', 'myarg']])


Tasks
-----

Installing pybuilder_django_enhanced_plugin exposes the following tasks:

1. "django_test": runs tests for the apps in 'django_apps'. Failures in any of the tests will break the build.
   Can be called as a task, but also hooks itself to the "run_unit_tests" phase of the analyze lifecycle.
2. "django_coverage": runs coverage on the tests of all the apps in 'django_apps'.
   You can set the behaviour of the coverage script by using the coverage plugin settings.
3. "django_management_commands": Runs common commands.
   If any of the command returns a return code != 0 the build will break.
   Commands must be set in the form [[command_name, arg1, arg2], [command_name_1, arg3]]
4. "django_generate": generates the project and apps if not already present
5. "django_run_test_server": Runs a django server
6. "django_run_test_server": Runs a django testserver with the fixtures provided in 'django_fixtures'
7. "django_e2e_tests": starts a test server and runs a list of commands provided in the property
   'django_management_commands'.
   django_management_commands is a list of lists. The first element of the list is the name of the command,
   the rest of the elements represent the actual command (e.g. [['curl_test', 'curl', '127.0.0.1:8000']] )


Quickstart
----------

Start a new project::

    pip install pybuilder
    pyb --startproject

Edit build.py::

    use_plugin("python.core")
    use_plugin("python.unittest")
    use_plugin("python.install_dependencies")
    use_plugin("python.flake8")
    use_plugin("python.distutils")
    use_plugin("pypi:pybuilder_django_enhanced_plugin")

    name = "django_pybuilder_test"
    default_task = "publish"

    @init
    def set_properties(project):
        project.set_property('django_project', 'myproject')
        project.set_property('django_apps', ['myapp', 'myotherapp'])
        project.set_property('django_subpath', 'django_project')

Generate the django project and start using django_enhanced_plugin::

    pyb django_generate
    pyb django_test
    # edit the project's settings.py file and add the apps to the list of installed apps
    pyb django_runserver
    # etc...

To use an existing project, simply copy your project and apps in a subdirectory under the pybuilder project
source (default is src/main/python) and set django_project, django_apps and django_subpath accordingly