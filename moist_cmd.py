import RPi.GPIO as GPIO
from time import sleep
import mcp3008
import httplib, urllib,urllib2
import time
import MySQLdb
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)
sleep = 2.5# how many seconds to sleep between posts to the channel
key = 'GFORB9SZFJ0GPTPU'  # Thingspeak channel to update
crop= ''

required_moisture_per_crop={'Beans':[300,500],'Citrus':[900,1200],'Cotton':[700,1300],'Groundnut':[500,700],'Maize':[500,800],'Soybean':[450,700]}

def thermometer():
    while True:
        m=sensor_data=mcp3008.readadc(5)
	status=GPIO.input(21)
     #   params = urllib.urlencode({'field1': sensor_data, 'key':key }) 
     #  headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
     #  conn = httplib.HTTPConnection("api.thingspeak.com:80")
     #   try:
     #	    print "in try"
     #       conn.request("POST", "/update", params, headers)
     #       response = conn.getresponse()
    
     #      print response.status, response.reason
     #       data = response.read()
     #	    print data
     #	    print "is the data"
     #       conn.close()
     #   except:
     #       print "connection failed"
     #      break
	if m>500:
	        GPIO.output(21,1)
    	else:
        	GPIO.output(21,0)
    	print "Moisture level: {:>5} ".format(sensor_data)
def  change_valve_manual():
	while True:
		try:
			req=urllib2.Request('http://mahikanthnag.net23.net/solenoid_status_retrieve.php')
			response = urllib2.urlopen(req)
			print "in try"
			the_page = response.read()	
			print "after response"
			s1=the_page[0:2]
			s2 = 'ON'
			if s1==s2:
				print "valve on"
				GPIO.output(21,1)
				time.sleep(5)
			else:				
				print "valve off"
				GPIO.output(21,0)
				time.sleep(5) 
				
		except:
			print "error"
			break

def getCropName():
	
		try:
                        req=urllib2.Request('http://mahikanthnag.net23.net/crop_name_retrieve.php')
                        crop_name_url = urllib2.urlopen(req)
                        print "in try"
                        crop = crop_name_url.read()
                        print "after response"
                        crop= crop.split('\n')[0]
			print crop
			print "is the selected crop"
			
                        return crop.strip()
                except:
                        print "error"
                        

def change_valve_auto():
	global crop
	while(1):
	 m1 = int(mcp3008.readadc(5))
	 m2 = int(mcp3008.readadc(6))
	 m3 = int(mcp3008.readadc(7))
         print "Moisture level1: {:>5} ".format(m1)
	 print "Moisture level2 : {:>5} ".format(m2)
	 print "Moisture level3 : {:>5} ".format(m3)
	 time.sleep(2);
	 print crop
	 print required_moisture_per_crop[crop]
	 if ((m1+m2+m3))>3*required_moisture_per_crop[crop][1]:
		GPIO.output(21,1)
	 else:
		GPIO.output(21,0)
	

def set_crop():
	global crop
	while(1):
		crop = getCropName()
		print required_moisture_per_crop[crop][1]
		print "test"
		if crop!='undefined' :
			break
		
if __name__ == "__main__":
        global crop
	set_crop()
	while True:
		print crop
		print "fter setcrop"
                change_valve_auto()
                time.sleep(sleep)


