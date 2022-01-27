import logging
from logging.handlers import RotatingFileHandler
import os
import sys

logger = logging.getLogger()

log_dir_name = os.path.join(os.getcwd(), "Logs")

log_file_name = os.path.join(log_dir_name, "card_game1.log")

if not os.path.exists(log_dir_name):
    os.makedirs(log_dir_name)

piv_log_fmt = logging.Formatter(
    fmt=u'%(asctime)s,%(msecs)d%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt=u'%m/%d/%Y %I:%M:%S %p-')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(piv_log_fmt)

file_stream = RotatingFileHandler(log_file_name, maxBytes=1024, backupCount=3, encoding='utf-8')
file_stream.setLevel(logging.DEBUG)
file_stream.setFormatter(piv_log_fmt)
file_stream.namer = lambda x: log_file_name + x.split('.')[-1] + '.log'

logger.addHandler(file_stream)
logger.addHandler(stdout_handler)
