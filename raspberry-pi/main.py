import RPi.GPIO as GPIO
import pygame
import subprocess
from time import sleep

# Constants
SET_BUTTON = 0
SFX_BUTTONS = list(range(1, 10))
CURRENT_SET = 1

# Setup GPIO
GPIO.setmode(GPIO.BCM)
BUTTON_PINS = {0: 17, 1: 27, 2: 22, 3: 5, 4: 6, 5: 13, 6: 19, 7: 26, 8: 21, 9: 20}  # Update with correct GPIO pins
for pin in BUTTON_PINS.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize pygame for audio and handling sound effects
pygame.mixer.init()

# Media management
video_proc = None
sfx_library = {}

def play_video(path):
    """Play the map video on loop."""
    global video_proc
    if video_proc:
        video_proc.kill()  # Stop any currently playing video
    video_proc = subprocess.Popen(['omxplayer', '--loop', '--no-osd', path])

def load_set(set_num):
    """Load the map and audio set, and start the media."""
    global CURRENT_SET
    CURRENT_SET = set_num

    # Play the video
    play_video(f'sets/set{set_num}/map.mp4')

    # Start the background music
    pygame.mixer.music.load(f'sets/set{set_num}/bgm.mp3')
    pygame.mixer.music.play(-1)  # Loop the background music indefinitely

    # Load sound effects for this set
    load_sfx(set_num)

def load_sfx(set_num):
    """Preload sound effects for the given set."""
    global sfx_library
    sfx_library.clear()
    for i in range(1, 10):
        sfx_library[i] = pygame.mixer.Sound(f'sets/set{set_num}/sfx{i}.wav')

def play_sfx(button_num):
    """Play the sound effect and duck the background music."""
    pygame.mixer.music.set_volume(0.3)  # Duck the music
    sfx = sfx_library.get(button_num)
    if sfx:
        sfx.play()
        while pygame.mixer.get_busy():  # Wait for the sound to finish
            sleep(0.1)
    pygame.mixer.music.set_volume(1.0)  # Restore music volume

# Button press handling
set_mode = False

def button_callback(channel):
    """Handle button presses."""
    global set_mode
    btn = [k for k, v in BUTTON_PINS.items() if v == channel][0]

    if btn == SET_BUTTON:
        set_mode = True
    elif btn in SFX_BUTTONS:
        if set_mode:
            load_set(btn)  # Switch to the selected map and audio set
            set_mode = False  # Return to normal mode
        else:
            play_sfx(btn)  # Play sound effect

# Register button presses
for pin in BUTTON_PINS.values():
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

# Main loop
try:
    while True:
        sleep(1)  # Keep the program running and responsive to button presses
except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on exit
