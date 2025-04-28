# Uniform Bot README

## Overview
Uniform Bot is a Python-based Discord bot designed to dynamically generate World War II era U.S. Army uniform images. It uses Discord roles to determine rank and ribbons and composites them over a background or silhouette.

Built using:
- **Python 3.12**
- **discord.py**
- **Pillow (PIL)**

---

## Features
- Build dynamic ribbon racks based on user roles
- Correctly arrange ribbons from right-to-left and bottom-up
- Place ranks (e.g., Private First Class to Colonel) on uniforms
- Position the ribbon rack relative to a specific point on a background image
- Generate period-accurate WWII rank patches and technician badges
- Supports scaling and positioning without stretching images improperly

---

## Setup

### Prerequisites
- Python 3.12+
- A Discord bot token

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/10thmdhll/uniform-bot.git
    cd uniform-bot
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install discord.py Pillow aiohttp python-dotenv
    ```

### Configuration
Create a `.env` file or configure your bot token securely:
  ```
  cp default.env .env
  ```
Set the DISCORD_TOKEN=your_token_here line in the new .env file
  ```
  vi .env
  ```
Make sure your bot has permission to read roles, message history and send messages/files/images in your discord server.

---

## Key Files
- **bot.py**: Main bot script handling events and commands.
- **ranks/**: Directory containing rank patch images (e.g., PFC, CPL, SSGT, etc.)
- **awards/**: Directory containing ribbon images used to build the jacket.
---

## Usage

### Commands
- `/uniform` - Generates a complete uniform image based on the user's roles.

### Role-Image Mapping
Role names must exactly match or map to the entries defined in `rank_templates` dictionary. Special handling is included for ranks such as:
- `S/Sgt.` for Staff Sergeant
- `T/5` for Technician 5th Grade
- `T/4` for Technician 4th Grade
- `T/3` for Technician 3rd Grade

If you have special characters (like `/`) in role names, they are automatically handled internally.
All mapping is currently handled in the top section of the bot.py file.
The discord roles must match exactly to your server to be able to display the corresponding image.
---

## Development Notes
- Ribbon racks are generated to always fill the bottom row first (with 3 ribbons max per row).
- Images are placed and resized carefully to avoid distortion.
- Ribbons are arranged right-to-left, bottom-to-top to match official military standards.

---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License
MIT License. See `LICENSE` file for more details.

---
