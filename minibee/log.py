import logging
import logging.config
import yaml
import configparser
import os
import colorama
from pathlib import Path
colorama.init()

logConfigPath = Path('./log_config.yml')

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[m"
COLOR_SEQ = "\033[%d;%dm"
NORMAL = 0
BOLD = 1

COLORS = {
    "WARNING": (YELLOW, NORMAL),
    "INFO": (GREEN, NORMAL),
    "DEBUG": (CYAN, NORMAL),
    "CRITICAL": (RED, BOLD),
    "ERROR": (RED, NORMAL),
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, style, useColor=True):
        super(ColoredFormatter, self).__init__(msg, style=style)
        self.useColor = useColor

    def format(self, record):
        levelname = record.levelname
        if self.useColor and levelname in COLORS:
            levelnameColor = COLOR_SEQ % (COLORS[levelname][1], 30 + COLORS[levelname][0]) + levelname + RESET_SEQ
            record.levelname = levelnameColor
        return logging.Formatter.format(self, record)




def get_logger_and_formatter(logConfig, formatterName):
    targetList = []
    for logr in logConfig['loggers']:
        for handlr in logConfig['loggers'][logr]['handlers']:
            if logConfig['handlers'][handlr]['formatter'] == formatterName:
                targetList.append((logr, handlr))
    return targetList


def replace_formatter(targetList, newFormatter):
    for i in range(len(targetList)):
        logr, handlr = targetList[i]
        logr_ = logging.getLogger(logr)
        for handlr_ in logr_.handlers:
            if handlr_.name == handlr:
                handlr_.setFormatter(newFormatter)

def create_log_directories(logConfig):
    for handler in logConfig['handlers'].values():
        try:
            path = handler['filename']
            os.makedirs(os.path.dirname(path), exist_ok=True)
        except KeyError:
            continue

with open(logConfigPath, 'r') as ifile:
    logConfig = yaml.safe_load(ifile)


create_log_directories(logConfig)
logging.config.dictConfig(logConfig)

# ----------Colored formatter
targetList = get_logger_and_formatter(logConfig, 'colored')  # get formatters marked as 'colored'
newFormatter = ColoredFormatter(logConfig['formatters']['colored']['format'], logConfig['formatters']['colored']['style'], useColor=True)  # create formatter with colored output
replace_formatter(targetList, newFormatter)  # replace formatters marked as 'colored' by their colored version
# ---------------------------

logger = logging.getLogger('mainLogger')