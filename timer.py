import tkinter as tk
from tkinter import ttk, messagebox
import time
class TimerStopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⏱️ Timer & Stopwatch")
        self.root.geometry("370x300")
        self.root.configure(bg="#f0f4ff")

        self.setup_variables()
        self.create_tabs()
        self.update_display()

    def setup_variables(self):
        self.running = False
        self.start_time = 0
        self.elapsed = 0
        self.timer_target = 0
        self.mode = "stopwatch"

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)
        self.tab_stopwatch = ttk.Frame(tab_control)
        self.tab_timer = ttk.Frame(tab_control)

        tab_control.add(self.tab_stopwatch, text='Stopwatch')
        tab_control.add(self.tab_timer, text='Timer')
        tab_control.pack(expand=1, fill='both')

        self.create_stopwatch_ui()
        self.create_timer_ui()

    def create_stopwatch_ui(self):
        self.sw_label = tk.Label(self.tab_stopwatch, text="00:00:00.000", font=("Arial", 28))
        self.sw_label.pack(pady=20)

        btn_frame = tk.Frame(self.tab_stopwatch)
        btn_frame.pack(pady=10)

        self.sw_toggle_btn = tk.Button(btn_frame, text="▶ Start", width=10, command=self.toggle_stopwatch)
        self.sw_toggle_btn.grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="🔄 Reset", width=10, command=self.reset_stopwatch).grid(row=0, column=1, padx=5)

    def create_timer_ui(self):
        self.timer_label = tk.Label(self.tab_timer, text="00:00:00.000", font=("Arial", 28))
        self.timer_label.pack(pady=20)

        entry_frame = tk.Frame(self.tab_timer)
        entry_frame.pack(pady=5)

        tk.Label(entry_frame, text="Set Timer (seconds):").grid(row=0, column=0)
        self.timer_entry = tk.Entry(entry_frame, width=10)
        self.timer_entry.grid(row=0, column=1)

        btn_frame = tk.Frame(self.tab_timer)
        btn_frame.pack(pady=10)

        self.timer_toggle_btn = tk.Button(btn_frame, text="▶ Start", width=10, command=self.toggle_timer)
        self.timer_toggle_btn.grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="🔄 Reset", width=10, command=self.reset_timer).grid(row=0, column=1, padx=5)

    def toggle_stopwatch(self):
        if self.running:
            self.running = False
            self.sw_toggle_btn.config(text="▶ Start")
        else:
            self.mode = "stopwatch"
            self.start_time = time.time() - self.elapsed
            self.running = True
            self.sw_toggle_btn.config(text="⏸ Stop")

    def reset_stopwatch(self):
        self.running = False
        self.elapsed = 0
        self.sw_label.config(text="00:00:00.000")
        self.sw_toggle_btn.config(text="▶ Start")

    def toggle_timer(self):
        if self.running:
            self.running = False
            self.timer_toggle_btn.config(text="▶ Start")
        else:
            try:
                seconds = float(self.timer_entry.get())
                self.mode = "timer"
                self.timer_target = time.time() + seconds
                self.running = True
                self.timer_toggle_btn.config(text="⏸ Stop")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number of seconds.")

    def reset_timer(self):
        self.running = False
        self.elapsed = 0
        self.timer_label.config(text="00:00:00.000")
        self.timer_toggle_btn.config(text="▶ Start")
        self.timer_entry.delete(0, tk.END)

    def update_display(self):
        if self.running:
            now = time.time()
            if self.mode == "stopwatch":
                self.elapsed = now - self.start_time
            elif self.mode == "timer":
                remaining = self.timer_target - now
                self.elapsed = max(0, remaining)
                if remaining <= 0:
                    self.running = False
                    messagebox.showinfo("⏰ Time's Up!", "The countdown has finished!")
                    self.timer_toggle_btn.config(text="▶ Start")

        total_ms = int(self.elapsed * 1000)
        mins, ms = divmod(total_ms, 60000)
        secs, ms = divmod(ms, 1000)
        hrs, mins = divmod(mins, 60)
        time_text = f"{hrs:02}:{mins:02}:{secs:02}.{ms:03}"

        if self.mode == "stopwatch":
            self.sw_label.config(text=time_text)
        elif self.mode == "timer":
            self.timer_label.config(text=time_text)

        self.root.after(100, self.update_display)

root = tk.Tk()
app = TimerStopwatchApp(root)
root.mainloop()
