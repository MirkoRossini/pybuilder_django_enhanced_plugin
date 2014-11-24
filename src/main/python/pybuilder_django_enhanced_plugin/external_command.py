import os
from pybuilder.pluginhelper.external_command import ExternalCommandBuilder, ExternalCommandResult
from pybuilder.utils import read_file
from pybuilder.plugins.python.python_plugin_helper import as_list, execute_command, log_report
import subprocess
import signal


def spawn_process(command_and_arguments, out_file, error_file, env=None, cwd=None,
                                  shell=False):
    return subprocess.Popen(
        command_and_arguments,
        stdout=out_file,
        stderr=error_file,
        env=env,
        cwd=cwd,
        shell=shell,
        preexec_fn=os.setpgrp  # we set the process group in the child process
    )


def execute_command_in_background(command_and_arguments, out_file, error_file, env=None, cwd=None,
                                  shell=False):
    if env is None:
        env = os.environ
    # We set the variable PYTHONUNBUFFERED to autoflush the output in django runserver/testserver
    env = dict(env, **{'PYTHONUNBUFFERED': '1'})
    process = spawn_process(command_and_arguments, out_file, error_file, env, cwd, shell)
    return process


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
    def __init__(self, *args, **kwargs):
        super(EnhancedExternalCommandBuilder, self).__init__(*args, **kwargs)
        self.process = None
        self.report_file = None
        self.error_report_file = None

    def run(self, logger, report_name):
        execution_result = execute_tool(
            project=self.project,
            name=self.command_name,
            report_name=report_name,
            command_and_arguments=self.parts,
            logger=logger,
        )
        exit_code, report_file = execution_result
        report_lines = read_file(report_file)
        error_report_file = '{0}.err'.format(report_file)
        error_report_lines = read_file(error_report_file)
        return ExternalCommandResult(exit_code, report_file, report_lines, error_report_file, error_report_lines)

    def run_in_parallel(self, logger, report_name):
        command = as_list(self.parts)
        self.report_file = open(self.project.expand_path("$dir_reports/{0}".format(report_name)), 'w')
        self.error_report_file = open('{0}.err'.format(self.report_file.name), 'w')
        logger.info("Running command in background: {}".format(command))
        self.process = execute_command_in_background(
            command_and_arguments=command,
            out_file=self.report_file,
            error_file=self.error_report_file
        )

    def run_with_output(self, logger, output_file):
        command = as_list(self.parts)
        logger.info("Running command writing to stout: {}".format(command))
        self.process = execute_command_in_background(
            command_and_arguments=command,
            out_file=output_file,
            error_file=output_file
        )
        self.process.wait()

    def get_report(self):
        if self.report_file is not None:
            self.report_file.flush()
            self.report_file.close()
            report_lines = read_file(self.report_file.name)
            report_file_name=self.report_file.name
            return report_file_name, report_lines
        return "", ""

    def get_error_report(self):
        if self.error_report_file is not None:
            self.error_report_file.flush()
            self.error_report_file.close()
            error_report_lines = read_file(self.error_report_file.name)
            error_report_file_name = self.error_report_file.name
            return error_report_file_name, error_report_lines
        return "", ""

    def stop_run(self):
        if self.process is None:
            raise ReferenceError("process is not set, make sure you ran a parallel process")
        os.killpg(self.process.pid, signal.SIGINT)
        exit_code = self.process.wait()
        report_file_name, report_lines = self.get_report()
        error_report_file_name, error_report_lines = self.get_error_report()
        self.process = None
        return ExternalCommandResult(exit_code, report_file_name, report_lines, error_report_file_name,
                                     error_report_lines)
