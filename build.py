from pybuilder.core import use_plugin, init, Author

use_plugin("python.core")
use_plugin("python.integrationtest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("copy_resources")
use_plugin("python.distutils")


name = "pybuilder-django-enhanced-plugin"
default_task = ["analyze", "run_integration_tests", "publish"]

summary = "Plugin for pybuilder providing some useful tasks for django development"
description = """pybuilder-django-enhanced-plugin is a plugin for pybuilder that provides
utilities to develop, build and deploy django projects.
"""

authors = [Author("Mirko Rossini", "mirko.rossini@ymail.com"),
           ]
url = "https://github.com/MirkoRossini/pybuilder_django_enhanced_plugin"
license = "BSD License"
version = "0.0.9"


@init
def set_properties(project):
    project.build_depends_on("flake8")
    project.depends_on("django")
    project.build_depends_on("coverage")
    project.set_property('integrationtest_inherit_environment', True)
    project.set_property('flake8_break_build', True)
    project.set_property("copy_resources_target", "$dir_dist")
    project.get_property("copy_resources_glob").append("LICENSE")
    project.get_property("copy_resources_glob").append("MANIFEST.in")
    project.get_property("copy_resources_glob").append("README.rst")
    # project.get_property("distutils_commands").append("bdist_wheel")
    # project.set_property("distutils_console_scripts", ["pyb_ = pybuilder.cli:main"])
    project.set_property("distutils_classifiers", [
                         'Programming Language :: Python',
                         'Programming Language :: Python :: Implementation :: CPython',
                         'Programming Language :: Python :: Implementation :: PyPy',
                         'Programming Language :: Python :: 2.6',
                         'Programming Language :: Python :: 2.7',
                         'Programming Language :: Python :: 3',
                         'Programming Language :: Python :: 3.2',
                         'Programming Language :: Python :: 3.3',
                         'Programming Language :: Python :: 3.4',
                         'Development Status :: 4 - Beta',
                         'Environment :: Console',
                         'Intended Audience :: Developers',
                         'License :: OSI Approved :: BSD License',
                         'Topic :: Software Development :: Build Tools',
                         'Topic :: Software Development :: Quality Assurance',
                         'Topic :: Software Development :: Testing'])


