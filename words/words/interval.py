# encoding=utf-8
from __future__ import print_function, unicode_literals, division
import datetime

data = {
    0: datetime.timedelta(minutes=0),
    1: datetime.timedelta(minutes=5),
    2: datetime.timedelta(minutes=30),
    3: datetime.timedelta(hours=3),
    4: datetime.timedelta(hours=5),
    5: datetime.timedelta(hours=12),
    6: datetime.timedelta(days=1),
    7: datetime.timedelta(days=3),
    8: datetime.timedelta(days=5),
    9: datetime.timedelta(days=7),
    10: datetime.timedelta(days=10),
    11: datetime.timedelta(days=15),
    12: datetime.timedelta(days=20),
    13: datetime.timedelta(days=25),
    14: datetime.timedelta(days=30),
    15: datetime.timedelta(days=35),
    16: datetime.timedelta(days=40),
    17: datetime.timedelta(days=50),
    18: datetime.timedelta(days=60),
    19: datetime.timedelta(days=70),
    20: datetime.timedelta(days=80),
    21: datetime.timedelta(days=90),
    22: datetime.timedelta(days=100),
    23: datetime.timedelta(days=120),
    24: datetime.timedelta(days=150),
    25: datetime.timedelta(days=200),
    26: datetime.timedelta(days=250),
    27: datetime.timedelta(days=300),
    28: datetime.timedelta(days=350),
    29: datetime.timedelta(days=400),
    30: datetime.timedelta(days=500),
    31: datetime.timedelta(days=700),
    32: datetime.timedelta(days=1000),
    33: datetime.timedelta(days=1500),
    34: datetime.timedelta(days=2000),
    35: datetime.timedelta(days=2500),
    36: datetime.timedelta(days=3000),
    37: datetime.timedelta(days=5000),
    38: datetime.timedelta(days=8000),
    39: datetime.timedelta(days=10000),
    40: datetime.timedelta(days=20000),
}


def interval(level):
    return data[level]
