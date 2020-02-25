# BOINC-STYLE program Description
# ========================================================================================================
# this program uses NONSHARED variables mechanism to asign a token to each different agent
# each token identifies univocally each agent. once the token is asigned to an agent, it must not change 
# a dicctionaty matches agents with tasks. 
# interactive functions fall in Agent0 as well as main() funcion.
# rest of agents only will execute 2 fuctions: parallel_set_unique_ID() , parallel_do_task()
# It means that DU_default will contain only these 2 functions.
# this programs offers help at program launching and shows detailed options and menus (easy to use)
# ========================================================================================================


import sys
import time
import random
import os
import subprocess

from datetime import datetime
#======================= GLOBAL VARS  =====================================================
#__CLOUDBOOK:GLOBAL__
number_of_agents=0
filename="videos/friends.mp4"
ffcom="-vf hflip"
time_portion=0
extension="mp4"

# ==========================================================================================
# MAIN function always falls into DU0 --> Agent0
#__CLOUDBOOK:MAIN__
def main():
	global number_of_agents
	
	os.system('cls')  # on windows
	#########################################
	#main program to execute by command line
	#=======================================
	print (" ")
	print (" ")
	print ("Welcome to BOINC program (V1.0)")
	print ("===============================")
	
	text=""
	while text=="":
		text=input ("Aproximate number of agents?:")
	
	number_of_agents=int(text)
	
	du0_main_boinc_menu()


	
# ==========================================================================================
#__CLOUDBOOK:DU0__
def du0_print(cad):
	print(cad)

# ==========================================================================================
#__CLOUDBOOK:PARALLEL__
def parallel_do_task(i, time_portion):	
	cad=("\n hello, I am doing portion"+str(i))
	du0_print (cad)
	#os.system('ffprobe -i concat.mp4 -show_entries format=duration -v quiet -of csv="p=0"')
	global filename
	global ffcom
	global extension
	start_time=int (i*time_portion)

	command="ffmpeg -y -i "+filename+ " "+ffcom+" -ss "+ str(start_time)+" -t "+ str(time_portion) +" portion_"+str(int(i*time_portion))+"."+extension
	print ("\n"+command+"\n")
	return_code = subprocess.call(command, shell=True)

# ======================================================================================
#__CLOUDBOOK:DU0__
def du0_concat_files():
	global extension
	command="ffmpeg -y -f concat -safe 0 -i list_concat.txt -c copy concat_file."+extension
	print ("\n"+command+"\n")
	return_code = subprocess.call(command, shell=True)

# ======================================================================================
#__CLOUDBOOK:DU0__
def du0_interactive_run():
	global number_of_agents
	global time_portion

	input("start? (press ENTER)")


	start_time = datetime.now()
	
	for i in range(number_of_agents):
		parallel_do_task(i,time_portion) 

	print ("\n all agents launched \n")
	
	#__CLOUDBOOK:SYNC__
	print ("\n all agents finished \n")

	#last task is to concat output files
	du0_concat_files()
	end_time = datetime.now()
	elapsed=(end_time-start_time)
	print ("==============================")
	print ("elapsed time:"+str(elapsed))
	print ("==============================")
	

#===========================================================================================	
#__CLOUDBOOK:DU0__
def du0_interactive_filename():
	global filename
	global ffcom
	global extension

	filename=input ("input video filename?:[videos/friends.mp4]")
	if (filename==""):
		filename="videos/friends.mp4"
		#obtenemos duracion
	
	extension=input ("output file extension?:[mp4]")
	if (extension==""):
		extension="mp4"
	
	
	
	global number_of_agents
	


	command='ffprobe -i '+ filename +' -show_entries format=duration -v quiet -of csv="p=0" >duracion.txt'
	return_code = subprocess.call(command, shell=True)
	f = open ('duracion.txt','r')
	mensaje = f.read()
	f.close()
	global time_portion
	time_portion=int (1+(float(mensaje)+1)/number_of_agents)
	print("file duration: "+ mensaje)
	print ("There are "+str(number_of_agents)+" -> each agent will process "+ str(time_portion)+" seconds")
	

	#create list of portions  to concat
	f = open ('list_concat.txt','w')
	for i in range(0,number_of_agents):
		cad="file 'portion_"+str(int(i*time_portion))+"."+extension+"' \n"
		f.write(cad)
	f.close()
	
	ffcom=input ("ffmpeg command?:[-vf hflip]")
	if (ffcom==""):
		ffcom="-vf hflip"
	if (ffcom=="-"):
		ffcom=""



#===========================================================================================	
#__CLOUDBOOK:DU0__
def du0_main_boinc_menu():

	while (True):		
		#os.system('cls')  # on windows
		print("")
		print ("main menu options")
		print ("=================")
		print (" i: input video filename and ffmpeg command")
		print (" r: run agents")
		print (" x: exit")
		
		command=input ("command?:")
		
		if (command=="x"):
			sys.exit()
		elif (command=="r"):
			du0_interactive_run()
		elif (command=="i"):
			du0_interactive_filename()
			
			
#===========================================================================================	


main()