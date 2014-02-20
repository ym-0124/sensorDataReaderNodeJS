#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__     = 'Reiko Aruga and Akihiro Miyata'
__copyright__  = 'Copyright (c) 2014 NTT Corp. All rights reserved.'
__maintainer__ = 'Akihiro Miyata'
__email__      = 'miyata.akihiro@lab.ntt.co.jp'

import sensor

from datetime import datetime as dt
import logging
import serial
import time

class SensorReader():
    def __init__(self, env, snsPort, baudRate, snsTimeout, readSize, readInterval, snsWeight, accDigit):
        self.env = env
        self.sensors = sensor.SensorAggr()
        self.ser = serial.Serial(port = snsPort, baudrate = baudRate, timeout = snsTimeout)
        logging.info('Serial port initialized (snsPort = %s, baudRate = %d, snsTimeout = %f).' % (snsPort, baudRate, snsTimeout))
        self.readSize = readSize
        self.readInterval = readInterval
        self.W = snsWeight
        self.D = accDigit

    def start(self):
        logging.info('SensorReader start (readSize = %d, readInterval = %f, snsWeight = %f, accDigit = %d).' % (self.readSize, self.readInterval, self.W, self.D))
        while True:
            buf = []
            for bd in self.ser.read(self.readSize): buf.append(ord(bd))
            recvnum = len(buf)
            for i in xrange(recvnum):
                if (hex(buf[i]) == hex(ord('$'))) or (hex(buf[i]) == hex(ord('+'))):
                    try:
                        length = (buf[i + 2] & 0xff) | ((buf[i + 3] & 0xff) << 8)
                        if (recvnum - i) < (length + 5): break
                        else:
                            z = i + 7
                            k = buf[z + 6] * 2 + 11

                            # Gets the last update time of the sensor.
                            id = (buf[z + ((buf[z + 6] & 0xff) - 1) * 2 + 7] & 0xff) | ((buf[z + ((buf[z + 6] & 0xff) - 1) * 2 + 8] & 0xff) << 8)
                            observedTime = self.sensors.lastUpdate(id)
                            if not observedTime: break
                            step = (dt.now() - observedTime) / recvnum

                            # Reads temperature, luminance, battery and acceleration data.
                            tmp = (buf[z + k] & 0xff) + ((buf[z + k + 1] & 0xff) << 8)
                            lum = (buf[z + k + 2] & 0xff) + ((buf[z + k + 3] & 0xff) << 8)
                            bat = (buf[z + k + 4] & 0xff) + ((buf[z + k + 5] & 0xff) << 8)
                            k += 6
                            for c in xrange(z + k, i + length, 6):
                                xraw = (buf[c] & 0xff) + ((buf[c + 1] & 0xff) << 8)
                                x = round(xraw * self.W, self.D) if xraw < 128 else round((xraw - 256) * self.W, self.D)
                                yraw = (buf[c + 2] & 0xff) + ((buf[c + 3] & 0xff) << 8)
                                y = round(yraw * self.W, self.D) if yraw < 128 else round((yraw - 256) * self.W, self.D)
                                zraw = (buf[c + 4] & 0xff) + ((buf[c + 5] & 0xff) << 8)
                                z = round(zraw * self.W, self.D) if zraw < 128 else round((zraw - 256) * self.W, self.D)
                                self.env.snsData.append([observedTime.strftime('%H:%M:%S.%f'), id, tmp, lum, bat, x, y, z])
                                observedTime += step
                            self.sensors.update(id, observedTime)
                            i += length + 4
                    except IndexError: pass
            time.sleep(self.readInterval)
