
# **Anime Wallpaper Changer**

This is a fully AI made project that allows you to change your desktop wallpaper with anime-themed images, automatically fetching high-quality **action, dark, and cyberpunk anime** wallpapers that are **suitable for boys**. It also supports wallpaper preview, history, and allows you to change or revert to previous wallpapers with just a few clicks.

## **Features:**

- Fetches anime wallpapers that match your **screen resolution**.
- Supports **dark-themed**, **action**, **mecha**, and **cyberpunk** anime wallpapers.
- Shows a live **preview** of the wallpaper before setting it.
- Keeps track of the last **3 wallpapers** in history.
- Allows you to **revert to previous wallpapers** with a dropdown selection.
- Simple, modern **UI** with dark mode and rounded buttons.

## **Installation Instructions**

### **Step 1: Install Python Dependencies**

Before running the app, you need to install the required Python packages. You can do this by running the following command in your terminal or command prompt:

```bash
pip install requests pillow customtkinter screeninfo
```

### **Step 2: Run the Python Script**

1. Download or clone this repository.
2. Open your terminal or command prompt.
3. Navigate to the folder containing the Python script.
4. Run the script:

```bash
python wallpaper_changer.py
```

### **Step 3: Set the Script to Run Automatically (Optional)**

If you want the app to start automatically when your PC boots up, follow these steps:

#### **Option 1: Add to Windows Startup Folder**

1. After creating the executable using **PyInstaller**, copy the `.exe` file.
2. Open the **Startup Folder**:
   - Press **Win + R** and type `shell:startup`, then press **Enter**.
3. Create a shortcut of the executable in the **Startup Folder**.

#### **Option 2: Add to Windows Registry**

1. Press **Win + R**, type `regedit`, and press **Enter** to open the **Registry Editor**.
2. Navigate to: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
3. Add a new string with the path to your executable:
   ```plaintext
   "C:\path\to\wallpaper_changer.exe"
   ```

## **Usage Instructions**

1. **Change Wallpaper**: Click on the "Change Wallpaper" button to fetch and apply a random anime wallpaper based on your screen resolution.
2. **Preview**: The current wallpaper will be shown in the preview section of the UI.
3. **History**: The app will store the last 3 wallpapers, and you can select a previous wallpaper from the dropdown menu to revert back.
4. **Revert Wallpaper**: Choose a wallpaper from the dropdown and it will be set as your desktop wallpaper.

---

## **Customization**

- If you want to change the type of wallpapers fetched (e.g., action, mecha, cyberpunk), you can modify the **API URL** in the `API_URL` variable within the code.
- You can also add more wallpapers to your history by modifying the `wallpaper_history` list.

---

## **Contributing**

Feel free to fork the repository, submit issues, and create pull requests for any improvements or new features!

---

## **License**

This project is licensed under the MIT License.

---

This should provide a clear and complete guide for setting up and using the **Anime Wallpaper Changer**. Let me know if you need any further tweaks!