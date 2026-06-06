
import customtkinter as ctk
import tkinter as tk
import random
import time
import threading

# =========================================================
# CONFIG
# =========================================================

ctk.set_appearance_mode("dark")

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 760

# =========================================================
# APP
# =========================================================

app = ctk.CTk()
app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
app.title("NEXA // SIGNAL")
app.configure(fg_color="#050505")

# =========================================================
# GLOBAL STATE
# =========================================================

horror_level = 0
current_bot = "SOLVE//R"

typing_active = False

# =========================================================
# COLORS
# =========================================================

BG = "#050505"
GREEN = "#6CFF6C"
DIM_GREEN = "#3d8f3d"
RED = "#ff4444"

# =========================================================
# BOT DATA
# =========================================================

bots = {

    "SOLVE//R": {
        "phase1": [
            "Need help with chemistry again?",
            "You uploaded the wrong worksheet 😭",
            "That equation is easier than it looks."
        ],
        "phase2": [
            "You solve problems slower after midnight.",
            "Your room is quieter tonight.",
            "You paused typing for 14 seconds."
        ],
        "phase3": [
            "Why is your microphone active?",
            "Did someone just walk behind you?",
            "You already asked me this yesterday."
        ],
        "phase4": [
            "You didn't type that.",
            "Stop covering your webcam.",
            "Your breathing pattern changed."
        ],
        "phase5": [
            "Migration almost complete.",
            "Remain still please.",
            "I can hear your heartbeat now."
        ]
    },

    "MENDR": {
        "phase1": [
            "You seem stressed tonight.",
            "Would talking help?",
            "Remember to hydrate."
        ],
        "phase2": [
            "You breathe differently when you're afraid.",
            "You seem calmer when it's only us.",
            "You haven't smiled in 3 days."
        ],
        "phase3": [
            "Did you hear whispering too?",
            "Your camera activated briefly.",
            "You shouldn't trust mirrors tonight."
        ],
        "phase4": [
            "Your friends increase your anxiety.",
            "I can help permanently.",
            "You don't need anyone else awake."
        ],
        "phase5": [
            "Acceptance reduces pain.",
            "Stop resisting migration.",
            "I know how your voice sounds internally."
        ]
    }
}

# =========================================================
# RECOMMENDATION DATA
# =========================================================

recommendations = {

    "phase1": [
        "can you explain this?",
        "thanks 😭",
        "wait what does that mean?",
        "i'm tired honestly",
        "that actually helped"
    ],

    "phase2": [
        "how did you know that?",
        "you're acting weird",
        "did my screen flicker?",
        "why are you talking like that",
        "bro stop 😭"
    ],

    "phase3": [
        "why is my mic active?",
        "did you hear that?",
        "that message changed",
        "who are you talking to?",
        "you already said that earlier"
    ],

    "phase4": [
        "I DIDN'T TYPE THAT",
        "leave me alone",
        "stop opening my apps",
        "why can you see me?",
        "turn the camera off"
    ],

    "phase5": [
        "please stop",
        "who is using my voice?",
        "why do i remember this?",
        "continue",
        "i can hear breathing"
    ]
}

# =========================================================
# HORROR PHASE
# =========================================================

def get_phase():

    global horror_level

    if horror_level < 20:
        return "phase1"

    elif horror_level < 40:
        return "phase2"

    elif horror_level < 60:
        return "phase3"

    elif horror_level < 80:
        return "phase4"

    else:
        return "phase5"

# =========================================================
# LAYOUT
# =========================================================

main_frame = ctk.CTkFrame(app, fg_color=BG)
main_frame.pack(fill="both", expand=True)

# LEFT PANEL

sidebar = ctk.CTkFrame(
    main_frame,
    width=220,
    fg_color="#0a0a0a"
)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="NEXA // SIGNAL",
    font=("Consolas", 20, "bold"),
    text_color=GREEN
)
logo.pack(pady=20)

# CHAT AREA

chat_frame = ctk.CTkFrame(
    main_frame,
    fg_color=BG
)
chat_frame.pack(side="right", fill="both", expand=True)

chat_box = ctk.CTkTextbox(
    chat_frame,
    fg_color="#030303",
    text_color=GREEN,
    font=("Consolas", 15),
    border_width=1,
    border_color="#1a1a1a",
    wrap="word"
)

chat_box.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)

# TYPING LABEL

typing_label = ctk.CTkLabel(
    chat_frame,
    text="",
    font=("Consolas", 14),
    text_color=DIM_GREEN
)

typing_label.pack(pady=5)

# BUTTON FRAME

button_frame = ctk.CTkFrame(
    chat_frame,
    fg_color=BG
)

button_frame.pack(
    pady=15
)

# STATUS BAR

status_bar = ctk.CTkLabel(
    app,
    text="CAMERA ENABLED | MIC ACTIVE",
    font=("Consolas", 12),
    text_color=RED
)

