import pygame
from time import *
from tkinter import *
from tkinter import filedialog
import threading
import RPi.GPIO as GPIO
import sys


root = Tk()
root.title('Julian SPA Test')
root.geometry ("800x500")
pygame.mixer.init()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(40, GPIO.OUT)
pwm_pin40 = GPIO.PWM(40,1000)
pwm_pin40.start(0)
sw_led1 = 37
GPIO.setup(sw_led1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
volup = 29
voldown = 31
play_pause = 36
GPIO.setup(volup,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(voldown,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(play_pause,GPIO.IN,pull_up_down=GPIO.PUD_UP)

play = 0
disable = 0
val = 0.5
vol_disable = 0	
a = 0
m_led = 100
disable_led = 1


def play_or_pause():
	#song = song_box.get(ACTIVE)
	#song = f'/home/Document/audio/{song}.mp3'
	#pygame.mixer.music.load(song)
	#pygame.mixer.music.play(loops=0)	
	while(True):
		if GPIO.input(play_pause)==0 and (disable)==0:
			globals()['play'] = play + 1
			print("Play Value", play)
			sleep(1)
			
			if (play)>1 and (disable)==0:
				globals()['play'] = 0	
							
def mp3():	
	
	while(True):
		if (play)==1:
			pygame.mixer.music.unpause()
			print("music play")
			sleep (1)
			break
			
	while(True):		
		if (play)==0:
			pygame.mixer.music.pause()
			print("music pause")
			mp3()
			sleep(1)	
	
def volumes():
	
	while(True):
		val = globals()['val']
		pygame.mixer.music.set_volume(val)
		
		if (val)>1:
			pygame.mixer.music.set_volume(1)
			globals()['val'] = 1
			
		if (val)<0:
			globals()['val'] = 0
		
def vol_read():
	
	while(vol_disable)==0:
		val = globals()['val']
		#pygame.mixer.music.set_volume(val)
		
		if GPIO.input(volup)==0:
			globals()['val'] = val + 0.1
			print("volume Value", val)
			sleep(0.5)
			
		if GPIO.input(voldown)==0:
			globals()['val'] = val - 0.1
			print("volume Value", val)
			sleep(0.5)		


def volup_btn():
	print("Master Volume UP")	
	globals()['val'] = globals()['val'] + 0.1
	
def voldown_btn():
	print("Master Volume Down")
	globals()['val'] = globals()['val'] - 0.1		
				
def add_song():
	song = filedialog.askopenfile(initialdir='audio/', title="Chooso a Song", filetypes=(('mp3 Files', '*mp3'),))
	#song = song.replace("", "")
	#song = song.replace(".mp3", "")
	song_box.insert(END, song)
	pass
		
def led_bttn():
	if (disable_led)==1:		
		print("Master LED ctrl pressed")
		sleep(0.5)	
		led_opr_thread = threading.Thread(target = led_opr)
		led_opr_thread.start()
	else:
		print("LED Button Disabled")
	
def led_opr():	
	if (a)>=1:	
		print("current led", a)	
		for dc in range(m_led, 0, -5):
			pwm_pin40.ChangeDutyCycle(dc)
			globals()['disable_led'] = 0
			sleep(1)
		pwm_pin40.ChangeDutyCycle(0)
		globals()['disable_led'] = 1
		sleep(0.5)		
		globals()['a'] = 0
		print("LED off")
	else:		
		print("current led", a)		
		for dc in range(0, m_led, 5):
			pwm_pin40.ChangeDutyCycle(dc)
			globals()['disable_led'] = 0
			sleep(1)
		pwm_pin40.ChangeDutyCycle(m_led)
		globals()['disable_led'] = 1	
		sleep(0.5)		
		globals()['a'] = 1
		print("LED on")
		
def led_ctrl():
		
	while(True):		
				
		if GPIO.input(sw_led1)==0 and (disable_led)==1:				
			print("Tank Led Controll pressed..!")
			led_bttn()
			sleep(1)
		elif GPIO.input(sw_led1)==0 and (disable_led)==0:
			print("Led Button Disabled")
			sleep(1)


def pause_ovrd():
	print("pause override pressed")	
	globals()['play'] = 0
def play_ovrd():
	print("play override pressed")
	
	if (play)==1:
		print("already play")	
	else:					
		globals()['play'] = 1	
	
	
def timer_sesion():
	timer_sesion_active = 0
	timer = 0
	for x in range(0, 90, 1):
		timer = timer + 1
		print("Session Timer..!", timer)
		sleep(1)
		
	if (timer)==90:
		print("Times UP..!", timer)
		print("Sesion finish prepare for end session in 5 second..!")
		sleep(5)
		print("Stop Music and disable manual controller in 5 sec")
		sleep(5)
		pygame.mixer.music.stop()					
		print("Music Stopped controller disabled")			
		globals()['vol_disable'] = 1
		sleep(5)
		print("Jump to End session")		
		p2 = threading.Thread(target = end_sesion)
		p2.start()
			
def timer_end_sesion():
	timer = 0
	while(True):		
		for x in range(0, 60, 1):
			timer = timer + 1
			print("END Session Timer..!", timer)
			sleep(1)
			
		
		if (timer)==60:
			print("End Sesion Finish..!", timer)
			print("Disable led switch in 5 second..!")
			sleep(5)
			print("Ramp UP Led in 5 sec")
			sleep(5)
			if (a)==0:
				led_opr_thread = threading.Thread(target = led_opr)
				led_opr_thread.start()
			else:
				print("LED already ON")							
			print("Stop End Session music in 5 sec")
			sleep(5)
			pygame.mixer.music.stop()					
			print("Announcement 1 in 5 Second")
			sleep(5)
			print("Announcement 2 in 5 Second")	
			sleep(5)
			print("Power the Pump 1 in 5 Second")
			sleep(5)
			print("Power The Pump 2 in 5 Second")
			sleep(5)
			print("Start the Exhaust Fan in 5 Second")
			sleep(5)
			print("Finalize End Session Procedure")	
			sleep(5)
			#pwm_pin40.ChangeDutyCycle(65)
			print("1 session cycle finished getting Ready for next round Session")
			print("Reset All Parameter in 5 Second")
			sleep(5)
			globals()['disable'] = 0						
			globals()['play'] = 0
			globals()['vol_disable'] = 0
			sleep(5)
			print ("Power off led at the end of session cycle")
			globals()['a'] = 0
			print("Done.. waiting until next scheduled hour")
			pwm_pin40.ChangeDutyCycle(0)
			pygame.mixer.music.load("audio/test.mp3")
			pygame.mixer.music.play(loops=10)
			pygame.mixer.music.pause()
			globals()['val'] = 0.5
			vol_read_thread = threading.Thread(target = vol_read)
			vol_read_thread.start()			
			break
			
def gen_float(start, stop, step):
	x = start
	while x <= stop:
		yield x
		x = x + step
		
rf = gen_float(0, 0.5, 0.02)
			
def end_sesion():
	print("End Session Started..!")
	print("Check Controller button..")
	globals()['disable']=1
	globals()['vol_disable']=1
	print("Button Disabled..!")
	sleep(5)
	print("Prepare The MP3 for End Session")
	sleep(5)
	print("Done.. lets play the music")
	pygame.mixer.music.load("audio/end.mp3")
	pygame.mixer.music.play(loops=0)
	pygame.mixer.music.set_volume(0)
	globals()['val'] = 0
	#gen_float()
	global rf
	rf = gen_float(0, 0.5, 0.02)
	for i in rf:
		pygame.mixer.music.set_volume(i)
		globals()['val'] = i
		sleep(1)	
	print("Start The end Sesion Countdown")
	timer_end_sesion()
	
pygame.mixer.music.load("audio/test.mp3")
pygame.mixer.music.play(loops=10)
pygame.mixer.music.pause()
pygame.mixer.music.set_volume(0.5)

#end_sesion()		
def start_sesion():
	timer_sesion_thread = threading.Thread(target = timer_sesion)
	led_opr_thread = threading.Thread(target = led_opr)	
	print("Session Started..!")
	#print("Music Ready and Paused")
	print("countdown will start in 5 sec")
	globals()['a'] = 0
	globals()['m_led'] = 100
	led_opr_thread.start()	
	sleep(5)
	timer_sesion_thread.start()
	##led_bttn()
	

	

# playlist box
song_box = Listbox(root, bg="black", fg="white", width=60, selectbackground="green")
song_box.pack(pady=20)	

# frame control
control_frame = Frame(root)
control_frame.pack()

#Start session
my_button = Button(root, text="Start Session", font=("Helvetica", 32), command=start_sesion)
my_button.pack(pady=20)

#LED Button
led_button = Button(root, text="LED", font=("Helvetica", 12), command=led_bttn)
led_button.pack(pady=20)

# control button
volup_btn = Button(control_frame, text="Vol +", borderwidth=0, command=volup_btn)
voldown_btn = Button(control_frame, text="Vol -", borderwidth=0, command=voldown_btn)
play_btn = Button(control_frame, text="Play", borderwidth=0, command=play_ovrd)
stop_btn = Button(control_frame, text="Pause", borderwidth=0, command=pause_ovrd)


volup_btn.grid(row=0, column=0)
voldown_btn.grid(row=0, column=1)
play_btn.grid(row=0, column=2)
stop_btn.grid(row=0, column=3, pady=20)

# menu

my_menu = Menu(root)
root.config(menu=my_menu)

# add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="add one to playlist", command=add_song)
			
play_or_pause_thread = threading.Thread(target = play_or_pause)
play_or_pause_thread.start()

mp3_thread = threading.Thread(target = mp3)
mp3_thread.start()	

start_sesion_thread = threading.Thread(target = start_sesion)
#start_sesion_thread.start()		

vol_read_thread = threading.Thread(target = vol_read)
vol_read_thread.start()	
volumes_thread = threading.Thread(target = volumes)
volumes_thread.start()	

##short debug
		
#end_sesion()
#led_ctrl_thread = threading.Thread(target = led_ctrl)
#led_ctrl_thread.start()	


root.mainloop()

