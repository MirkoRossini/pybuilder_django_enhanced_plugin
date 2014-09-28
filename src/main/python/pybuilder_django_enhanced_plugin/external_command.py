import os
from pybuilder.pluginhelper.external_command import ExternalCommandBuilder, ExternalCommandResult
from pybuilder.utils import read_file
from pybuilder.plugins.python.python_plugin_helper import as_list, execute_command, log_report


def execute_tool(project, name, report_name, command_and_arguments, logger=None):
    command = as_list(command_and_arguments)
    report_file = project.expand_path("$dir_reports/{0}".format(report_name))
    logger.info("Running command: {}".format(command))

    execution_result = execute_command(command, report_file), report_file
    report_file = execution_result[1]
    report_lines = read_file(report_file)
    if project.get_property(name + "_verbose_output") and logger:
        log_report(logger, name, report_lines)
    return execution_result


class EnhancedExternalCommandBuilder(ExternalCommandBuilder):
    def run(self, logger, report_name):
        execution_result = execute_tool(project=self.project,
                                        name=self.command_name,
                                        report_name=report_name,
                                        command_and_arguments=self.parts,
                                        logger=logger,
                                        )
        exit_code, report_file = execution_result
        report_lines = read_file(report_file)
        error_report_file = '{0}.err'.format(report_file)  # TODO @mriehl not dry, execute_tool... should return this
        error_report_lines = read_file(error_report_file)
        return ExternalCommandResult(exit_code, report_file, report_lines, error_report_file, error_report_lines)
