import os
import random
import requests
import ctypes
import customtkinter as ctk
from PIL import Image, ImageTk
from io import BytesIO
import screeninfo  # To get screen resolution

# Get screen resolution
screen = screeninfo.get_monitors()[0]
SCREEN_WIDTH = screen.width
SCREEN_HEIGHT = screen.height

# Folder to save wallpapers
WALLPAPER_FOLDER = os.path.expanduser("~") + "/AnimeWallpapers"
os.makedirs(WALLPAPER_FOLDER, exist_ok=True)

# Wallhaven API - Fetch wallpapers that match screen resolution
API_URL = f"https://wallhaven.cc/api/v1/search?q=anime&categories=111&purity=110&resolutions={SCREEN_WIDTH}x{SCREEN_HEIGHT}&sorting=random"

# Initialize history
wallpaper_history = []

def download_wallpaper():
    """Fetch a random wallpaper that matches the screen resolution."""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                image_url = random.choice(data["data"])["path"]  # Get random wallpaper
                
                img_data = requests.get(image_url).content
                
                # Save image locally
                image_name = f"anime_wallpaper_{random.randint(1000, 9999)}.jpg"
                image_path = os.path.join(WALLPAPER_FOLDER, image_name)
                with open(image_path, "wb") as file:
                    file.write(img_data)
                
                return image_path
            else:
                raise Exception("No wallpapers found")
        else:
            raise Exception("Failed to fetch wallpapers")
    except Exception as e:
        ctk.CTkMessagebox(title="Error", message=f"Could not download wallpaper: {e}", icon="cancel")
        return None

def change_wallpaper():
    """Download a new wallpaper and set it as desktop background."""
    wallpaper_path = download_wallpaper()
    if wallpaper_path:
        set_wallpaper(wallpaper_path)
        update_history(wallpaper_path)

def set_wallpaper(image_path):
    """Set a given image as the desktop wallpaper."""
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
    update_preview(image_path)

def update_preview(image_path):
    """Update the preview section with the new wallpaper."""
    img = Image.open(image_path)
    img.thumbnail((250, 250))  # Resize for preview
    img = ImageTk.PhotoImage(img)
    preview_label.configure(image=img)
    preview_label.image = img

def update_history(image_path):
    """Store wallpaper history and update the dropdown menu."""
    if image_path not in wallpaper_history:
        if len(wallpaper_history) >= 3:
            wallpaper_history.pop(0)  # Remove oldest entry
        wallpaper_history.append(image_path)

    # Update dropdown menu
    history_dropdown.configure(values=wallpaper_history)
    history_dropdown.set(image_path)

def revert_wallpaper(choice):
    """Revert to a previously used wallpaper."""
    set_wallpaper(choice)

# UI setup
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Anime Wallpaper Changer")
app.geometry("400x550")
app.resizable(False, False)

# Title
title_label = ctk.CTkLabel(app, text="Anime Wallpaper Changer", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Preview Section
preview_label = ctk.CTkLabel(app, text="Preview", width=250, height=250, fg_color="gray", corner_radius=10)
preview_label.pack(pady=10)

# Change Wallpaper Button
change_btn = ctk.CTkButton(app, text="Change Wallpaper", command=change_wallpaper, font=("Arial", 14), corner_radius=20)
change_btn.pack(pady=10)

# History Dropdown
history_dropdown = ctk.CTkComboBox(app, values=[], command=revert_wallpaper)
history_dropdown.pack(pady=10)

# Run App
app.mainloop()
