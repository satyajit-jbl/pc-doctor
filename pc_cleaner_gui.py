import os
import shutil
import tempfile
import ctypes
import tkinter as tk
from tkinter import messagebox

# ----------------- CLEAN FUNCTIONS -----------------

def delete_files(folder):
    if not os.path.exists(folder):
        return
    for root, dirs, files in os.walk(folder):
        for file in files:
            try:
                os.remove(os.path.join(root, file))
            except:
                pass
        for dir in dirs:
            try:
                shutil.rmtree(os.path.join(root, dir))
            except:
                pass


def clear_system_temp(log):
    log("Cleaning system temp files...")
    delete_files(tempfile.gettempdir())


def clear_user_temp(log):
    log("Cleaning user temp files...")
    temp = os.environ.get("TEMP")
    if temp:
        delete_files(temp)


def clear_recent(log):
    log("Cleaning recent files...")
    recent = os.path.join(
        os.environ["APPDATA"],
        "Microsoft",
        "Windows",
        "Recent"
    )
    delete_files(recent)


def empty_recycle_bin(log):
    log("Emptying recycle bin...")
    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000001)
    except:
        pass


# ----------------- DISK USAGE -----------------

def get_disk_usage():
    total, used, free = shutil.disk_usage("C:/")
    gb = 1024 ** 3
    return total // gb, used // gb, free // gb


# ----------------- GUI APP -----------------

class PCCleanerApp:
    def __init__(self, root):
        self.root = root
        root.title("PC Cleaner")
        root.geometry("520x500")
        root.resizable(False, False)

        tk.Label(root, text="🧹 PC Cleaner", font=("Arial", 18, "bold")).pack(pady=10)

        self.disk_label = tk.Label(root, font=("Arial", 11))
        self.disk_label.pack()

        # Checkboxes
        self.var_sys_temp = tk.BooleanVar(value=True)
        self.var_user_temp = tk.BooleanVar(value=True)
        self.var_recent = tk.BooleanVar(value=True)
        self.var_recycle = tk.BooleanVar(value=True)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Checkbutton(frame, text="System Temp Files", variable=self.var_sys_temp).grid(row=0, column=0, sticky="w")
        tk.Checkbutton(frame, text="User Temp Files", variable=self.var_user_temp).grid(row=1, column=0, sticky="w")
        tk.Checkbutton(frame, text="Recent Files", variable=self.var_recent).grid(row=2, column=0, sticky="w")
        tk.Checkbutton(frame, text="Recycle Bin", variable=self.var_recycle).grid(row=3, column=0, sticky="w")

        self.log_box = tk.Text(root, height=12, width=60)
        self.log_box.pack(pady=10)

        tk.Button(
            root,
            text="Clean Now",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            command=self.start_cleanup
        ).pack(pady=10)

        self.update_disk()

    def log(self, msg):
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)
        self.root.update()

    def update_disk(self):
        total, used, free = get_disk_usage()
        self.disk_label.config(
            text=f"Disk C:  Total {total} GB | Used {used} GB | Free {free} GB"
        )

    def start_cleanup(self):
        before = get_disk_usage()
        self.log(f"Before Cleanup → Free Space: {before[2]} GB")

        if self.var_sys_temp.get():
            clear_system_temp(self.log)
        if self.var_user_temp.get():
            clear_user_temp(self.log)
        if self.var_recent.get():
            clear_recent(self.log)
        if self.var_recycle.get():
            empty_recycle_bin(self.log)

        after = get_disk_usage()
        freed = after[2] - before[2]

        self.log(f"After Cleanup → Free Space: {after[2]} GB")
        self.log(f"Total Space Freed: {freed} GB")

        self.update_disk()
        messagebox.showinfo("Cleanup Done", "Selected cleanup completed successfully!")


# ----------------- RUN -----------------

if __name__ == "__main__":
    root = tk.Tk()
    PCCleanerApp(root)
    root.mainloop()
