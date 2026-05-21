"""
============================================================
Sorting Algorithm Visualizer — COMP9001 Final Project
Author: Tiansheng Chen (560517309)
============================================================

>>> THIS IS THE MAIN SCRIPT — run with: python3 main.py <

REQUIRES (all must be installed locally):
    - Python 3.10+
    - tkinter (bundled with Python on macOS/Windows)
    - matplotlib
    - numpy
    - pygame-ce  (NOT pygame — main pygame package has no
                  Python 3.14 wheel yet; use pygame-ce instead)

INSTALL:
    pip install matplotlib numpy pygame-ce

HOW TO USE:
    1. Run `python3 main.py`
    2. Press any key on the splash screen to enter the main UI
    3. Press PLAY to start the animation
    4. Adjust SPEED / SIZE sliders, use PAUSE / RESET / SOUND

NOTE TO TUTOR:
    This is a GUI application using tkinter + matplotlib +
    pygame-ce. It will NOT run inside Ed's environment.
    Please run it locally.

    Demo screenshots + writeup: see my Padlet post.
    Source: https://github.com/tianshengchen1217-wq/sorting-visualizer
============================================================
"""
import tkinter
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms import bubble_sort, selection_sort, quicksort, mergesort
import pygame
import numpy as np

# ============================================================
# Sound engine (pygame mixer, programmatic sine waves)
# ============================================================
SOUND_ENABLED = True
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=256)
except Exception as e:
    print(f"[warn] sound disabled: {e}")
    SOUND_ENABLED = False


def beep(freq=800, dur_ms=40, volume=0.15):                 #Generate a sine-wave beep on the fly. Silent if pygame failed to init.
    if not SOUND_ENABLED or not sound_on:
        return
    try:
        sr = 22050
        n = int(sr * dur_ms / 1000)
        t = np.arange(n) / sr
        wave = np.sin(2 * np.pi * freq * t) 
        envelope = np.exp(-t * 30)
        samples = (wave * envelope * 32767 * volume).astype(np.int16)
        pygame.sndarray.make_sound(samples).play()
    except Exception:
        pass   # never let sound break the UI

# === Theme: Cyberpunk Classic ===
BG_COLOR      = "#0a0e27"
SUBPLOT_BG    = "#1a1a2e"
DEFAULT_COLOR = "#00d9ff"
COMPARE_COLOR = "#ff006e"
SWAP_COLOR    = "#ffbe0b"
SORTED_COLOR  = "#06ffa5"
TEXT_COLOR    = "#ffffff"
GRID_COLOR    = "#5f5f7f"
EDGE_COLOR    = "#5dffea"
BTN_BG        = "#1a1a2e"
BTN_FG        = "#00d9ff"
BTN_HOVER_BG  = "#ff006e"
BTN_HOVER_FG  = "#ffffff"

# Algorithm sound frequencies (Hz) — A3-E4-A4-E5, harmonically aligned
ALGO_FREQ = {
    "Bubble Sort":    330,
    "Selection Sort": 440,
    "Quicksort":      660,
    "Mergesort":      880,
}

# Runtime mute toggle (separate from SOUND_ENABLED which is install-time)
sound_on = True


# ============================================================
# AlgorithmView class
# ============================================================
class AlgorithmView:
    def __init__(self, name, sort_function, data, ax):
        self.name = name
        self.sort_function = sort_function
        self.data = data.copy()
        self.ax = ax
        self.step, self.comparisons, self.swaps = sort_function(self.data)
        self.current_frame = 0

    def draw(self):
        #Draw current frame: theme-colored bars, active indices highlighted, title shows counters + step progress.
        # unpack new 5-tuple step element
        frame_data, frame_comp, frame_swap, active, action = self.step[self.current_frame]
        
        # decide color for each bar based on action and active indices
        is_last_frame = (self.current_frame == len(self.step) - 1)
        if is_last_frame:
            # everything green when fully sorted
            colors = [SORTED_COLOR] * len(frame_data)
        else:
            colors = [DEFAULT_COLOR] * len(frame_data)
            if action == "compare":
                for idx in active:
                    colors[idx] = COMPARE_COLOR
            elif action == "swap":
                for idx in active:
                    colors[idx] = SWAP_COLOR
        
        # draw bars with outline
        self.ax.clear()
        self.ax.bar(
            range(len(frame_data)),
            frame_data,
            color = colors,
            edgecolor = EDGE_COLOR,
            linewidth = 1.5,
            width=0.7
        )
        
        # apply theme to this subplot
        self.ax.set_facecolor(SUBPLOT_BG)
        self.ax.tick_params(colors = GRID_COLOR)
        for spine in self.ax.spines.values():
            spine.set_color(GRID_COLOR)
        
        # title: terminal-style prefix + live counters + step progress
        title = (
            f"> {self.name}\n"
            f"  comp:{frame_comp}  swap:{frame_swap}  step:{self.current_frame}/{len(self.step) - 1}"
        )
        self.ax.set_title(
            title,
            color = TEXT_COLOR,
            fontfamily = "monospace",
            fontsize = 10,
            loc = "left",
        )

        # Algorithm-specific sound: compare = brief tick, swap = louder thunk
        freq = ALGO_FREQ.get(self.name, 440)
        if action == "compare":
            beep(freq=freq, dur_ms=6, volume=0.012)
        elif action == "swap":
            beep(freq=freq, dur_ms=20, volume=0.035)

    def advance(self):
        #Move to next frame if possible.
        if self.current_frame < len(self.step) - 1:
            self.current_frame += 1
            return True
        return False


