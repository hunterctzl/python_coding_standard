import json
import logging
import os
import sys
import time
import traceback
from functools import wraps

import pandas as pd

# if in GCP dataproc env, enable GCP logging component
if os.getenv("DATAPROC_IMAGE_TYPE"):
    import google.cloud.logging

    client = google.cloud.logging.Client()
    client.setup_logging()

cur_path = os.path.dirname(os.path.abspath(__file__))
log_folder_index = cur_path.rfind("/", 0, cur_path.rfind("/"))
log_path = cur_path[:log_folder_index] + "/log/pyspark_info.log"

log_format = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
log_handler = logging.FileHandler(log_path)
log_handler.setFormatter(log_format)

out_logger = logging.getLogger("STDOUT")
out_logger.setLevel(logging.INFO)
out_logger.addHandler(log_handler)

err_logger = logging.getLogger("STDERR")
err_logger.setLevel(logging.ERROR)
err_logger.addHandler(log_handler)


def logger(func):
    # This is the decoration function used to create log for recommendation models
    @wraps(func)
    def log_wrapper(self, *args, **kwargs):
        old_stdout = sys.stdout
        stdout_logger = OutputLogger(out_logger, logging.INFO)
        sys.stdout = stdout_logger

        old_stderr = sys.stderr
        stderr_logger = OutputLogger(err_logger, logging.ERROR)
        sys.stderr = stderr_logger

        verbosity_level = 1
        if (
            getattr(self, "verbosity_level", None)
            and str(self.verbosity_level) != "undefined__verbosity_level"
        ):
            verbosity_level = self.getOrDefault(param=self.verbosity_level)

        if verbosity_level == 1:
            print(f"{func.__qualname__} starts running")
            start_time = time.time()
            for param_name, param_value in kwargs.items():
                if isinstance(param_value, pd.DataFrame):
                    print(
                        f"{func.__qualname__} input {param_name} shape: "
                        f"{param_value.shape}"
                    )

        result = func(self, *args, **kwargs)

        if verbosity_level == 1:
            func_duration = time.time() - start_time
            print(f"{func.__qualname__} lasts for {func_duration} seconds")
            print(f"{func.__qualname__} ends running")

        sys.stdout = old_stdout
        sys.stderr = old_stderr
        return result

    return log_wrapper


class OutputLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, msg):
        if msg and not msg.isspace():
            self.logger.log(self.log_level, msg)

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()


def log_exception(
    message: str,
    log_path: str,
):
    """

    This is a helper function to log the exceptions

    Parameters
    ----------
    message: str
        message to describe certain exception
    log_path:
        the path to save the log file

    Returns
    -------

    """
    assert isinstance(message, str), "message must be str"
    assert isinstance(log_path, str), "log_path must be str"
    ex_type, ex_value, ex_traceback = sys.exc_info()
    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)
    # Format stacktrace
    stack_trace = "File : %s , Line : %d, Func.Name : %s, Message : %s" % (
        trace_back[-1][0],
        trace_back[-1][1],
        trace_back[-1][2],
        trace_back[-1][3],
    )
    exception_log = {}
    exception_log["message"] = message
    exception_log["exception_type"] = ex_type.__name__
    exception_log["exception_message"] = str(ex_value)
    exception_log["stack_trace"] = stack_trace
    with open(log_path, "a") as outfile:
        json.dump(exception_log, outfile)
        outfile.write("\n")
