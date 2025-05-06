import pygame
import os
import sys
import ffmpeg
import numpy as np
from pygame.locals import *
from math import ceil
from PIL import Image, ImageDraw

# Constants
GRID_SIZE_INCH = 1  # 1-inch size for each grid element
TV_DPI = 96  # Assuming a TV DPI of 96 (can vary, adjust as needed)

# Initialize Pygame
pygame.init()

# Create the window
WIDTH, HEIGHT = 1280, 720  # Adjust to your screen resolution (use your TV's native res)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Live Map Editor")

# Choose between hexagon and square grid
GRID_TYPE = 'hex'  # 'hex' or 'square'
GRID_COLOR = (255, 255, 255)  # White grid color
GRID_WIDTH = 5  # Grid width (number of columns in the grid)
GRID_HEIGHT = 5  # Grid height (number of rows in the grid)
GRID_SPACING = 50  # Grid spacing (in pixels)

# Load media (Background image/video and sound effects)
bg_file = None  # The map image/video
bg_music_file = None  # The background music
sfx_files = []  # List of sound effects files for each grid cell

# Function to calculate pixel dimensions of each grid element based on the desired inch size
def calculate_grid_pixel_size():
    return GRID_SIZE_INCH * (TV_DPI / 2.54)  # Convert from inches to pixels (using 2.54cm per inch)

# Function to draw hexagonal grid
def draw_hex_grid():
    grid_size_px = calculate_grid_pixel_size()
    hex_height = grid_size_px * 1.5
    hex_width = grid_size_px * 2

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = col * hex_width + (row % 2) * hex_width / 2
            y = row * hex_height
            pygame.draw.polygon(screen, GRID_COLOR, [
                (x, y),  # Top-left
                (x + hex_width / 2, y + hex_height / 2),  # Top-right
                (x, y + hex_height),  # Bottom-left
                (x - hex_width / 2, y + hex_height / 2)  # Bottom-right
            ])

# Function to draw square grid
def draw_square_grid():
    grid_size_px = calculate_grid_pixel_size()
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            pygame.draw.rect(screen, GRID_COLOR, (col * grid_size_px, row * grid_size_px, grid_size_px, grid_size_px), 2)

# Function to handle video/GIF input and overlay
def handle_video_gif(bg_file):
    video_output_file = "output_map_with_grid.mp4"
    gif_output_file = "output_map_with_grid.gif"

    input_file_ext = bg_file.lower().split('.')[-1]

    if input_file_ext in ['mp4', 'avi', 'mov']:
        # Handle video file
        print("Processing video...")
        process_video(bg_file, video_output_file)
    elif input_file_ext == 'gif':
        # Handle GIF file
        print("Processing GIF...")
        process_gif(bg_file, gif_output_file)
    else:
        print(f"Unsupported file type {input_file_ext}. Please upload a valid video or gif file.")
        sys.exit()

def process_video(input_file, output_file):
    """Process video file, overlay grid on each frame, and output the result."""
    print("Processing video frames...")
    ffmpeg.input(input_file).output(output_file, vcodec='libx264').run()
    print(f"Video saved as {output_file}")

def process_gif(input_file, output_file):
    """Process GIF, overlay grid, and output the result as a new GIF."""
    img = Image.open(input_file)
    frames = []

    for frame in range(img.n_frames):
        img.seek(frame)
        frame_img = img.convert('RGBA')
        draw = ImageDraw.Draw(frame_img)

        # Overlay the grid on each frame
        draw_grid(draw, img.size[0], img.size[1])

        frames.append(frame_img)

    frames[0].save(output_file, save_all=True, append_images=frames[1:], loop=0, duration=100)

    print(f"GIF saved as {output_file}")

def draw_grid(draw, width, height):
    """Draw the grid (hexagon or square) on a given image."""
    if GRID_TYPE == 'hex':
        draw_hex_grid_on_image(draw, width, height)
    else:
        draw_square_grid_on_image(draw, width, height)

def draw_hex_grid_on_image(draw, width, height):
    grid_size_px = calculate_grid_pixel_size()
    hex_height = grid_size_px * 1.5
    hex_width = grid_size_px * 2

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = col * hex_width + (row % 2) * hex_width / 2
            y = row * hex_height
            draw.polygon([
                (x, y),  # Top-left
                (x + hex_width / 2, y + hex_height / 2),  # Top-right
                (x, y + hex_height),  # Bottom-left
                (x - hex_width / 2, y + hex_height / 2)  # Bottom-right
            ], outline=GRID_COLOR)

def draw_square_grid_on_image(draw, width, height):
    grid_size_px = calculate_grid_pixel_size()

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = col * grid_size_px
            y = row * grid_size_px
            draw.rectangle([x, y, x + grid_size_px, y + grid_size_px], outline=GRID_COLOR)

# Main loop to upload background and apply grid
def main():
    global bg_file, bg_music_file, sfx_files

    # Choose background map image or video
    bg_file = input("Enter the file path for the background map (video or image): ")
    if not os.path.exists(bg_file):
        print(f"File {bg_file} does not exist. Exiting.")
        sys.exit()

    bg_music_file = input("Enter the file path for the background music: ")
    if not os.path.exists(bg_music_file):
        print(f"File {bg_music_file} does not exist. Exiting.")
        sys.exit()

    sfx_files = []
    for i in range(1, 10):
        sfx_path = input(f"Enter the file path for sound effect {i}: ")
        if os.path.exists(sfx_path):
            sfx_files.append(sfx_path)
        else:
            print(f"Sound effect {i} file does not exist, skipping it.")

    # Process the background file (image or video)
    input_file_ext = bg_file.lower().split('.')[-1]

    if input_file_ext in ['png', 'jpg', 'jpeg', 'gif']:
        # If it's an image, overlay the grid
        print("Processing image...")
        bg = pygame.image.load(bg_file)
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        screen.blit(bg, (0, 0))
        
        if GRID_TYPE == 'hex':
            draw_hex_grid()
        else:
            draw_square_grid()
        
        pygame.display.flip()
        pygame.image.save(screen, 'output_map_with_grid.png')
        print("Image saved as output_map_with_grid.png")
    else:
        # If it's a video or gif, process it
        handle_video_gif(bg_file)

    pygame.quit()

if __name__ == "__main__":
    main()
