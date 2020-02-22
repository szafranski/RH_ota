
### You can change user name and version you want to use here:

name = 'pi'           ### change to '<your username>' or leave unchanged if you haven't changed the default username on raspberry

version = 'master'    ### change to eg. '2.0.2' or leave as it is (can be in beta so check out latest release page:
                      ### https://github.com/RotorHazard/RotorHazard/releases and check current "Latest release version"

from time import sleep
import os
import sys
class bcolors:
	HEADER = '\033[95m'
	BLUE = '\033[94m'
	OKGREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def image():
	print("""
\t\t\t                               **/(((/**                              
\t\t\t                            */###########(*                           
\t\t\t                          */#####@@@@@#####(*                         
\t\t\t                         *(((((@@@###@@@#####*,                       
\t\t\t                       */((((@@@#######@@@####/*                      
\t\t\t                      *(((((@@@(((((#(##@@@#####*                     
\t\t\t                    **((((&@@&((((*...####@@@####**                   
\t\t\t                   *(((((@@@((((((....((((#@@@#####*                  
\t\t\t                 **((((#@@@((((((*.....((((#%@@&####/*                
\t\t\t                */((((@@@((((((((......(((((((@@@####(*               
\t\t\t              .*(((((@@@(((((((((......((((((((@@@%####**             
\t\t\t             */((((@@@(((((((((((......((((((((((@@@####(*            
\t\t\t            *(((((@@@((((((((((((.....*(((((((((((@@@#####*,          
\t\t\t          **((((@@@((((((((((((((.....((((((((((((((@@@(#(#/*         
\t\t\t          *((((@@@(((((((((((((((.....(((((((((((((((@@@((###*        
\t\t\t       */((((&@@&(((((((((((((,...(((....(((((((((((((#@@@((((/*      
\t\t\t      */((((@@@(((((((((......................((((((((((@@@((((#*     
\t\t\t    .*//(((@@@((((((............(((((((*.........,(((((((%@@&((((/*   
\t\t\t   */////@@@(((((........../((((((((((((((*..........((((((@@@(((((*  
\t\t\t  */////@@@/(((......./(((((((((((((((((((((((/......../((((@@@#((((*.
\t\t\t *////%@@/////(((((((((((((((((((((((((((((((((((((((..(((((((@@@((((*
\t\t\t *////@@@/////////((((((((((((((((((((((((((((((((((((((((((((@@@((((*
\t\t\t **/////@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#((((**
\t\t\t  ***/////////////////(((((((((((((((((((((((((((((((((((((((((((((** 
\t\t\t     ****////////////////((((((((((((((((((((((((((((((((((((/****   
""")


def first ():
	image ()
	os.system("clear")
	print("\n\n\n\n\n")
	image()
	sleep(1.6)
first()

