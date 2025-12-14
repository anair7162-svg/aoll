import tkinter as tk
import threading
import time
import random
import pyautogui
import winsound
import sys
from PIL import Image, ImageTk, ImageOps

# Delay before everything starts
time.sleep(5)
print("[✓] Starting full glitch prank...")

# Capture screenshot
screenshot = pyautogui.screenshot()
screen_path = "screen_capture.png"
screenshot.save(screen_path)

# Init window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

# Load screenshot into canvas
base_img = Image.open(screen_path)
bg_image = ImageTk.PhotoImage(base_img)
bg_item = canvas.create_image(0, 0, anchor="nw", image=bg_image)

def launch_glitch():
    print("[✓] O key pressed. Launching glitch sequence!")
    # Start all chaos threads
    threading.Thread(target=visual_insanity, daemon=True).start()
    threading.Thread(target=draw_bars, daemon=True).start()
    threading.Thread(target=jitter, daemon=True).start()
    threading.Thread(target=buzz, daemon=True).start()
    threading.Thread(target=fake_errors, daemon=True).start()

root.bind("o", lambda e: launch_glitch())

# Escape key to quit
def stop(event=None):
    root.destroy()
    sys.exit()

root.bind("<Escape>", stop)

# Image transformation engine
def visual_insanity():
    while True:
        img = base_img.copy()
        r = random.random()

        if r < 0.2:
            img = img.rotate(random.choice([90, 180]), expand=True)
        elif r < 0.4:
            img = ImageOps.mirror(img)
        elif r < 0.5:
            img = Image.new("RGB", base_img.size, "white")

        img = img.resize((screen_w, screen_h))
        tk_img = ImageTk.PhotoImage(img)
        canvas.itemconfig(bg_item, image=tk_img)
        canvas.image = tk_img

        time.sleep(0.4)

# Glitch bar overlay
def draw_bars():
    while True:
        canvas.delete("bars")
        for _ in range(random.randint(10, 20)):
            x = random.randint(0, screen_w)
            w = random.randint(8, 40)
            y_shift = random.randint(-30, 30)
            color = random.choice(['#ff3333', '#00ffee', '#222', '#fff', '#ffcc00', '#00ff00'])
            canvas.create_rectangle(x, y_shift, x + w, screen_h + y_shift, fill=color, outline="", tags="bars")
        root.update_idletasks()
        time.sleep(0.05)

# Mouse jitter
def jitter():
    while True:
        x, y = pyautogui.position()
        dx = random.randint(-12, 12)
        dy = random.randint(-12, 12)
        pyautogui.moveTo(x + dx, y + dy, duration=0.01)
        time.sleep(0.03)

# Buzz forever
def buzz():
    while True:
        winsound.Beep(300, 200)

# Pop-up system error alerts
def fake_errors():
    messages = [
        "⚠ Display Driver Timeout Detected.",
        "💥 Memory Overflow at GPU Channel 3.",
        "❌ DXGI Fatal Exception C000001D",
        "🛑 Kernel Exception: Thread Hung in Render Loop"
    ]
    time.sleep(6)
    while True:
        popup = tk.Toplevel()
        popup.title("System Alert")
        popup.geometry(f"300x100+{random.randint(100, screen_w - 300)}+{random.randint(100, screen_h - 100)}")
        popup.attributes("-topmost", True)
        popup.configure(bg="white")
        label = tk.Label(popup, text=random.choice(messages), fg="red", bg="white",
                         font=("Segoe UI", 10, "bold"))
        label.pack(pady=30)
        popup.after(random.randint(2000, 4000), popup.destroy)
        time.sleep(random.uniform(2.0, 3.5))

# Launch chaos threads
threading.Thread(target=visual_insanity, daemon=True).start()
threading.Thread(target=draw_bars, daemon=True).start()
threading.Thread(target=jitter, daemon=True).start()
threading.Thread(target=buzz, daemon=True).start()
threading.Thread(target=fake_errors, daemon=True).start()

print("[✓] Glitch world deployed. Press ESC to flee.")
root.mainloop()