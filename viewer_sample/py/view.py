#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__     = 'Akihiro Miyata'
__copyright__  = 'Copyright (c) 2014 NTT Corp. All rights reserved.'
__maintainer__ = 'Akihiro Miyata'
__email__      = 'miyata.akihiro@lab.ntt.co.jp'

import json
from websocket import create_connection

ws = create_connection('ws://127.0.0.1:8080/')

while True:
    try:
        raw = ws.recv()
        parsed = json.loads(raw)
        for data in parsed['data']: print data
    except KeyboardInterrupt: break
