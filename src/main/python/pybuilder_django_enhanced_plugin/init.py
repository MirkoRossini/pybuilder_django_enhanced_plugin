__author__ = 'Mirko Rossini'
from pybuilder.core import init


@init
def set_properties(project):
    project.build_depends_on("django")
