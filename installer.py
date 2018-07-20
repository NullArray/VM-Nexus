#!/usr/bin/env python2.7

"""  
+-----------+------------------------------------------+
|Application: VM-Nexus	    (YAR!)   	 ____          |
|...........:         	        \      ,'   Y`.	       |
|Version....: 1.0.0		  \   /        \       |
|License....: GNU GPL 3            `  \ ()  () /       |
|Author.....: Vector/NullArray         `. /\ ,'        |
|Twitter....: @Real__Vector        8====| "" |====8    |
|...........:                           `LLLU'         |
+-----------+------------------------------------------+
|Now with:	         Automated      	       |	   
|                  Dependency Management               |         
|  Where we're going, we don't need requirements files |
+------------------------------------------------------+
						    """
# Auto PIP
def install(package):
    if not pip_imported == 1:
	from pip._internal import main as pipmain
	pip_imported = 1
    
    pipmain(['install', package])

"""Imports, with automated dependency management"""
import os
import sys
import time
import json
import urllib

from random import random, randint

try:
	import platform as p
except ImportError as e:
	if debug:
		print e

	install(platform)
	import platform as p
	
try:	
	from easygui import *
except ImportError as e:
	if debug:
		print e
	
	install(easygui)
	from easygui import *
	
try:
	from tqdm import trange
except ImportError as e:
	if debug:
		print e
	
	install(tqdm)
	from tqdm import trange

try:	
	from colorama import init
except ImportError as e:
	if debug:
		print e
	
	install(colorama)
	from colorama import init

try:
	from whichcraft import which
except ImportError as e:
	if debug:
		print e
	
	install(whichcraft)
	from whichcraft import which

try:
	from terminaltables import AsciiTable
except ImportError as e:
	if debug:
		print e
	
	install(terminaltables)
	from terminaltables import AsciiTable


"""Supporting Operations"""
# If we're on Windows we have to init Colorama
# to be able to use ANSI color codes
if sys.platform == 'win32' or 'Windows' in p.system():
	init()

# TQDM Class to facilitate functional progress indicator
class TqdmUpTo(tqdm):

	def update_to(self, b=1, bsize=1, tsize=None):
		if tsize is not None:
			self.total = tsize
			self.update(b * bsize - self.n)

# Check if our config file is present
if not os.path.isfile('q_config.json'):
	config = { 'first_run': 'True',
	           'qemu_installed': 'False',
		   'virt-manager_installed':,'False',
		   'GUI_mode': 'off',
		   'architecture': 'null' }
			    
	with open('q_config.json', 'wb') as outfile:
		json.dump(config, outfile)
		outfile.close()
else:
	# Load configuration file
	with open('q_config.json', 'rb') as infile:
		config = json.load(infile)

# ANSI coloring
def text(color, text):
    # Colors
    green   = "\x1b[32;01m" + text + "\x1b[39;49;00m"
    cyan    = "\x1b[33;36m" + text + "\x1b[39;49;00m"
    red     = "\x1b[31;01m" + text + "\x1b[39;49;00m"
    magenta = "\x1b[0;35m"  + text + "\x1b[39;49;00m"
    
    # Background
    green_bg   = "\e[42m" + text + "\x1b[39;49;00m"
    cyan_bg    = "\e[46m" + text + "\x1b[39;49;00m"
    red_bg     = "\e[41m" + text + "\x1b[39;49;00m"
    magenta_bg = "\e[45m" + text + "\x1b[39;49;00m"
    
    # Debug Note
    invalid = """
    \x1b[31;01m[!]\x1b[39;49;00m Invalid argument;
    \x1b[0;35m[*]\x1b[39;49;00mValid color arguments are: 'green', 'cyan', 'magenta' and 'red'.
    \x1b[0;35m[*]\x1b[39;49;00mValid BG color arguments are: 'green_bg', 'cyan_bg', 'magenta_bg' and 'red_bg'. """
    
    if color == 'green':
        return green
    elif color == 'cyan':
        return cyan
    elif color == 'red':
        return red
    elif color == 'green_bg':
        return green_bg
    elif color == 'cyan_bg':
        return cyan_bg
    elif color == 'red_bg':
        return red_bg
    elif color == 'magenta_bg':
        return magenta_bg
    else:
	return invalid

