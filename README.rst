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


Tasks
-----

Installing pybuilder_django_enhanced_plugin exposes the following tasks:

1. "django_test": runs tests for the apps in 'django_apps'. Failures in any of the tests will break the build.
