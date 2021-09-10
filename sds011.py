# python code combined from 
# https://towardsdatascience.com/sensing-the-air-quality-5ed5320f7a56
# and https://www.raspberrypi.org/blog/monitor-air-quality-with-a-raspberry-pi/
# and utilizes code from https://github.com/ikalchev/py-sds011

import serial, time, datetime, logging, sys, aqi
from Adafruit_IO import Client
from sds011 import *

# try logging to stdout
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# create an instance of the SDS011 sensor for gathering data
sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)

# create a client for Adafruit
aio = Client("atorman", "aio_iHnb71IgtDvC15QFDORh2jeDz0YT")

# start timer
dt = datetime.datetime.now()
print (f'start timer: {dt}')

# loop for a specific range of time
# for instance, 0-1440 and sleep 60 seconds = 
# 1 reading per 1 minutes for a day

for index in range(0,144):
	# wake up sensor to collect data for a period of time
	sensor.sleep(sleep=False)
	time.sleep(58)
	#time.sleep(10)
	
	# query the sensor for that data
	pmt_2_5, pmt_10 = sensor.query()
	
	# convert to AQI from python-aqi (https://pypi.org/project/python-aqi
	aqi_2_5 = aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pmt_2_5), algo=aqi.ALGO_EPA)
	aqi_10 = aqi.to_iaqi(aqi.POLLUTANT_PM10, str(pmt_10), algo=aqi.ALGO_EPA)
	
	# grab a date timestamp and print it to screen with the
	# data it collected for PMT 2.5 and 10
	ct = datetime.datetime.now()
	print (ct)
	print (f"PMT2.5: {pmt_2_5}")
	print (f"PMT10: {pmt_10}")
	print (f"PMT2.5 AQI: {aqi_2_5}")
	print (f"PMT10 AQI: {aqi_10}")
    
	# send the data to Adafruit - cast decimal as string
	aio.send('pmt2-dot-5', pmt_2_5)
	aio.send('pmt10', pmt_10)
	aio.send('aqi2-dot-5', str(aqi_2_5))
	aio.send('aqi10', str(aqi_10))
	
	# put the sensor to sleep for a few seconds before
	# looping to collect the next series of data
	sensor.sleep(sleep=True)
	time.sleep(540)
	#time.sleep(2)
