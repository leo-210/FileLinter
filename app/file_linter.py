
import argparse
import os
import sys

from loguru import logger
from yaml import safe_load as load

from init import init


# Initialize the argument parser
parser = argparse.ArgumentParser(description="File linter")
parser.add_argument("init", help="creates a config file", action="store_true")
parser.add_argument("-c", "--config", help="the config file path", required=False, default="file-linter.yml")
parser.add_argument("--debug", help="enable debug mode", required=False, action="store_true")
args = parser.parse_args()

# Add format to logger
logger.remove()
if args.debug:
    logger.add(sys.stdout, format="[{time}] <level>{level}:</level> {message}", level="DEBUG")
else:
    logger.add(sys.stdout, colorize=True, format="<level>{level}:</level> {message}", level="INFO")

if args.init:
    init(os.path.realpath(__file__), logger)
    sys.exit(0)

config_file_path = args.config

# Check if the config file exists
if not os.path.isfile(config_file_path):
    logger.error("The config file does not exist. Make sure you have a file-linter.yml file in the working directory.")
    sys.exit(1)

# Check if whe can access the config file
if not os.access(config_file_path, os.R_OK):
    logger.error("The config file is not readable. Check the permissions of the file.")
    sys.exit(1)

# Parse the config file
with open(config_file_path, "r") as config_file:
    config = load(config_file.read())