# ============================================================
# Window + layout
# ============================================================
window = tkinter.Tk()
window.title("Sorting Algorithm Visualizer")
window.configure(bg=BG_COLOR)
window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+0+0")

# Top control bar
control_frame = tkinter.Frame(window, bg=BG_COLOR, pady=12)
control_frame.pack(side=tkinter.TOP, fill=tkinter.X)

# Matplotlib figure
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.patch.set_facecolor(BG_COLOR)
fig.subplots_adjust(hspace=0.7, wspace=0.15)

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)


# ============================================================
# Global state 
# ============================================================
views = []
is_playing = False
after_id = None
SPEED_MS = 300


# ============================================================
# Helpers
# ============================================================
def generate_data(n=15):
    #Random unique numbers
    return random.sample(range(1, n * 2 + 1), n)


def create_views(data):
    #build the 4 views for given data
    global views
    for row in axes:
        for ax in row:
            ax.clear()
    views = [
        AlgorithmView("Bubble Sort",    bubble_sort,    data, axes[0][0]),
        AlgorithmView("Selection Sort", selection_sort, data, axes[0][1]),
        AlgorithmView("Quicksort",      quicksort,      data, axes[1][0]),
        AlgorithmView("Mergesort",      mergesort,      data, axes[1][1]),
    ]
    for v in views:
        v.draw()
    canvas.draw()


def play_step():
    """Advance every view by one frame; reschedule if any can still advance."""
    global after_id, is_playing
    if not is_playing:
        return
    any_advanced = False
    for view in views:
        if view.advance():
            any_advanced = True
        view.draw()
    canvas.draw()
    if any_advanced:
        after_id = window.after(SPEED_MS, play_step)
    else:
        is_playing = False
        after_id = None


# ============================================================
# Button callbacks
# ============================================================
def on_play():
    global is_playing
    if is_playing:
        return                       # already playing, ignore
    is_playing = True
    play_step()


def on_pause():
    global is_playing, after_id
    is_playing = False
    if after_id is not None:
        window.after_cancel(after_id)
        after_id = None


def on_reset():
    global is_playing, after_id
    is_playing = False
    if after_id is not None:
        window.after_cancel(after_id)
        after_id = None
    n = size_slider.get() 
    create_views(generate_data(n))

def on_toggle_sound():
    global sound_on
    sound_on = not sound_on
    sound_btn.config(text="🔊 SOUND" if sound_on else "🔇 MUTED")

def on_speed_change(val):
    #Slider drag → update animation delay
    global SPEED_MS
    SPEED_MS = int(val)


def on_size_change(event):
    """Slider release → regenerate data with new size / 松手 → 用新尺寸重置"""
    on_reset()


# ============================================================
# Fake buttons (Label + click event)
# ============================================================
def make_button(parent, text, callback):
    btn = tkinter.Label(
        parent,
        text=text,
        bg=BTN_BG,
        fg=BTN_FG,
        font=("Menlo", 14, "bold"),
        padx=24,
        pady=8,
        cursor="hand2",
        borderwidth=2,
        relief=tkinter.SOLID,
    )
    btn.bind("<Button-1>", lambda e: callback())
    btn.bind("<Enter>",    lambda e: btn.config(bg=BTN_HOVER_BG, fg=BTN_HOVER_FG))
    btn.bind("<Leave>",    lambda e: btn.config(bg=BTN_BG,       fg=BTN_FG))
    return btn

