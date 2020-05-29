#!/usr/bin/env python

import json
import time

import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt
plt.ion()

import numpy as np

days = 7

def plot(*args):
    fig, ax = plt.subplots()
    for yy in args:
        xx = np.arange(len(yy))
        ee = np.sqrt(yy)
        ax.plot(xx, yy)
        ax.fill_between(xx, yy-ee, yy+ee, alpha=0.2)
        continue
    return

fn = "new-cases-chart-data.json"

raw = eval(open(fn).read())
start = (len(raw[0]) - 1) % days + 1

allTimes = np.array([time.mktime(time.strptime(xx, '%m/%d/%Y')) for xx in raw[0][1:]])
times = np.array([time.mktime(time.strptime(xx, '%m/%d/%Y')) for xx in raw[0][start:]])
times -= times[0]
times /= 86400
times.shape = (-1, days)
times = np.round(times.transpose())

allCooked = np.array([float(xx) for xx in raw[1][1:]])
ma = np.convolve(allCooked, np.ones(days)/days, mode='valid')

cooked = np.array([float(xx) for xx in raw[1][start:]])
cooked.shape = (-1, days)
cooked = cooked.transpose()

byWeek = np.add.reduce(cooked, 0)
byDay = np.add.reduce(cooked, 1)
nDay = np.add.reduce(cooked / byWeek, 1)

plot(byDay)
plot(byWeek)
plot(nDay)
plot(ma)

fig, ax = plt.subplots()
for ii in range(len(times)):
    ax.plot(times[ii], cooked[ii], alpha=0.2)
    continue

plt.show()
