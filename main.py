import smbus
import time
import math
import _thread
from datetime import datetime
from pushover import init, Client
from gpiozero import Buzzer
from gpiozero import Button
from MinIMU_v5_pi import MinIMU_v5_pi

#Global variables:
buzzerFlag = False
buzzerTime = 0

def Get_Magnitude_Difference(prev_value, current_value):
	#current_value = IMU.readAccelerometer()
	valX = current_value[0] - prev_value[0]
	valY = current_value[1] - prev_value[1]
	valZ = current_value[2] - prev_value[2]
	val = [valX,valY,valZ]
	return math.sqrt(valX**2 + valY**2 + valZ**2)


def button_pressed_handler():
	global buzzerFlag
	buzzerFlag = False

def handle_buzzer():
	
	global buzzerFlag
	global buzzerTime
	pushoverKey = "utbdicrgcw9aqkmxweyq4ent9kxzbh"
	buzzer = Buzzer(17)
	
	frequency = 2 if buzzerTime<3.5 else 4
	
	if(buzzerTime >= 7):
		buzzerFlag = False
		now = datetime.now()
		currentTime = now.strftime("%H:%M:%S")
		Client(pushoverKey).send_message("The Person has fallen and has not responded at " + currentTime, title="Emergency: Fallen Person")
		buzzerTime = 0
	
	if(buzzerFlag == True):
		print(buzzerTime)
		buzzer.on()
		time.sleep(1/frequency)
		buzzerTime = buzzerTime + 1/frequency
	else:
		buzzer.off()
		
	return buzzerTime
	

def main():
		pushoverAPIToken = "a5fte2rvo476jmo8fcaqtkjmav59ie"
		init(pushoverAPIToken)
		IMU = MinIMU_v5_pi()
		#IMU.trackYaw()
		button = Button(27)
		global buzzerFlag
		global buzzerTime
		button.when_pressed = button_pressed_handler
		prev_value_acc = IMU.readAccelerometer()
		prev_value_gyro = IMU.readGyro()
		
		IMU.trackAngle()
		while True:
						
			current_value_acc = IMU.readAccelerometer()
			current_value_gyro = IMU.readGyro()
				
			magnitude_diff_acc = Get_Magnitude_Difference(prev_value_acc, current_value_acc)
			magnitude_diff_gyro = Get_Magnitude_Difference(prev_value_gyro, current_value_gyro)
			
			if(magnitude_diff_acc > 20 and magnitude_diff_gyro > 400):
				buzzerTime = 0
				buzzerFlag = True	
			
			handle_buzzer()
			prev_value_acc = current_value_acc
			prev_value_gyro = current_value_gyro
			time.sleep(0.1)


if __name__ == "__main__":
	print("MinIMU is main")
	main()
	
