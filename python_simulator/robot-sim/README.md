Research_Track1_Assignment1
------------------------------------------------
The first assignment of the Research Track1 is to set the robot to find and grab all the gold boxes in the environment ` Figure1 ` and put all together as in ` Figure2 ` showed.

![First_pos](https://github.com/AlirezaTj99/Research_Track_Assignment1/assets/150545194/2b93591c-33b3-4b9b-9d02-0d944454b071)
> Figure1) The first place of the configuration of the boxes

![Final_pos](https://github.com/AlirezaTj99/Research_Track_Assignment1/assets/150545194/d7795262-aa61-4887-b40f-98a3c3c75ac2)
> Figure2) Final configuration of the gold boxes

![](sr/Flowchart.png)
> Figure3) flowchart

Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

## Exercise
-----------------------------

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

When done, you can run the program with:

```bash
$ python2 run.py assignment.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```
Coding
-------------------------
The robot should search, find, grab, move and place all the gold boxes together in a same lacation. For this, we have some parameters: `a_th` and `d_th`. They are the angle and distance threshold, respectively. These parameters help robot to understand when it's close to the gold box to grab. And also the `Grabber` that we list() the code of the last boxes that robot grabbed and put them in the right location. We also have another defined functions: 
`drive`
`turn`
`find_gold()`
`release_find_gold()`
`grabbing()`
`Release_Grabbed_Gold()`

### drive ###
Function for setting a linear velocity
Args: speed (int): the speed of the wheels
seconds (int): the time interval

```python
def drive(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

```
### turn ###
Function for setting an angular velocity
Args: speed (int): the speed of the wheels
seconds (int): the time interval

```python
def turn(speed, seconds):

    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

```
### find_gold() ###
Function to find the closest Golden Box with no elements in the list "GrabbedGold"
	
Returns:
dist (float): distance of the closest golden token (-1 if no token is detected)
rot_y (float): angle between the robot and the golden token (-1 if no token is detected)
Code (int): The code of the closest golden token (-1 if no golden token is detected)

```python
def find_gold():

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

```
### release_find_gold() ###
Function to find the closest box nearby (among the boxes that were previously grabbed and put
next to each other) as a drop location
It finds the closest box which is in the "GrabbedGold" list and takes the box it grabbed to the location
It finds the closest one so it does not bump into the other boxes on its way
	
Returns:
dist (float): distance of the closest golden token (-1 if no token is detected)
rot_y (float): angle between the robot and the golden token (-1 if no token is detected)
Code (int): The code of the closest golden token (-1 if no golden token is detected)

```python
def release_find_gold():
     
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

```
### grabbing() ###
Function to move towards the closest box

```python

def grabbing():
     
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

```
### Release_Grabbed_Gold() ###
Function to move robot towards the closest dropping place

```python
def Release_Grabbed_Gold():
     
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

```
### while ###

```python
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

```
[sr-api]: https://studentrobotics.org/docs/programming/sr/
