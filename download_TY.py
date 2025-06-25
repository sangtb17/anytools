import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import platform

def select_folder():
    folder = filedialog.askdirectory()
    save_folder.set(folder)

def is_tiktok_url(url):
    return "tiktok.com" in url.lower()

def update_status(text, color):
    status_label.config(text=text, fg=color)
    root.update_idletasks()

def download_video():
    url = video_link.get().strip()
    folder = save_folder.get().strip()
    quality = quality_choice.get().strip()
    if not url or not folder:
        update_status("Please input link video and select save folder.", "red")
        return

    update_status("Downloading video...", "blue")

    if is_tiktok_url(url):
        cmd = [
            "yt-dlp",
            url,
            "-o", os.path.join(folder, "%(title)s.%(ext)s")
        ]
    else:
        if quality == "480p":
            format_string = "bestvideo[height=480]+bestaudio/best[height=480]"
        elif quality == "720p":
            format_string = "bestvideo[height=720]+bestaudio/best[height=720]"
        elif quality == "1080p":
            format_string = "bestvideo[height=1080]+bestaudio/best[height=1080]"
        else:
            format_string = "best"

        cmd = [
            "yt-dlp",
            "-f", format_string,
            url,
            "-o", os.path.join(folder, "%(title)s.%(ext)s")
        ]
    root.after(100, lambda: run_command(cmd, "Video download completed"))

def download_channel():
    url = channel_link.get().strip()
    folder = save_folder.get().strip()
    quality = quality_choice.get().strip()
    if not url or not folder:
        update_status("Please input link channel and select save folder.", "red")
        return

    update_status("Downloading channel...", "blue")

    if is_tiktok_url(url):
        cmd = [
            "yt-dlp",
            "--yes-playlist",
            url,
            "-o", os.path.join(folder, "%(title)s.%(ext)s")
        ]
    else:
        if quality == "480p":
            format_string = "bestvideo[height=480]+bestaudio/best[height=480]"
        elif quality == "720p":
            format_string = "bestvideo[height=720]+bestaudio/best[height=720]"
        elif quality == "1080p":
            format_string = "bestvideo[height=1080]+bestaudio/best[height=1080]"
        else:
            format_string = "best"

        cmd = [
            "yt-dlp",
            "--yes-playlist",
            "-f", format_string,
            url,
            "-o", os.path.join(folder, "%(title)s.%(ext)s")
        ]
    root.after(100, lambda: run_command(cmd, "Download Channel Completed!"))

def run_command(cmd, success_msg):
    try:
        subprocess.run(cmd, check=True)

        # Tìm file mới nhất tải về
        folder = save_folder.get().strip()
        files = os.listdir(folder)
        files = [f for f in files if f.endswith((".webm", ".mkv", ".ts"))]
        if files:
            latest_file = max([os.path.join(folder, f) for f in files], key=os.path.getctime)
            mp4_file = os.path.splitext(latest_file)[0] + "_converted.mp4"

            update_status("Converting to .mp4...", "blue")

            subprocess.run([
                "ffmpeg", "-i", latest_file, "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", mp4_file
            ], check=True)

            # Xóa file gốc sau khi convert
            os.remove(latest_file)

            update_status(success_msg + " (Converted to .mp4)", "green")
            messagebox.showinfo("Notice", success_msg + "\nFile .mp4 created!")
        else:
            update_status(success_msg, "green")
            messagebox.showinfo("Notice", success_msg)
    except subprocess.CalledProcessError as e:
        update_status(f"Error: {e}", "red")
        messagebox.showerror("Error", f"Error: {e}")
    except Exception as e:
        update_status(f"Error: {e}", "red")
        messagebox.showerror("Error", f"Error: {e}")

def open_folder():
    folder = save_folder.get().strip()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select correct folder.")
        return

    if platform.system() == "Windows":
        os.startfile(folder)
    elif platform.system() == "Darwin":
        subprocess.run(["open", folder])
    else:
        subprocess.run(["xdg-open", folder])

    
root = tk.Tk()
root.title("Download video TikTok - Youtube (Auto Convert MP4)_Sang TB")

# Các trường nhập
tk.Label(root, text="Link Video").grid(row=0, column=0, padx=10, pady=5, sticky="w")
video_link = tk.StringVar()
tk.Entry(root, textvariable=video_link, width=50).grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Link Channel").grid(row=1, column=0, padx=10, pady=5, sticky="w")
channel_link = tk.StringVar()
tk.Entry(root, textvariable=channel_link, width=50).grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Save Folder").grid(row=2, column=0, padx=10, pady=5, sticky="w")
save_folder = tk.StringVar()
tk.Entry(root, textvariable=save_folder, width=50).grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Select", command=select_folder).grid(row=2, column=2, padx=10, pady=5)

# Combobox chất lượng
tk.Label(root, text="Select Quality").grid(row=3, column=0, padx=10, pady=5, sticky="w")
quality_choice = tk.StringVar(value="720p")
quality_menu = ttk.Combobox(root, textvariable=quality_choice, values=["480p", "720p", "1080p"], width=10)
quality_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Buttons
tk.Button(root, text="Download Video", bg="green",width=15, command=download_video).grid(row=4, column=1, padx=10, pady=5,sticky='s') #n, e, s, and/or w
tk.Button(root, text="Download Channel", bg="green",width=15, command=download_channel,).grid(row=5, column=1, padx=10, pady=5,sticky="s")
tk.Button(root, text="Open Folder", bg="orange", command=open_folder).grid(row=4, column=2,  padx=10, pady=5,sticky="w")

# Status
status_label = tk.Label(root, text="", fg="red", font=("Arial", 10), width=60, anchor="w")
status_label.grid(row=7, column=0, columnspan=3, pady=5, sticky="w")

root.mainloop()