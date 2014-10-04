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
        project.set_property('django_module', 'myproject')
        project.set_property('django_apps', ['myapp', 'myotherapp'])
        project.set_property('django_subpath', 'nested/dir')
        project.set_property('django_management_commands', [['custom_command', 'myarg']])


Tasks
-----

Installing pybuilder_django_enhanced_plugin exposes the following tasks:

1. "django_test": runs tests for the apps in 'django_apps'. Failures in any of the tests will break the build.
2. "django_coverage": runs coverage on the tests of all the apps in 'django_apps'.
   You can set the behaviour of the coverage script by using the coverage plugin settings.
3. "django_management_commands": Runs common commands. If any of the command returns a return code != 0 the build will break.
   Commands must be set in the form [[command_name, arg1, arg2], [command_name_1, arg3]]