# Banner header
def header():
	print text('cyan', "  _____ _____ __ __ _____ _____  ")
	print text('cyan', " |   | |   __|  |  |  |  |   __| ")
	print text('cyan', " | | | |   __|-   -|  |  |__   | ")
	print text('cyan', " |_|___|_____|__|__|_____|_____| ")
	print text('cyan', " VM-Nexus, VM Management & Utils ")
			  
# Execute/Capture OS commands/output
def cmdline(command):
    process = subprocess.Popen(
    args=command,
    stdout=subprocess.PIPE,
    shell=True)
    
    return process.communicate()[0]

#---UNDER cONSTRUCTION---#
def check_list(): # Replace with array of available VMs?
	if 'False' in config["first_run"] and 'True' in config["qemu_installed"]:
		# VM lists
		# Auto-Downloader


"""Installation Operations"""
def win_downloader(link):
	outfile = link.replace('/', ' ').split()[-1]
	out     = outfile.replace("/dev/null", os.devnull)

	try:
		with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=outfile) as t:
			urllib.urlretrieve(link, filename=out, reporthook=t.update_to, data=None)
	except Exception as e:
		if debug:
			print text("red", "[!]Critical. An error was raised while downloading or writing data.")
			sys.exit(e)
		else:
			print text("red", "[!]Critical. An error was raised while downloading or writing data")
			sys.exit(0)
			
	return outfile

# Installation operations for Windows
def handle_win(arch):
	# Print header
	cmdline('cls')
	header()
	
	print """
Welcome to VM-Nexus, please be patient while we check
our configuration and make sure all of our resources
are in order...\n"""
	if 'False' in config["qemu_installed"] and which('virt-manager') is None:
		print text("cyan", "[?]It seems QEMU is currently not installed\n")
		print "Would you like Nexus to install QEMU and related utilities automatically?"
	
		choice = raw_input("[Y]es/[N]o").lower()
	
		if choice == "y":
			print text("green", "\n[+] Downloading installer for Windows.\n")
			time.sleep(1)
	
			if 'x86_64' or 'AMD64' in arch:
				link = 'https://qemu.weilnetz.de/w64/qemu-w64-setup-20180404.exe'
			else:
				link = 'https://qemu.weilnetz.de/w32/qemu-w32-setup-20180430.exe'
			
			# Call downloader function
			binary = win_downloader(link)	
			print text("green", "\n[+]Done, initializing installer...\n")
		
			home_dir = os.getenv('HOME')
			
			template = "start %s >> %s/VMN-install.log && DEL %s" % (binary, home_dir, binary)
			cmdline(template)
		
			# QEMU installer -> virt-manager(Win version AKA virt-viewer)	
			print text("green", "[+]Done\n")
			time.sleep(2)
		
			print text("green", "[+]QEMU can be used from the CMD line or via a GUI on Windows")
			print text("cyan", "[?]Download and install GUI?")
		
			choice = raw_input("[Y]es(recommended)/[N]o").lower()
		
			if choice == "y":
				print text("green", "\n[+] Downloading virt-viewer for Windows.\n")
				time.sleep(1)
			
			if 'x86_64' or 'AMD64' in arch:
				link = 'https://virt-manager.org/download/sources/virt-viewer/virt-viewer-x64-6.0.msi'
			else:
				link = 'https://virt-manager.org/download/sources/virt-viewer/virt-viewer-x86-6.0.msi'
			
			# Call downloader function
			binary = win_downloader(link)
			
			print text("green", "[+]Done, initializing installer...\n")
			cmdline(template)
				
			print text("green", "[+]Done\n")
			time.sleep(2)
			print text("green", "[+]Updating config.\n")
			time.sleep(2)
		
			# Update the Config file
			config['first_run'] = 'False'
			config['qemu_installed'] = 'True'
			config['architecture'] = arch
		
			try:
				with open('q_config.json', 'wb') as outfile:
					json.dump(config, outfile)
					outfile.close()
			except IOError as e:
				if debug:
					print text("red", "[!]An IO error was raised while trying to write to config.")
					sys.exit(e)
				else:
					print text("red", "[!]Critical. An error was raised while trying to write to config")
					sys.exit(0)
		
			print text("green", "\n[+]Updated config succesfully.")
			time.sleep(2)
		
			# Go to management menu
			# Go to management menu	
			
	elif choice == "n":
		print text("red", "[!]Aborted")
		
		time.sleep(1.5)
		sys.exit(0)
	else:
		print text("red", "[!]Unhandled Option")
		
		time.sleep(1.5)
		sys.exit(0)
		
		

