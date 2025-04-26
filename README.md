🛠 Setup Instructions

Requirements
     Python 3.9 or newer
     Pip (Python package manager)
     (Optional) A virtual environment for Python projects

Install Required Python Packages
     Run this command in your terminal or command prompt:
     
     pip install pillow discord.py

Packages explained:
     Pillow: Used for image generation and editing.
     discord.py: For interacting with Discord servers and member roles (if needed).

Clone the Repository

     git clone https://github.com/10thmdhll/uniform-bot uniform-bot

Running the Project
     Run in a Detached Screen Session
          To keep the bot alive after you close your terminal:
          Start a named screen session

     screen -S uniform

Activate venv inside screen

     source uniform-bot/bin/activate

Launch the bot

     python bot.py

Detach from screen
     Press Ctrl-A then D.
     The bot remains running in the background.

Reattach to screen

     screen -r uniform

Stop & close
     Inside the session: Ctrl-C to halt the script, then exit to close screen.

