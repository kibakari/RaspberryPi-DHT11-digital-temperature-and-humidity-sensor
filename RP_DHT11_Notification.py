import RPi.GPIO as GPIO
import dht11
import time
import datetime
import requests

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

sensor_list = [
	dht11.DHT11(pin=15)
	]

# when you increase the number of the sensors, change like below.
'''
sensor_list = [
	dht11.DHT11(pin=14),
	dht11.DHT11(pin=15)
 ...
	]
'''

result = [0] * (len(sensor_list)+1)
Webhook_url = '***'  # fill your url
output_data = ''

try:
	while True:
		for sensor_num in range(len(sensor_list)):
			retry_conunter = 0
			while (retry_conunter < 50):
				result[sensor_num] = sensor_list[sensor_num].read()
				if result[sensor_num].is_valid():
					print("Last valid input: " + str(datetime.datetime.now()))
					print("Temperature%d: %-3.1f C" % (sensor_num+1, result[sensor_num].temperature))
					print("Humidity%d: %-3.1f %%" % (sensor_num+1, result[sensor_num].humidity))
					print(retry_conunter)
					break
				elif retry_conunter >= 49:
					print("cannot get the sensor data")
				else:
					retry_conunter += 1
			if sensor_num == 0:
				output_data ={'key':'%d Temp: %-3.1f \u2103 \n%d Humid: %-3.1f %%\n' % (sensor_num+1, result[sensor_num].temperature, sensor_num+1, result[sensor_num].humidity)}
			else:
				output_data['key'] += '%d Temp: %-3.1f \u2103 \n%d Humid: %-3.1f %%\n' % (sensor_num+1, result[sensor_num].temperature, sensor_num+1, result[sensor_num].humidity)
		response = requests.post(Webhook_url,json=output_data)
		print(response.text)
		time.sleep(30)


except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
