import os
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
sfx_channel = pygame.mixer.Channel(1)

def play_video(path):
    """Play the map video on loop."""
    global video_proc
    if video_proc:
        video_proc.kill()  # Stop any currently playing video
    if not os.path.exists(path):
        print(f"Video file not found: {path}")
        return
    try:
        video_proc = subprocess.Popen(['omxplayer', '--loop', '--no-osd', path])
    except Exception as exc:
        print(f"Failed to play video {path}: {exc}")

def load_set(set_num):
    """Load the map and audio set, and start the media."""
    global CURRENT_SET
    CURRENT_SET = set_num

    # Play the video
    play_video(f'sets/set{set_num}/map.mp4')

    # Start the background music
    bgm_path = f'sets/set{set_num}/bgm.mp3'
    if os.path.exists(bgm_path):
        try:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)  # Loop the background music indefinitely
        except pygame.error as exc:
            print(f"Failed to load background music {bgm_path}: {exc}")
    else:
        print(f"Background music file not found: {bgm_path}")

    # Load sound effects for this set
    load_sfx(set_num)

def load_sfx(set_num):
    """Preload sound effects for the given set."""
    global sfx_library
    sfx_library.clear()
    for i in range(1, 10):
        path = f'sets/set{set_num}/sfx{i}.wav'
        if os.path.exists(path):
            try:
                sfx_library[i] = pygame.mixer.Sound(path)
            except pygame.error as exc:
                print(f"Failed to load sound effect {path}: {exc}")
        else:
            print(f"Sound effect file not found: {path}")

def play_sfx(button_num):
    """Play the sound effect and duck the background music."""
    pygame.mixer.music.set_volume(0.3)  # Duck the music
    sfx = sfx_library.get(button_num)
    if sfx:
        sfx_channel.play(sfx)
        while sfx_channel.get_busy():  # Wait for the sound to finish
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
