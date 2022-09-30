""" Define envvars for the execution of the app """
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
