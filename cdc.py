#!/usr/bin/env python

import json
import time
import urllib

import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt
plt.ion()

import numpy as np

skipBytes = 3
skipItems = 1
days = 7
fn = "new-cases-chart-data.json"
url = "https://www.cdc.gov/coronavirus/2019-ncov/json/new-cases-chart-data.json"

#raw = json.loads(open(fn).read()[skipBytes:])
raw = json.loads(urllib.urlopen(url).read()[skipBytes:])

times = np.array([time.mktime(time.strptime(xx, '%m/%d/%Y')) for xx in raw[0][skipItems:]])
times -= times[0]
times /= 86400
times = np.round(times)
times += 0.5

cases = np.array([float(xx) for xx in raw[1][skipItems:]])

kernel = np.ones(days)/days

maTimes = np.convolve(times, kernel, mode='valid')
maCases = np.convolve(cases, kernel, mode='valid')

fig, ax = plt.subplots()
for ii in range(days):
    ax.plot(times[ii::7], cases[ii::7], alpha=0.3)
    continue

ax.plot(maTimes, maCases)
ax.plot(times, cases, alpha=0.2)

plt.show()
