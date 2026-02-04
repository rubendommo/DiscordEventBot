import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import tkinter as tk
from tkinter import messagebox, ttk
import threading, time, json, os, sys, requests, userpaths, zoneinfo

CURRENT_VERSION = "v0.0.1"

GITHUB_OWNER = "rubendommo"
GITHUB_REPO = "DiscordEventBot"


def check_github_update():
    try:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()

        latest_version = data.get("tag_name")
        if latest_version != CURRENT_VERSION:
            # Hay nueva versión
            messagebox.showinfo(
                "Update available",
                f"New version available: {latest_version}\n"
                f"Current version: {CURRENT_VERSION}\n\n"
                "Go Github to download."
            )
    except Exception as e:
        print("Error checking updates:", e)

eventName = ""
description = ""
hour = 0
minute = 0
tokenBot = ""
textChannel = ""
voiceChannel = ""
timeZone = 'Europe/Madrid'
rol = ""

documents_dir = userpaths.get_my_documents()
FOLDER_NAME = os.path.join(documents_dir, "DiscordEventBot")
CONFIG_FILE = os.path.join(FOLDER_NAME, "config.json")

def save_data():
    data = {"flags": {}, "values": {}}

    data["flags"]["save_description"]      = bool(descripcionCheckbox_var.get())
    data["flags"]["save_timezone"]         = bool(timeZoneCheckbox_var.get())
    data["flags"]["save_voicechannel"]     = bool(canalCheckbox_var.get())
    data["flags"]["save_textchannel"]      = bool(canalTextoCheckbox_var.get())
    data["flags"]["save_rol"]              = bool(rolCheckbox_var.get())
    data["flags"]["save_token"]            = bool(tokenCheckbox_var.get())

    if data["flags"]["save_description"]:
        data["values"]["description"] = entry_desc.get()
    if data["flags"]["save_timezone"]:
        data["values"]["timeZone"] = entry_timeZone.get()
    if data["flags"]["save_voicechannel"]:
        data["values"]["voiceChannel"] = canal_entry.get()
    if data["flags"]["save_textchannel"]:
        data["values"]["textChannel"] = canalTexto_entry.get()
    if data["flags"]["save_rol"]:
        data["values"]["rol"] = rol_entry.get()
    if data["flags"]["save_token"]:
        data["values"]["tokenBot"] = token_entry.get()

    if not any(data["flags"].values()):
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        return

    os.makedirs(FOLDER_NAME, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_data():
    if not os.path.exists(CONFIG_FILE):
        return

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    flags  = data.get("flags", {})
    values = data.get("values", {})

    if flags.get("save_description", False):
        entry_desc.delete(0, tk.END)
        entry_desc.insert(0, values.get("description", ""))
        descripcionCheckbox_var.set(1)

    if flags.get("save_timezone", False):
        entry_timeZone.delete(0, tk.END)
        entry_timeZone.insert(0, values.get("timeZone", ""))
        timeZoneCheckbox_var.set(1)

    if flags.get("save_voicechannel", False):
        canal_entry.delete(0, tk.END)
        canal_entry.insert(0, values.get("voiceChannel", ""))
        canalCheckbox_var.set(1)

    if flags.get("save_textchannel", False):
        canalTexto_entry.delete(0, tk.END)
        canalTexto_entry.insert(0, values.get("textChannel", ""))
        canalTextoCheckbox_var.set(1)

    if flags.get("save_rol", False):
        rol_entry.delete(0, tk.END)
        rol_entry.insert(0, values.get("rol", ""))
        rolCheckbox_var.set(1)

    if flags.get("save_token", False):
        token_entry.delete(0, tk.END)
        token_entry.insert(0, values.get("tokenBot", ""))
        tokenCheckbox_var.set(1)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

event_created = False

@bot.event
async def on_ready():
    global event_created, eventName, description, hour, minute, timeZone, voiceChannel, tokenBot, rol, textChannel
    if event_created:
        return

    for guild in bot.guilds:
        guild_voiceChannel = discord.utils.get(guild.voice_channels, id=int(voiceChannel))
        if guild_voiceChannel is None:
            continue

        rolText = ""
        try:
            rol_id = int(rol)
        except ValueError:
            rol_id = None

        if rol_id:
            guild_rol = discord.utils.get(guild.roles, id=rol_id)
            if guild_rol:
                rolText = guild_rol.mention

        existing = await guild.fetch_scheduled_events()
        if any(e.name == eventName for e in existing):
            continue

        timeZoneUTC = zoneinfo.ZoneInfo(timeZone)
        start_time_local = datetime.now(timeZoneUTC).replace(hour=hour, minute=minute, second=0, microsecond=0)
        start_time_utc = start_time_local.astimezone(timezone.utc)

        start = start_time_utc
        end = start + timedelta(hours=2, minutes=30)

        evento = await guild.create_scheduled_event(
            name=eventName,
            start_time=start,
            end_time=end,
            description=description,
            entity_type=discord.EntityType.voice,
            channel=guild_voiceChannel,
            privacy_level=discord.PrivacyLevel.guild_only
        )

        guild_textChannel = discord.utils.get(guild.text_channels, id=int(textChannel))
        if guild_textChannel:
            await guild_textChannel.send(
                f"📅 **NEW EVENT:**\n{evento.name}"
                f"\n🕒 Start: <t:{int(start.timestamp())}:F>\n\n{description}"
                f"\n{rolText}\n\n🔗{evento.url}"
            )

    event_created = True
    await bot.close()

def center_window(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")


def loadingScreen():
    load_win = tk.Toplevel(root)
    load_win.title("Sending...")
    load_win.grab_set()

    label = tk.Label(load_win, text="Sending Event...")
    label.pack(padx=10, pady=10)

    progress = ttk.Progressbar(load_win, mode="indeterminate")
    progress.pack(padx=10, pady=10)
    progress.start(10)

    center_window(load_win)  

    thread = threading.Thread(target=run_task, args=(load_win, progress))
    thread.start()

def endend():
    end_win = tk.Toplevel(root)
    end_win.title("Completed")
    end_win.grab_set()

    label = tk.Label(end_win, text="Completed")
    label.pack(padx=10, pady=10)

    btn_close = tk.Button(end_win, text="Close", command=sys.exit)
    btn_close.pack(padx=10, pady=12)
    center_window(end_win)  


def run_task(win, progress):
    save_data()
    bot.run(tokenBot)
    time.sleep(3)
    progress.stop()
    endend()

def start_bot():
    global eventName, description, hour, minute, timeZone, voiceChannel, tokenBot, rol, textChannel

    eventName = entry_nombre.get()
    description = entry_desc.get()
    timeZone = entry_timeZone.get()
    hour = int(entry_hora.get())
    minute = int(entry_min.get())
    textChannel = canalTexto_entry.get()
    voiceChannel = canal_entry.get()
    rol = rol_entry.get()
    tokenBot = token_entry.get()

    if not eventName:
        messagebox.showerror("Error", "The event name cant be empty.")
        return
    
    loadingScreen()

root = tk.Tk()
root.title("Discord Event Bot")

threading.Thread(target=check_github_update, daemon=True).start()

descripcionCheckbox_var = tk.IntVar()
canalCheckbox_var = tk.IntVar()
canalTextoCheckbox_var = tk.IntVar()
tokenCheckbox_var = tk.IntVar()
timeZoneCheckbox_var = tk.IntVar()
rolCheckbox_var = tk.IntVar()

tk.Label(root, text="Event Name:").grid(row=0, column=0, sticky="e")
entry_nombre = tk.Entry(root, width=30)
entry_nombre.grid(row=0, column=1)

tk.Label(root, text="Description:").grid(row=1, column=0, sticky="e")
entry_desc = tk.Entry(root, width=30)
entry_desc.grid(row=1, column=1)
tk.Checkbutton(root, text="Save", variable=descripcionCheckbox_var).grid(row=1, column=2)

tk.Label(root, text="TimeZone:").grid(row=2, column=0, sticky="e")
entry_timeZone = tk.Entry(root, width=30)
entry_timeZone.grid(row=2, column=1)
tk.Checkbutton(root, text="Save", variable=timeZoneCheckbox_var).grid(row=2, column=2)

tk.Label(root, text="Hour (0–23):").grid(row=3, column=0, sticky="e")
entry_hora = tk.Entry(root, width=5)
entry_hora.grid(row=3, column=1, sticky="w")

tk.Label(root, text="Minute (0–59):").grid(row=4, column=0, sticky="e")
entry_min = tk.Entry(root, width=5)
entry_min.grid(row=4, column=1, sticky="w")

tk.Label(root, text="Text Channel ID:").grid(row=5, column=0, sticky="e")
canalTexto_entry = tk.Entry(root, width=45)
canalTexto_entry.grid(row=5, column=1)
tk.Checkbutton(root, text="Save", variable=canalTextoCheckbox_var).grid(row=5, column=2)

tk.Label(root, text="Voice Channel ID:").grid(row=6, column=0, sticky="e")
canal_entry = tk.Entry(root, width=45)
canal_entry.grid(row=6, column=1)
tk.Checkbutton(root, text="Save", variable=canalCheckbox_var).grid(row=6, column=2)

tk.Label(root, text="Role ID:").grid(row=7, column=0, sticky="e")
rol_entry = tk.Entry(root, width=45)
rol_entry.grid(row=7, column=1)
tk.Checkbutton(root, text="Save", variable=rolCheckbox_var).grid(row=7, column=2)

tk.Label(root, text="Bot Token:").grid(row=8, column=0, sticky="e")
token_entry = tk.Entry(root, width=45)
token_entry.grid(row=8, column=1)
tk.Checkbutton(root, text="Save", variable=tokenCheckbox_var).grid(row=8, column=2)

tk.Button(root, text="Send", command=start_bot).grid(row=9, column=0, columnspan=3, pady=10)

tk.Label(root, text=CURRENT_VERSION).grid(row=10, column=3, sticky="e")

center_window(root)  

load_data()

root.mainloop()
