# DiscordEventBot

DiscordEventBot is a Python-based Discord bot designed to create and manage scheduled voice channel events on your Discord server. It features an easy-to-use graphical interface to configure event details, time zones, channels, and roles, and automatically posts event announcements with reminders in designated text channels.

---

## Features

- 🗓️ **Create scheduled voice channel events** with custom names, descriptions, start times, and durations  
- 🌍 Supports **time zone management** to schedule events accurately regardless of server location  
- 🔔 Posts event announcements in specified text channels, tagging specific roles if desired  
- 💬 Uses Discord's native scheduled event feature with start and end times  
- 🛠️ Includes a **Tkinter GUI** for easy configuration without editing code  
- 🔄 Checks for updates on GitHub and notifies users when a new version is available  
- 📁 Supports saving configuration settings for reuse  

---

## Requirements

- Python 3.8 or newer  
- `discord.py` library (for Discord bot integration)  
- `requests` library (for update checks)  
- `userpaths` library (for finding user's Documents directory)  
- Access to Discord Developer Portal to create a bot token  
- Proper permissions to manage scheduled events and send messages in your server  

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/rubendommo/DiscordEventBot.git
    ```
2. Change directory:
    ```bash
    cd DiscordEventBot
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *If you don't have a `requirements.txt` file, install manually:*  
    ```bash
    pip install discord.py requests userpaths
    ```

---

## Configuration & Usage

1. Run the application with:
    ```bash
    python botDiscord.py
    ```
2. The GUI window will open. Fill out the following fields:

   - **Event Name**: The name of your scheduled event  
   - **Description**: A description for the event  
   - **TimeZone**: Time zone string (e.g., `Europe/Madrid`) for event scheduling  
   - **Hour & Minute**: Start time of the event (24-hour format)  
   - **Text Channel ID**: Discord text channel ID where the announcement will be posted  
   - **Voice Channel ID**: Discord voice channel ID where the event will take place  
   - **Role ID**: Optional role ID to mention in the announcement  
   - **Bot Token**: Your Discord bot token from Developer Portal  

3. Optionally select "Save" checkboxes to persist these values between runs.  
4. Click **Send** to create and announce the event on your Discord server.  
5. The bot will automatically create a scheduled event, send the announcement, and then exit.  

---

## How It Works

- The bot connects to Discord using the provided token.  
- It finds the specified voice and text channels, and optionally the role to mention.  
- It creates a scheduled event in the voice channel starting at the given time and lasting 2 hours 30 minutes.  
- An announcement is sent in the specified text channel with event details and a clickable link.  
- The bot then disconnects automatically.  

---

## Development & Contribution

Contributions, bug reports, and feature requests are welcome!

To contribute:

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Open a pull request  

Please ensure your code follows PEP8 standards and includes relevant comments.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- Uses [discord.py](https://discordpy.readthedocs.io/)  
- Thanks to the Discord Developer community for event scheduling API support  

---

## Contact

For questions or support, open an issue or contact the repository owner.
