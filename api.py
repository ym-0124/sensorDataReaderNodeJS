#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__     = 'Akihiro Miyata'
__copyright__  = 'Copyright (c) 2014 NTT Corp. All rights reserved.'
__maintainer__ = 'Akihiro Miyata'
__email__      = 'miyata.akihiro@lab.ntt.co.jp'

from gevent import sleep
import json

class WebSocketApi(object):
    def __init__(self, env, pushInterval, dataLabel):
        self.env = env
        self.pushInterval = pushInterval
        self.dataLabel = dataLabel
        
    def __call__(self, environ, start_response):
        '''
        Sends sensor data to the web socket client.
        '''
        ws = environ['wsgi.websocket']
        while True:
            try:
                # Fetches the data following the previous ones.
                lastFetchTime = self.env.wsLastFetchTimes[ws]
                currFetchTime, data = self.env.snsData.extract(lastFetchTime)
            except KeyError:
                # For the first fetch (or the case where the previous data have been removed from the buffer).
                currFetchTime = self.env.snsData.appendTimes[-1]
                data = self.env.snsData.data
            # Sends the data to the web socket client.
            ws.send(json.dumps({self.dataLabel : data}))
            # Updates the last fetch time.
            self.env.wsLastFetchTimes[ws] = currFetchTime
            sleep(self.pushInterval)