def make_slider(parent, label, from_, to, default, command=None, on_release=None):
    #Build a labelled slider with cyberpunk theme.
    container = tkinter.Frame(parent, bg=BG_COLOR)

    lbl = tkinter.Label(
        container, text=label,
        bg=BG_COLOR, fg=BTN_FG,
        font=("Menlo", 11, "bold"),
    )
    lbl.pack(side=tkinter.TOP)

    scale = tkinter.Scale(
        container,
        from_=from_, to=to,
        orient=tkinter.HORIZONTAL,
        length=180,
        bg=BG_COLOR,
        fg=BTN_FG,
        troughcolor=SUBPLOT_BG,
        activebackground=BTN_HOVER_BG,
        highlightthickness=0,
        borderwidth=0,
        font=("Menlo", 9),
        command=command,
    )
    scale.set(default)
    if on_release is not None:
        scale.bind("<ButtonRelease-1>", on_release)
    scale.pack(side=tkinter.TOP)
    return container, scale


play_btn  = make_button(control_frame, "▶ PLAY",  on_play)
pause_btn = make_button(control_frame, "⏸ PAUSE", on_pause)
reset_btn = make_button(control_frame, "🔄 RESET", on_reset)
sound_btn = make_button(control_frame, "🔊 SOUND", on_toggle_sound)

play_btn.pack(side=tkinter.LEFT, padx=10)
pause_btn.pack(side=tkinter.LEFT, padx=10)
reset_btn.pack(side=tkinter.LEFT, padx=10)
sound_btn.pack(side=tkinter.LEFT, padx=10)

# === Sliders ===
speed_box, speed_slider = make_slider(
    control_frame, "SPEED (ms)", 50, 800, SPEED_MS,
    command=on_speed_change,
)
size_box, size_slider = make_slider(
    control_frame, "SIZE", 5, 50, 15,
    on_release=on_size_change,
)
speed_box.pack(side=tkinter.LEFT, padx=20)
size_box.pack(side=tkinter.LEFT, padx=20)


# ============================================================
# Initial state
# ============================================================
create_views(generate_data())

# ============================================================
# Splash screen
# ============================================================
SPLASH_LINES = [
    # (text, ms_per_char)
    ("> SORTING ALGORITHM VISUALIZER", 60),
    ("> ============================", 20),
    ("", 0),
    ("> COMP9001 Final Project", 40),
    ("> by Chen Tiansheng", 40),
    ("", 0),
    ("> Initializing modules...", 30),
    ("> [OK] algorithms.bubble_sort", 12),
    ("> [OK] algorithms.selection_sort", 12),
    ("> [OK] algorithms.quicksort", 12),
    ("> [OK] algorithms.mergesort", 12),
    ("> [OK] visualization engine", 12),
    ("", 0),
    ("> System ready.", 80),
    ("", 0),
    ("> Press any key to start_", 50),
]

splash_frame = tkinter.Frame(window, bg="#000000")
splash_frame.place(x=0, y=0, relwidth=1, relheight=1)

splash_text = tkinter.Label(
    splash_frame,
    text="",
    bg="#000000",
    fg=BTN_FG,
    font=("Menlo", 20, "bold"),
    justify="left",
    anchor="nw",
)
splash_text.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.75)

# splash state
_splash_line = 0
_splash_char = 0
_splash_buf = ""
_splash_done = False


def splash_type():
    """Recursive typewriter: prints one char, schedules itself for the next."""
    global _splash_line, _splash_char, _splash_buf, _splash_done

    if _splash_line >= len(SPLASH_LINES):
        _splash_done = True
        return

    line, char_speed = SPLASH_LINES[_splash_line]

    if _splash_char < len(line):
        _splash_buf += line[_splash_char]
        _splash_char += 1
        splash_text.config(text=_splash_buf)
        # key click sound (only on non-space chars to reduce noise)
        if line[_splash_char - 1] != " ":
            beep(freq=1400, dur_ms=12, volume=0.04)
        window.after(max(char_speed, 1), splash_type)
    else:
        # end of line: newline + low enter beep
        _splash_buf += "\n"
        _splash_line += 1
        _splash_char = 0
        if line:                          # don't beep on blank lines
            beep(freq=500, dur_ms=25, volume=0.08)
        window.after(180, splash_type)


def end_splash(event=None):
    """Triggered by any key. Only works after typing finishes."""
    if not _splash_done:
        return
    beep(freq=900, dur_ms=80, volume=0.15)    # confirm beep
    splash_frame.destroy()
    window.unbind("<Key>")


window.bind("<Key>", end_splash)

# Boot chime: low → mid → high (mimics OS startup)
window.after(100, lambda: beep(freq=300, dur_ms=80, volume=0.2))
window.after(220, lambda: beep(freq=500, dur_ms=80, volume=0.2))
window.after(340, lambda: beep(freq=800, dur_ms=120, volume=0.25))

# Start typewriter after the boot chime
window.after(700, splash_type)

window.mainloop()