def handle_mac(arch):
	# Print header
	cmdline('clear')
	header()
	
	print """
Welcome to VM-Nexus, please be patient while we check
our configuration and make sure all of our resources
are in order...\n"""
	if 'False' in config["qemu_installed"] and which('virt-manager') is None:
		# Install QEMU and related utilities
		print text("cyan", "[?]It seems QEMU is currently not installed\n")
		print "Would you like VM-Nexus to install QEMU and related utilities automatically?"
	
		choice = raw_input("[Y]es/[N]o").lower()
	
		if choice == "y":
			print text("green", "\n[+] Downloading and installing for Mac.\n")
			time.sleep(1)
			
			if which('brew') is None:
				cmdline("ruby -e '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)' < /dev/null 2> /dev/null | tee -a VMN-Install.log")
			
			cmdline("brew install qemu | tee -a VMN-Install.log")
			
			print text("green", "[+]Done\n")
			time.sleep(2)
			
			print text("green", "[+]QEMU can be used from the terminal or via a GUI on Mac\n")
			print "Please note that the current HomeBrew has some limitations"
			print "For instance, the openssh-askpass dependency is not included" 
			print "Which means a work-around must be employed. In this case adding the"
			print "`--debug` flag when using the CLI to start virt-manager will solve it."
			print
			print "In case you'd like to have a more detailed look at some of these issues please"
			print "Visit the repo at: https://github.com/jeffreywildman/homebrew-virt-manager\n\n"
			time.sleep(2)
			
			print text("cyan", "[?]Download and install GUI anyway?")
			
			choice = raw_input("[Y]es/[N]o").lower()		
				
			if choice == "y":
				print text("green", "\n[+] Downloading and installing 'virt-manager'.\n")
				time.sleep(1)
				
				cmdline("brew tap jeffreywildman/homebrew-virt-manager | tee -a VMN-Install.log")
				cmdline("brew install virt-manager virt-viewer | tee -a VMN-Install.log")
				
				print text("green", "[+]Done\n")
				time.sleep(2)
				print text("green", "[+]Updating config.\n")
				time.sleep(2)
		
				# Update the Config file
				config['first_run'] = 'False'
				config['qemu_installed'] = 'True'
				config['architecture'] = arch
		
				try:
					with open('q_config.json', 'wb') as outfile:
						json.dump(config, outfile)
						outfile.close()
				except IOError as e:
					if debug:
						print text("red", "[!]An IO error was raised while trying to write to config.")
						sys.exit(e)
					else:
						print text("red", "[!]Critical. An error was raised while trying to write to config")
						sys.exit(0)
		
				print text("green", "\n[+]Updated config succesfully.")
				time.sleep(2)
		
				# Go to management menu
				# Go to management menu	
				
			elif choice == "n":
				print text("red", "[!]Aborted")
		
				time.sleep(1.5)
				sys.exit(0)
			else:
				print text("red", "[!]Unhandled Option")
		
				time.sleep(1.5)
				sys.exit(0)
			
