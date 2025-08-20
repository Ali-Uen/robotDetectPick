from workspace import *
from converter import *
from pyniryo import *
import numpy as np
import math


def convert_data(data):
	
	# converts centimeter to meter
	pos_cm = np.array([data[0],data[1],data[2]])
	pos_m = np.array(pos_cm/100)
	pos_m = np.around(pos_m, 2)

	# converts degree to radient
	end_d = np.array([data[3],data[4],data[5]])
	end_r = np.array(end_d)*((math.pi)/180)
	end_r = np.around (end_r, 2)
	
	# sort data into an array
	j1 = pos_m[0]
	j2 = pos_m[1]
	j3 = pos_m[2]
	j4 = end_r[0]
	j5 = end_r[1]
	j6 = end_r[2]

	convert =[j1,j2,j3,j4,j5,j6]
	return (convert)
