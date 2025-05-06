# Interactive D&D Table

Bring your D&D sessions to life with dynamic maps, sound effects, and immersive controls.

## 🧙 Overview

This project turns any TV into a living, interactive Dungeons & Dragons map using a Raspberry Pi Zero WH and a custom 10-key controller. It’s designed to enhance immersion without the need for laptops, touchscreens, mouse input, or internet. The DM sets up the campaign using a custom PC program, then transfers / upload it to the Raspberry Pi's SD card.

## 🎯 Features

- 📺 **Live Map Display**: Top-down maps shown on a TV in real-time.
- 🔊 **Sound Effects**: 7 dedicated buttons trigger atmospheric sounds.
- 🎵 **Background Music**: Changes dynamically with the map.

-🔊 9 Buttons – Used for sound effects by default.
-🗺️ Map Switching Mode – Press the Set button, then one of the 9 buttons to switch directly to a corresponding map.
-🎬 1 Set Button – Activates "map select" mode.

Example:
Press Set, then Button 3 → instantly switches to Map 3, with its associated background music and sound theme.

- 🐍 Powered by Raspberry Pi Zero WH (lightweight & portable)

## 🛠️ Components

- Raspberry Pi Zero WH
- HDMI-connected TV or monitor
- Custom-built keypad with 10 mechanical or tactile buttons
- Speaker (for audio output)
- Python scripts (map control, sound playback, etc.)

## 🧩 How It Works

1. The Raspberry Pi displays a top-down map on the TV.
2. The keypad connects via GPIO or USB (depending on your build).
3. Pressing a button triggers sound effects or changes the map.
4. Background music/ sound effects updates automatically based on the current map.