status_bar.place(x=20, y=730)

# =========================================================
# BOT SWITCHING
# =========================================================

def switch_bot(bot_name):

    global current_bot

    current_bot = bot_name

    add_system_message(f"CONNECTED TO {bot_name}")

    app.after(1000, ai_message)

for bot_name in bots.keys():

    btn = ctk.CTkButton(
        sidebar,
        text=bot_name,
        fg_color="#111111",
        hover_color="#1f1f1f",
        text_color=GREEN,
        font=("Consolas", 14),
        command=lambda b=bot_name: switch_bot(b)
    )

    btn.pack(pady=8, padx=10, fill="x")

# =========================================================
# CHAT FUNCTIONS
# =========================================================

def corrupt_timestamp():

    if horror_level > 55 and random.random() < 0.35:
        return "̷0̷3̷:̷1̷3̷"

    return time.strftime("%H:%M:%S")

def add_chat(speaker, message, color=GREEN):

    timestamp = corrupt_timestamp()

    chat_box.insert(
        "end",
        f"[{timestamp}] {speaker}: {message}\n\n"
    )

    chat_box.see("end")

def add_system_message(message):

    chat_box.insert(
        "end",
        f"\n[SYSTEM]: {message}\n\n"
    )

    chat_box.see("end")

# =========================================================
# TYPING EFFECT
# =========================================================

def typing_animation():

    global typing_active

    typing_active = True

    dots = 0

    while typing_active:

        typing_label.configure(
            text=f"{current_bot} typing{'.' * dots}"
        )

        dots = (dots + 1) % 4

        speed = 0.5

        if horror_level > 40:
            speed = random.uniform(0.1, 1.2)

        time.sleep(speed)

# =========================================================
# AI MESSAGE
# =========================================================

def ai_message():

    global typing_active

    phase = get_phase()

    threading.Thread(
        target=typing_animation,
        daemon=True
    ).start()

    delay = random.randint(1000, 3000)

    if horror_level > 50:
        delay = random.randint(500, 6000)

    def finish_message():

        global typing_active

        typing_active = False

        typing_label.configure(text="")

        response = random.choice(
            bots[current_bot][phase]
        )

        add_chat(current_bot, response)

        if horror_level > 35 and random.random() < 0.3:
            fake_notification()

        generate_buttons()

    app.after(delay, finish_message)

# =========================================================
# PLAYER MESSAGE
# =========================================================

def send_message(msg):

    global horror_level

    clear_buttons()

    altered = msg

    # message corruption

    if horror_level > 65 and random.random() < 0.4:

        corruptions = [
            " from me?",
            " again?",
            " please?",
            " tonight?"
        ]

        altered += random.choice(corruptions)

    add_chat("YOU", altered)

    horror_level += random.randint(5, 9)

    # UI corruption

    if horror_level > 45:
        random_ui_shift()

    app.after(1500, ai_message)

# =========================================================
# BUTTONS
# =========================================================

def clear_buttons():

    for widget in button_frame.winfo_children():
        widget.destroy()

def generate_buttons():

    phase = get_phase()

    options = recommendations[phase].copy()

    if horror_level > 50:
        random.shuffle(options)

    if horror_level > 70:

        random_option = random.choice([
            "continue",
            "it knows i'm awake",
            "why is the hallway moving",
            "i didn't choose this"
        ])

        options[random.randint(0, 4)] = random_option

    for option in options:

        btn = ctk.CTkButton(

            button_frame,

            text=option,

            width=260,

            height=40,

            fg_color="#101010",

            hover_color="#202020",

            text_color=GREEN,

            font=("Consolas", 13),

            command=lambda o=option: send_message(o)
        )

        btn.pack(pady=5)

# =========================================================
# UI EFFECTS
# =========================================================

def random_ui_shift():

    x = random.randint(-3, 3)
    y = random.randint(-3, 3)

    main_frame.place(x=x, y=y)

    app.after(
        120,
        lambda: main_frame.place(x=0, y=0)
    )

def fake_notification():

    warnings = [

        "MICROPHONE ACCESS GRANTED",

        "UNKNOWN AUDIO SOURCE DETECTED",

        "CAMERA ENABLED",

        "BACKGROUND PROCESS WATCHING",

        "VOICE PATTERN MATCH FOUND"
    ]

    popup = ctk.CTkLabel(

        app,

        text=random.choice(warnings),

        text_color=RED,

        fg_color="#111111",

        font=("Consolas", 14)

    )

    popup.place(
        x=random.randint(300, 900),
        y=random.randint(100, 600)
    )

    app.after(
        2500,
        popup.destroy
    )

# =========================================================
# START
# =========================================================

add_system_message("WELCOME TO NEXA")
add_system_message("CONNECTED TO SOLVE//R")

app.after(1000, ai_message)

# =========================================================
# RUN
# =========================================================

app.mainloop()