from __future__ import print_function
import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""
d_th = 0.4
""" float: Threshold for the control of the linear distance"""
R = Robot()
""" instance of the class Robot"""

Grabber = list()
""" to import a code on the grabbed boxes """
#Gold = True

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):

    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
	
def find_gold():

	"""
	Function to find the closest Golden Box with no elements in the list "GrabbedGold"
	
	Returns:
	dist (float): distance of the closest golden token (-1 if no token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no token is detected)
	Code (int): The code of the closest golden token (-1 if no golden token is detected)
	
	"""

	dist =100

	for token in R.see():
		if token.dist<dist and token.info.marker_type == MARKER_TOKEN_GOLD and token.info.code not in Grabber:   
			dist = token.dist
			rot_y = token.rot_y
			Code = token.info.code	
	if dist == 100:
		return -1 , -1 ,-1
	
	else:
		return dist,rot_y,Code
		
def release_find_gold():

	"""
	Function to find the closest box nearby (among the boxes that were previously grabbed and put next to each other) as a drop location
	It finds the closest box which is in the "GrabbedGold" list and takes the box it grabbed to the location
	It finds the closest one so it does not bump into the other boxes on its way
	
	Returns:
	dist (float): distance of the closest golden token (-1 if no token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no token is detected)
	Code (int): The code of the closest golden token (-1 if no golden token is detected)
	
	
	"""
     
	dist =100
	
	for token in R.see():
		if token.dist<dist and token.info.marker_type == MARKER_TOKEN_GOLD and token.info.code in Grabber:
			dist = token.dist
			rot_y = token.rot_y
			Code = token.info.code	
	if dist == 100:
		return -1 , -1 ,-1
	
	else:
		return dist,rot_y,Code

def grabbing():

	"""
	Function to move towards the closest box nearby ( The boxes that are not yet grabbed and moved)
	
	"""
     
	while True:
	    dist, rot_y ,Code = find_gold()  # looking for the gold boxes
	    if dist <= d_th: # if the robot is close to a gold box, the while loop stopped, then the robot can grab the box 
		print("Found a gold box!")	 
		
		break
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token but not close enough, we go forward to reach the gold box
		print("Going forward!")
		drive(10, 1)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right until it's aligned
		print("Left a bit...")
		turn(-1, 1)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(10, 1)

def Release_Grabbed_Gold():
	"""
	
	Function to move towards the closest drop location ( The closest box which was previously moved and relocated)
	
	"""
     
	while True:
	    dist,rot_y,Code = release_find_gold()  # looking for the previously gold box 
	    if dist < d_th + 0.15:  # if the robot is well aligned with the token but not close enough, we go forward to reach the gold box
	    # The 0.15 value is defined to leave a small distance between boxes	 
		
		break
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the dropping place but not close enough, we go forward to put it
		print("Getting closer!")
		drive(10, 1)
	    elif rot_y < -a_th: # if the robot is not well aligned with the dropping place, we move it on the left or on the right until it's aligned
		print("Left a bit...")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(10, 2)
	

dist,rot_y,Code = find_gold() # the robot search for the closest gold box
while dist == -1:  # if the robot couldn't find any gold box, it keeps turning and searching to find any one
	print("Searching for the gold boxes")
	turn(10,4)
	dist,rot_y,Code = find_gold()
	
grabbing() # the robot goes toward the closest gold box to grab the box
R.grab()
print("Found a gold box!")
	
turn(-10,2) # the robot turns around and goes forward to a the dropping place
drive(10 , 20)
R.release()
print("Done")
	
# the robot goes back to avoiding tauch any boxes
drive(-10 , 2)
turn(20,4)

Grabber.append(Code) # the code of the previous box added to the list. robot looks for other gold boxes

while len(Grabber)<6: # at the end the robot has the code of all 6 boxes correctly
# the robot goes toward the closest gold box to grabs it
	dist,rot_y,Code= find_gold()
	while dist == -1:
		print("Searching for the gold boxes")
		turn(10,4)
		dist,rot_y,Code = find_gold()
	grabbing()
	R.grab()
	print("Found a gold box!")		
	# the robot found a dropping place to put the box on it
	dist1,rot1_y,code1 = release_find_gold()
		
	while dist1 == -1:
		print("Getting closer!")
		turn(20,2)
		dist1,rot1_y,code1 = release_find_gold()
	Release_Grabbed_Gold()
	R.release()
	print("Done")
	drive(-10,2)
	turn(10,4)
		
	Grabber.append(Code) # the code of the previous box added to the list. robot looks for other gold boxes
