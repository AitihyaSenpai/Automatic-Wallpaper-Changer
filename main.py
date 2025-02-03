import os
import random
import requests
import ctypes
import customtkinter as ctk
from tkinter import filedialog
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
selected_wallpaper = None  # Stores the wallpaper to confirm

def load_existing_wallpapers():
    """Load previously downloaded wallpapers from the folder and add them to history."""
    global wallpaper_history
    image_files = [os.path.join(WALLPAPER_FOLDER, f) for f in os.listdir(WALLPAPER_FOLDER) if f.endswith((".jpg", ".png", ".jpeg"))]
    wallpaper_history = sorted(image_files, key=os.path.getctime, reverse=True)[:10]  # Keep only last 10 files

    # Update dropdown menu
    history_dropdown.configure(values=wallpaper_history)
    if wallpaper_history:
        history_dropdown.set(wallpaper_history[0])  # Default to the latest one

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

def prepare_new_wallpaper():
    """Download a new wallpaper and preview it (without applying it yet)."""
    global selected_wallpaper
    wallpaper_path = download_wallpaper()
    if wallpaper_path:
        selected_wallpaper = wallpaper_path
        update_preview(wallpaper_path)

def upload_wallpaper():
    """Upload a wallpaper from the device and preview it."""
    global selected_wallpaper
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        selected_wallpaper = file_path
        update_preview(file_path)

def confirm_wallpaper():
    """Apply the selected wallpaper from preview."""
    global selected_wallpaper
    if selected_wallpaper:
        set_wallpaper(selected_wallpaper)
        update_history(selected_wallpaper)

def set_wallpaper(image_path):
    """Set a given image as the desktop wallpaper."""
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)

def update_preview(image_path):
    """Update the preview section with the selected wallpaper."""
    img = Image.open(image_path)
    img.thumbnail((250, 250))  # Resize for preview
    img = ImageTk.PhotoImage(img)
    preview_label.configure(image=img)
    preview_label.image = img

def update_history(image_path):
    """Store wallpaper history and update the dropdown menu."""
    if image_path not in wallpaper_history:
        if len(wallpaper_history) >= 10:
            wallpaper_history.pop(0)  # Remove oldest entry
        wallpaper_history.append(image_path)

    # Update dropdown menu
    history_dropdown.configure(values=wallpaper_history)
    history_dropdown.set(image_path)

def preview_from_dropdown(choice):
    """Preview a wallpaper from the dropdown before applying it."""
    global selected_wallpaper
    selected_wallpaper = choice
    update_preview(choice)

# UI setup
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Anime Wallpaper Changer")
app.geometry("400x600")
app.resizable(False, False)

# Title
title_label = ctk.CTkLabel(app, text="Anime Wallpaper Changer", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Preview Section
preview_label = ctk.CTkLabel(app, text="", width=250, height=250, fg_color="gray", corner_radius=10)
preview_label.pack(pady=10)

# Button Frame (Side by Side)
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=5)

# Change Wallpaper Button
change_btn = ctk.CTkButton(button_frame, text="Search", command=prepare_new_wallpaper, font=("Arial", 14), corner_radius=20)
change_btn.grid(row=0, column=0, padx=10)

# Upload Wallpaper Button
upload_btn = ctk.CTkButton(button_frame, text="Upload", command=upload_wallpaper, font=("Arial", 14), corner_radius=20)
upload_btn.grid(row=0, column=1, padx=10)

# History Dropdown
history_dropdown = ctk.CTkComboBox(app, values=[], command=preview_from_dropdown)
history_dropdown.pack(pady=10)

# Confirm Wallpaper Button
confirm_btn = ctk.CTkButton(app, text="Set Wallpaper", command=confirm_wallpaper, font=("Arial", 14), fg_color="green", corner_radius=20)
confirm_btn.pack(pady=10)

# Load existing wallpapers
load_existing_wallpapers()

# Run App
app.mainloop()