def installation():
	#os.system("sudo killall python *server.py")
	os.system("sudo systemctl stop rotorhazard")
	os.system("clear")
	sleep(0.1)
	print("\n\t\t Installation process started - please wait... \n")
	os.chdir("/home/"+name)
	os.system("sudo apt-get update && sudo apt-get upgrade -y")
	os.system("sudo systemctl enable ssh")
	os.system("sudo systemctl start ssh ")
	os.system("sudo apt-get install wget libjpeg-dev i2c-tools python-dev python-rpi.gpio libffi-dev python-smbus build-essential python-pip git scons swig -y")
	os.system("sudo pip install cffi ")
	os.system("sudo pip install pillow")
	os.system("echo 'dtparam=i2c_baudrate=75000' | sudo tee -a /boot/config.txt")
	os.system("echo 'core_freq=250' | sudo tee -a /boot/config.txt")
	os.system("echo 'dtparam=spi=on' | sudo sudo tee -a /boot/config.txt  ")  
	os.system("echo 'i2c-bcm2708' | sudo tee -a /boot/config.txt")
	os.system("echo 'i2c-dev' | sudo tee -a /boot/config.txt")
	os.system("echo 'dtparam=i2c1=on' | sudo tee -a /boot/config.txt")
	os.system("echo 'dtparam=i2c_arm=on' | sudo tee -a /boot/config.txt")
	os.system("sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf")
	os.system("sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf")
	os.chdir("/home/"+name)
	os.system("wget https://codeload.github.com/RotorHazard/RotorHazard/zip/"+version+" -O temp.zip")
	os.system("unzip temp.zip")
	os.system("rm temp.zip")
	os.system("mv RotorHazard-"+version+" /home/"+name+"/RotorHazard")
	os.system("sudo pip install -r /home/"+name+"/RotorHazard/src/server/requirements.txt")
	os.system("sudo chmod 777 /home/"+name+"/RotorHazard/src/server")
	os.chdir("/home/"+name)
	os.system("sudo git clone https://github.com/jgarff/rpi_ws281x.git")
	os.chdir("/home/"+name+"/rpi_ws281x")
	os.system("sudo scons")
	os.chdir("/home/"+name+"/rpi_ws281x/python")
	os.system("sudo python setup.py install")
	os.chdir("/home/"+name)
	os.system("sudo git clone https://github.com/chrisb2/pi_ina219.git")
	os.chdir("/home/"+name+"/pi_ina219")
	os.system("sudo python setup.py install")
	os.chdir("/home/"+name)
	os.system("sudo git clone https://github.com/rm-hull/bme280.git")
	os.chdir("/home/"+name+"/bme280")
	os.system("mkdir /home/"+name+"/.old_RotorHazard.old")
	os.system("echo 'leave this file here' | sudo tee -a /home/"+name+"/.old_RotorHazard.old/.installation-check_file.txt")
	os.system("sudo python setup.py install")
	os.system("sudo apt-get install openjdk-8-jdk-headless -y")
	os.system("sudo rm /lib/systemd/system/rotorhazard.service")
	os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("echo '[Unit]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("echo 'Description=RotorHazard Server' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("echo 'After=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("echo '[Service]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("echo 'WorkingDirectory=/home/"+name+"/RotorHazard/src/server' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("echo 'ExecStart=/usr/bin/python server.py' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("echo '[Install]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("echo 'WantedBy=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service")
	os.system("sudo chmod 644 /lib/systemd/system/rotorhazard.service")
	os.system("sudo systemctl daemon-reload")
	os.system("sudo systemctl enable rotorhazard.service")
	print("""\n\n\t
	##############################################\t
	##                                          ##\t
	##         Installation completed!          ##\t
	##                                          ##\t
	##############################################\t""")
	end()

def update():
	os.system("clear")
	if os.path.exists("/home/"+name+"/RotorHazard") == False:
		print("""\n\t Looks like you don't have RotorHazard server software installed for now!!! \n\t\t
	 If so please install your server software first or you won't be able to use the timer. """)
	 	selection=str(raw_input("""\n\n\t\t"""+bcolors.OKGREEN+""" 'i' - Install the software - recommended """+ bcolors.ENDC+
		"""\n\n\t\t 'u' - Force update procedure   \n\n\t\t 'a' - Abort both  \n\n """))
		if selection == 'i':
			installation()
		if selection == 'u':
			update()
		if selection == 'a':
			print("\n\n\t\t\tBye, bye\n\n\t\t")
			sleep(1)
			os.system("clear")
			sys.exit()
		else:
			main()
	else :
		#os.system("sudo killall python *server.py")
		os.system("sudo systemctl stop rotorhazard")
		os.system("clear")
		sleep(0.1)
		print("\n\t\t Updating existing installation - please wait... \n")
		os.system("sudo systemctl stop rotorhazard")
		os.system("sudo pip install pillow")
		os.system("sudo apt-get install libjpeg-dev -y")
		os.system("sudo apt-get update && sudo apt-get upgrade -y")
		os.system("sudo mv /home/"+name+"/RotorHazard.old /home/"+name+"/.old_RotorHazard.old/")
		os.system("sudo mv /home/"+name+"/RotorHazard /home/"+name+"/RotorHazard.old")
		os.chdir("/home/"+name)
		os.system("wget https://codeload.github.com/RotorHazard/RotorHazard/zip/"+version+" -O temp.zip")
		os.system("unzip temp.zip")
		os.system("sudo mv /home/"+name+"/RotorHazard-"+version+" /home/"+name+"/RotorHazard")
		os.system("rm temp.zip")
		os.system("mkdir /home/"+name+"/backup_RH_data")
		os.system("cp /home/"+name+"/RotorHazard.old/src/server/config.json /home/"+name+"/RotorHazard/src/server/")
		os.system("cp -r /home/"+name+"/RotorHazard.old/src/server/static/image /home/"+name+"/backup_RH_data/")
		os.system("cp -a /home/"+name+"/RotorHazard.old/src/server/static/image/ /home/"+name+"/RotorHazard/src/server/static/image/")
		os.system("cp /home/"+name+"/RotorHazard.old/src/server/config.json /home/"+name+"/backup_RH_data")
		os.system("cp /home/"+name+"/RotorHazard.old/src/server/database.db /home/"+name+"/RotorHazard/src/server/")
		os.chdir("/home/"+name+"/RotorHazard/src/server")
		os.system("cp /home/"+name+"/RotorHazard.old/src/server/database.db /home/"+name+"/backup_RH_data")
		os.system("sudo pip install --upgrade --no-cache-dir -r requirements.txt")
		print("""\n\n\t
		##############################################\t
		##                                          ##\t
		##            Update completed!             ##\t
		##                                          ##\t
		##############################################\t""")
		end()

def end():
	print("\n\n\n\t\tType 'r' for reboot - recommended\n")
	print("\t\tType 's' to start the server now\n")
	print("\t\tType 'e' for exit\n")
	def endMenu():
		selection=str(raw_input(""))
		if selection =='r':	
			os.system("sudo reboot")
		if selection =='e':	
			print("\n\n\t\t\tBye, bye\n\n\t\t")
			sleep(1)
			os.system("clear")
			sys.exit()
		if selection =='s':	
			print("\n\n\t\t\tServer will start in few seconds\n\n\t\t")
			sleep(2)
			os.system("clear")
			os.system("python /home/"+name+"/RotorHazard/src/server/server.py")
			sys.exit()
		else: 
			end()
	endMenu()	
	os.system("clear")

def main():
	os.system("clear")
	sleep(0.2)
	print("""\n\n\t\t"""+bcolors.RED+"""AUTOMATIC UPDATE AND INSTALLATION OF ROTORHAZARD RACING TIMER SOFTWARE\n\n\t"""+bcolors.ENDC+"""
	This script will automatically install or update RotorHazard software on your Raspberry Pi. \n\t
	All additional software depedancies and libraries also will be installed or updated.\n\t
	Your current database and config file should stay on the updated software.\n\t
	After rebooting please check by typing 'sudo raspi-config' if I2C, SPI and SSH protocols are active.\n\n\t
	Source will be '"""+bcolors.BLUE+version+bcolors.ENDC+"""' repository of RotorHazard software on github - or version choosen by you.\n\t
	Make sure that you are logged as user '"""+bcolors.BLUE+name+bcolors.ENDC+"""'. \n\n\tYou can change those by oppening this file in text editor - like 'nano'.
	\n\n\n\t\t\t\t\t\t\t\t\tEnjoy!\n\n\t\t
	\t 'i' - Install software from skratch\n\t\t
	\t 'u' - Update existing installation\n\t\t
	\t 'a' - Abort \n""")
	selection=str(raw_input(""))
	if selection =='i':	
		if (os.path.exists("/home/"+name+"/.old_RotorHazard.old/.installation-check_file.txt") == True) or (os.path.exists("/home/"+name+"/RotorHazard") == True):
			os.system("clear")
			print("""\n\t Looks like you already have RotorHazard server software installed. \n
	 If so please use update mode instead. """)
			selection=str(raw_input("""\n\n\t\t"""+bcolors.OKGREEN+""" 'u' - Select update mode - recommended """+ bcolors.ENDC+
			"""\n\n\t\t 'i' - Force installation anyway   \n\n\t\t 'a' - Abort both  \n\n """))
			if selection == 'u':
				update()
			if selection == 'i':
				installation()
			if selection == 'a':
				print("\n\n\t\t\tBye, bye\n\n\t\t")
				sleep(1)
				os.system("clear")
				sys.exit()
			else:
				main()
		else :
			installation()
	if selection =='u':	
		update()
	if selection =='a':	
		os.system("clear")
		print("\n\n")
		image()
		print("\n\t\t\t\t\t\t  Happy flyin'!\n")
		sleep(1.3)
		os.system("clear")
		sys.exit()
	else :
		main()
main()
