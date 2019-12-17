import cv2
import numpy as np
from pynput import keyboard
import imutils
import serial
import time

var = serial.Serial('COM3',9600)#เลือก comport ที่เชื่อมต่อ Arduino
time.sleep(2)
print("Connected to Arduino...")

KILL = False

# function for registering key presses
def on_press(key):
	if key.char == 'q':
		global KILL
		KILL = True
		#print('Killing now')

def main():
	#ที่อยู่ของ Model Machine Leaning
	net = cv2.dnn.readNetFromCaffe('C:/Users/Jue/Desktop/TurtleBot-Follow-Person-master/TurtleBot-Follow-Person-master/MobileNetSSD_deploy.prototxt.txt', 'C:/Users/Jue/Desktop/TurtleBot-Follow-Person-master/TurtleBot-Follow-Person-master/MobileNetSSD_deploy.caffemodel')

	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
	
	#ติดต่อกับ Camera
	cap = cv2.VideoCapture(0)

	# Take first frame
	ret, frame = cap.read()
	(h, w) = frame.shape[:2]
	h1 = int(h / 2)
	dot1 = int(w / 2)

	while 1:
		# capture next frame and convert to grayscale
		ret, frame = cap.read()
		frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		# convert frame to a blob for object detection
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
			0.007843, (300, 300), 127.5)
		net.setInput(blob)
		detections = net.forward()

		# loop over the detections
		for i in np.arange(0, detections.shape[2]):
			object_type = detections[0,0,i,1]
			confidence = detections[0, 0, i, 2]
			if object_type == 15 and confidence > 0.2: # execute if confidence is high for person detection
				# extract the index of the class label from the
				# `detections`, then compute the (x, y)-coordinates of
				# the bounding box for the object 
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

                #function ส่งค่าไปยัง Arduino
				distant = endX
				print(distant)
				if distant >= 430:
    					test = var.write('f'.encode())  #sent Arduino
				if distant <= 429:
    					var.write('o'.encode()) #sent to Arduino end function sent to Arduino
				centerX =  int(startX + ((endX - startX)/2))
				centerY =  int(startY + ((endY - startY)/2))
                
				if centerX > dot1 +21 :
    					Go = var.write('p'.encode())
				if centerX < dot1 -22 :
    					Back = var.write('m'.encode())
				#draw the prediction on the frame
				#label = "{}: {:.2f}%".format('person',confidence * 100)
				cv2.rectangle(frame, (startX, startY), (endX, endY),(204,0,0), 2)
				#ศูนย์กลางของกรอบคน
				dot = cv2.circle(frame,(centerX,centerY),5,(255,255,255),-1)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				#cv2.putText(frame, label, (startX,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[int(object_type)], 2)
		cv2.imshow('SNC Test Camera', frame)
		
		if KILL:
			print("\nFinished")
			cv2.destroyAllWindows()
			exit()
		cv2.waitKey(1)

if __name__ == '__main__':
	listener = keyboard.Listener(on_press=on_press)
	listener.start()
	main()
	exit()