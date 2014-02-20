#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__     = 'Akihiro Miyata'                                                                                                                                                                                                
__copyright__  = 'Copyright (c) 2014 NTT Corp. All rights reserved.'                                         
__maintainer__ = 'Akihiro Miyata'                                                                           
__email__      = 'miyata.akihiro@lab.ntt.co.jp'        

from datetime import datetime as dt

class Sensor:
    def __init__(self, id):
        self.id = id
        self.lastUpdate = dt.now()
    def update(self, observedTime):
        self.lastUpdate = observedTime

class SensorAggr(dict):
    def __init__(self):
        dict.__init__(self)
    def lastUpdate(self, id):
        if id in self:
            return self[id].lastUpdate
        else:
            self[id] = Sensor(id)
            return False
    def update(self, id, observedTime):
        self[id].update(observedTime)

class SensorData():
    def __init__(self, limit):
        self.appendTimes = []
        self.data = []
        self.limit = limit

    def append(self, data):
        '''
        Appends the data to self.data.
        '''
        self.appendTimes.append(dt.now())
        self.data.append(data)
        # If # of elements exeeds the limit, the head elements will be removed.
        if len(self.appendTimes) > self.limit:
            del self.appendTimes[:(len(self.appendTimes) - self.limit)]
            del self.data[:(len(self.data) - self.limit)]

    def extract(self, appendTime):
        '''
        Extracts the data obtained after the specified time.
        '''
        try:
            index = self.appendTimes.index(appendTime) + 1
        except ValueError:
            index = 0
        return self.appendTimes[-1], self.data[index:]

# Test code
if __name__ == '__main__':
    # Case 1
    from datetime import timedelta
    import time
    buffer = SensorData(10)
    for i in xrange(20): buffer.append([1.0, 1.0 + i, 1.0 * i])
    res = buffer.extract(dt.now() - timedelta(1))
    assert len(res[1]) == 10, 'len(buffer) should be 10.'
