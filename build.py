from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.integrationtest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "pybuilder-django-enhanced-plugin"
default_task = ["run_integration_tests", "publish"]


@init
def set_properties(project):
    project.build_depends_on("flake8")
    project.set_property('integrationtest_inherit_environment', True)
    project.set_property('coverage_break_build', False)
