#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__     = 'Akihiro Miyata'
__copyright__  = 'Copyright (c) 2014 NTT Corp. All rights reserved.'
__maintainer__ = 'Akihiro Miyata'
__email__      = 'miyata.akihiro@lab.ntt.co.jp'

from api import WebSocketApi
from sensor.sensor import SensorData
from sensor.sensorreader import SensorReader

import ConfigParser as cp
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import logging, logging.config
from threading import Thread

SERVER_CONF = 'conf/server.conf'
LOG_CONF    = 'conf/log.conf'

class Env():
    def __init__(self, bufSize):
        self.snsData = SensorData(bufSize)
        self.wsLastFetchTimes = {}

def srProc(snsReaderParams):
    '''
    Starts the sensor reader process.
    '''
    server = SensorReader(*snsReaderParams)
    server.start()

def wsProc(env, wsHost, wsPort, pushInterval, dataLabel):
    '''
    Starts the WebSocket server process.
    '''
    server = pywsgi.WSGIServer((wsHost, wsPort), WebSocketApi(env, pushInterval, dataLabel), handler_class = WebSocketHandler)
    logging.info('WebSocket server start (%s:%d, pushInterval = %f sec, dataLabel = %s).' % (wsHost, wsPort, pushInterval, dataLabel))
    server.serve_forever()

if __name__ == '__main__':
    # Loads logging settings.
    logging.config.fileConfig(LOG_CONF)
    logging.info('System start.')

    # Loads server settings.
    conf = cp.SafeConfigParser()
    conf.read(SERVER_CONF)
    wsHost       = conf.get('general', 'wsHost')
    wsPort       = int(conf.get('general', 'wsPort'))
    snsPort      = conf.get('sensor', 'snsPort')
    baudRate     = int(conf.get('sensor', 'baudRate'))
    snsTimeout   = float(conf.get('sensor', 'snsTimeout'))
    readSize     = int(conf.get('sensor', 'readSize'))
    readInterval = float(conf.get('sensor', 'readInterval'))
    snsWeight    = float(conf.get('sensor', 'snsWeight'))
    accDigit     = int(conf.get('sensor', 'accDigit'))
    bufSize      = int(conf.get('sensor', 'bufSize'))
    pushInterval = float(conf.get('api', 'pushInterval'))
    dataLabel    = conf.get('api', 'dataLabel')

    the_env = Env(bufSize)

    # Starts the sensor reader process.
    srth = Thread(target = srProc, args = [(the_env, snsPort, baudRate, snsTimeout, readSize, readInterval, snsWeight, accDigit)])
    srth.setDaemon(True)
    srth.start()

    # Starts the WebSocket server process.
    wsth = Thread(target = wsProc, args = [the_env, wsHost, wsPort, pushInterval, dataLabel])
    wsth.setDaemon(True)
    wsth.start()

    # Stops the system when q is typed.
    print 'Type q to stop.'
    while True:
        if raw_input() == 'q':
            logging.info('System stop.')
            break
