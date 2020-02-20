# BOINC-STYLE program Description
# ========================================================================================================
# IMPORTANT: this program has a section at parallel_do_task() to be removed befor cloudbook make
# The section has testing purposes in non-cloudbook version. This section is included inside 
# __CLOUDBOOK:BEGINREMOVE__ and __CLOUDBOOK:ENDREMOVE__ pragmas to delete automatically
#
#                   ------ program description ------
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
#======================= GLOBAL VARS  =====================================================
#__CLOUDBOOK:GLOBAL__
epoch=0 # the same epoch for all agents processing
number_of_agents=0
filename="videos/friends.mp4"
ffcom="-vf hflip"
time_portion=0


# dictionary which matches tokens with tasks
boinc_dict={}


#__CLOUDBOOK:NONSHARED__
unique_id=10 # TOKEN . it is a non shared value for agent_ids. starts at 10 for clarity

#__CLOUDBOOK:NONSHARED__
epoch_done=-1 # this is a non shared value for epoch to avoid repetitions of invocations

# ==========================================================================================
# MAIN function always falls into DU0 --> Agent0
def main():
	global boinc_dict
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
	
	global number_of_agents
	number_of_agents=int(text)

	#create list of portions 
	f = open ('list_concat.txt','w')
	for i in range(0,number_of_agents):
		cad="file 'portion_"+str(i+10)+".mp4' \n"
		f.write(cad)
	f.close()

	# assign a portion to each machine invoking all
	# ----------------------------------------------
	for i in range(0,number_of_agents): 
		token=10 +i %number_of_agents 
		parallel_set_unique_ID(token,False) # this is a parallel function invoked on all agents
		du0_assign_task_to_unique_ID(token, 1) # T1 is the default task
	
	du0_list_agents_tasks()

	du0_main_boinc_menu()

# ==========================================================================================
#__CLOUDBOOK:LOCAL__
def local_T1():
	cad="\n hello, I am "+ str(unique_id)+ " doing T1"
	du0_print (cad)
	#os.system('ffprobe -i concat.mp4 -show_entries format=duration -v quiet -of csv="p=0"')
	global filename
	global fcom
	global time_portion

	start_time=(int (str(unique_id))-10)*time_portion

	command="ffmpeg -y -i "+filename+ " "+ffcom+" -ss "+ str(start_time)+" -t "+ str(time_portion) +" portion_"+str(unique_id)+".mp4"
	print ("\n"+command+"\n")
	return_code = subprocess.call(command, shell=True)
	#du0_print ("duracion"+str(return_code))
	

# ==========================================================================================
#__CLOUDBOOK:LOCAL__
def local_T2():
	cad="\n hello, I am "+ str(unique_id)+ " doing T2"
	du0_print (cad)
	
# ==========================================================================================
# this function is invoked from agent0 to any agent. 
# assign a token to identify each agent univocally
#__CLOUDBOOK:PARALLEL__
def parallel_set_unique_ID(token,replace):
	global unique_id

	if (unique_id!=None and replace==False):
		return
	else:
		unique_id=token
	

# ==========================================================================================
#__CLOUDBOOK:DU0__
def du0_assign_task_to_unique_ID(token, task):
	global boinc_dict
	boinc_dict[token]=task
	
# ==========================================================================================
#__CLOUDBOOK:DU0__
def du0_print(cad):
	print(cad)

# ==========================================================================================
#__CLOUDBOOK:PARALLEL__
def parallel_do_task(epoch):
	global boinc_dict
	global unique_id   # DUDA : esto se pone asi aunque sea una non shared?
	global epoch_done
	global number_of_agents
	
	

	#__CLOUDBOOK:BEGINREMOVE__	
	unique_id+=1 # this is a non shared variable
	if (unique_id==number_of_agents+10):
		unique_id=10
	epoch_done=epoch-1	# this is a non shared variable
	#__CLOUDBOOK:ENDREMOVE__	

	
	if (epoch_done!=epoch):
		epoch_done=epoch
		my_task=boinc_dict[unique_id]
		if (my_task==1):
			local_T1()
		elif (my_task==2):
			local_T2()

# ======================================================================================
#__CLOUDBOOK:DU0__
def du0_concat_files():
	command="ffmpeg -y -f concat -safe 0 -i list_concat.txt -c copy concat_file.mp4"
	print ("\n"+command+"\n")
	return_code = subprocess.call(command, shell=True)

# ======================================================================================
#__CLOUDBOOK:DU0__
def du0_interactive_run():
	global number_of_agents
	global epoch

	input("start? (press ENTER)")
	epoch=epoch+1
	for i in range(number_of_agents):
		parallel_do_task(epoch) 

	print ("\n all agents launched \n")
	
	#__CLOUDBOOK:SYNC__
	print ("\n all agents finished \n")

	#last task is to concat output files
	du0_concat_files()


#===========================================================================================	
#__CLOUDBOOK:DU0__
def du0_interactive_assign_task():
	du0_list_agents_tasks()
	token1=int (input ("token1?:"))
	task1=int(input ("task?[1|2]:"))
	du0_assign_task_to_unique_ID(token1, task1)
	return
#===========================================================================================	
#__CLOUDBOOK:DU0__
def du0_list_agents_tasks():
	print ("\n------ LIST OF AGENTS/TASKS --------\n")
	print (boinc_dict)
	print ("\n------------------------------------\n")
		
	return
#===========================================================================================	
#__CLOUDBOOK:DU0__
def du0_interactive_filename():
	global filename
	filename=input ("video filename?:[videos/friends.mp4]")
	if (filename==""):
		filename="videos/friends.mp4"
		#obtenemos duracion
	command='ffprobe -i '+ filename +' -show_entries format=duration -v quiet -of csv="p=0" >duracion.txt'
	return_code = subprocess.call(command, shell=True)
	f = open ('duracion.txt','r')
	mensaje = f.read()
	global time_portion
	time_portion=(float(mensaje)+1)/number_of_agents
	print("file duration: "+ mensaje)
	print ("each agent will process "+ str(time_portion)+"seconds")
	f.close()
	
	ffcom=input ("ffmpeg command?:[-vf hflip]")
	if (ffcom==""):
		ffcom="-vf hflip"


#===========================================================================================	
#__CLOUDBOOK:DU0__
def du0_main_boinc_menu():

	while (True):		
		#os.system('cls')  # on windows
		print("")
		print ("main menu options")
		print ("=================")
		print (" i: input video filename and ffmpeg command")
		print (" l: list agents vs tasks")
		print (" a: assign a task to an agent")
		print (" r: run agents")
		print (" x: exit")
		
		command=input ("command?:")
		if (command=="l"):
			du0_list_agents_tasks()
		elif (command=="x"):
			sys.exit()
		elif (command=="a"):
			du0_interactive_assign_task()
		elif (command=="r"):
			du0_interactive_run()
		elif (command=="i"):
			du0_interactive_filename()
			
			
#===========================================================================================	


main()