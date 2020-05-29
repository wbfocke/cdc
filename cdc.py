#!/usr/bin/env python

import json
import time
import urllib

import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt
plt.ion()

import numpy as np


url = "https://www.cdc.gov/coronavirus/2019-ncov/json/new-cases-chart-data.json"
chs = 'utf-8-sig'
skipItems = 1 # skip column headers

days = 7


raw = json.loads(urllib.urlopen(url).read().decode(chs))

times = np.array([time.mktime(time.strptime(xx, '%m/%d/%Y')) for xx in raw[0][skipItems:]])
times -= times[0]
times /= 86400
times = np.round(times)
times += 0.5

cases = np.array([float(xx) for xx in raw[1][skipItems:]])

kernel = np.ones(days)/days

maTimes = np.convolve(times, kernel, mode='valid')
maCases = np.convolve(cases, kernel, mode='valid')
maSigma = np.sqrt((np.convolve(cases**2, kernel, mode='valid') - maCases**2) * days / (days - 1))

fig, ax = plt.subplots()
for ii in range(days):
    ax.plot(times[ii::7], cases[ii::7], alpha=0.3)
    continue

ax.plot(maTimes, maCases)
ax.fill_between(maTimes, maCases-maSigma, maCases+maSigma, alpha=0.2)
ax.plot(times, cases, alpha=0.2)

plt.show()
