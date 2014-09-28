from pybuilder.core import use_plugin, init, Author

use_plugin("python.core")
use_plugin("python.integrationtest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "pybuilder-django-enhanced-plugin"
default_task = ["run_integration_tests", "publish"]

summary = "Plugin for pybuilder providing some useful tasks for django development"
description = """pybuilder-django-enhanced-plugin is a plugin for pybuilder that provides
utilities to develop, build and deploy django projects.
"""

authors = [Author("Mirko Rossini", "mirko.rossini@ymail.com"),
           ]
url = "https://github.com/MirkoRossini/pybuilder_django_enhanced_plugin"
license = "BSD License"
version = "0.0.1"


@init
def set_properties(project):
    project.build_depends_on("flake8")
    project.set_property('integrationtest_inherit_environment', True)
    project.set_property('coverage_break_build', False)
    project.get_property("copy_resources_glob").append("LICENSE")