def handle_linux(arch):
	# Print header
	cmdline('clear')
	header()
	
	print """
Welcome to VM-Nexus, please be patient while we check
our configuration and make sure all of our resources
are in order...\n"""
	if 'False' in config["qemu_installed"] and which('virt-manager') is None:
		# Install QEMU and related utilities
		print text("cyan", "[?]It seems QEMU is currently not installed\n")
		print "Would you like Nexus to install QEMU and related utilities automatically?"
	
		choice = raw_input("[Y]es/[N]o").lower()
		
		if choice == 'y':
			print text("green", "\n[+] Downloading and installing for Linux.\n")
			time.sleep(1)			
			
			distro = p.uname()
			
			# Ubuntu/Debian
			if 'Ubuntu' or 'Debian' in distro:
				print text("green", "\n[+] Invoking package manager.\n")
				time.sleep(1)
				
				cmdline("sudo apt-get install libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev")
				cmdline("sudo apt-get install qemu-kvm")
				cmdline("sudo apt-get install virt-manager")
			# Fedora	
			elif 'Fedora' in distro:					
				print text("green", "\n[+] Invoking package manager.\n")
				time.sleep(1)
				
				cmdline("sudo yum install glib2-devel libfdt-devel pixman-devel zlib-devel")
				cmdline("sudo dnf install @virtualization")
				cmdline("yum install virt-manager")
			#CentOS
			elif 'CentOS' in distro:
				print text("green", "\n[+] Invoking package manager.\n")
				time.sleep(1)
				
				cmdline("sudo yum install glib2-devel libfdt-devel pixman-devel zlib-devel")
				cmdline("sudo yum install qemu-kvm")
				cmdline("sudo yum install virt-manager")
			# Gentoo
			elif 'Gentoo' in distro:
				print text("green", "\n[+] Invoking package manager.\n")
				time.sleep(1)
				
				cmdline("sudo emerge --ask app-emulation/qemu")
				cmdline("sudo emerge virt-manager")
			else:
				print text("red", "[!]Unfortunately your distro is currently not supported by VM-Nexus"
				print "\nExiting..."
				
				sys.exit(0)
			
			cmdline("clear")
			print text("green", "[+]Done\n")
			time.sleep(2)
			print text("green", "[+]Updating config.\n")
			time.sleep(2)
		
			# Update the Config file
			config['first_run'] = 'False'
			config['qemu_installed'] = 'True'
			config['architecture'] = arch
		
			try:
				with open('q_config.json', 'wb') as outfile:
					json.dump(config, outfile)
					outfile.close()
			except IOError as e:
				if debug:
					print text("red", "[!]An IO error was raised while trying to write to config.")
					sys.exit(e)
				else:
					print text("red", "[!]Critical. An error was raised while trying to write to config")
					sys.exit(0)
		
			print text("green", "\n[+]Updated config succesfully.")
			time.sleep(2)
		
			# Go to management menu	
			# Go to management menu	
			
		elif choice == "n":
			print text("red", "[!]Aborted")
		
			time.sleep(1.5)
			sys.exit(0)
		else:
			print text("red", "[!]Unhandled Option")
		
			time.sleep(1.5)
			sys.exit(0)


if __name__ == '__main__':
	if sys.argv[1:] == "--debug":
		debug = True
		print text("green", "[+]Debug mode on")
	else:
		debug = False
	
	arch = p.architecture()				   
					   
	if sys.platform == 'win32' or "Windows" in p.system():
		# Call appropriate handler
		handle_win(arch)

	elif sys.platform == 'darwin':
		# Call appropriate handler
		handle_mac(arch)

	elif sys.platform == 'linux2':
		# Call appropriate handler
		handle_linux(arch)
