import tkinter as tk
from tkinter import ttk
import time
import platform
import pyttsx3
from gtts import gTTS
import playsound
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

# Windows-only sound
if platform.system() == 'Windows':
    import winsound

# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-',    'B': '-...',  'C': '-.-.', 
    'D': '-..',   'E': '.',     'F': '..-.',
    'G': '--.',   'H': '....',  'I': '..',
    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',
    'S': '...',   'T': '-',     'U': '..-',
    'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', ' ': '/', '.': '.-.-.-', ',': '--..--'
}
REVERSE_MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

ENGLISH_URDU_DICT = {
    'HELLO': 'ہیلو',
    'WORLD': 'دنیا',
    'LOVE': 'محبت',
    'PEACE': 'امن',
    'GOOD': 'اچھا',
    'MORNING': 'صبح بخیر',
    'HOW ARE YOU': 'آپ کیسے ہیں؟'
}

# Encoding and Decoding
def encode_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '?') for char in text)

def decode_from_morse(code):
    words = code.strip().split(' / ')
    return ' '.join(
        ''.join(REVERSE_MORSE_CODE_DICT.get(c, '?') for c in word.split())
        for word in words
    )

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def manual_translate_to_urdu(text):
    return ENGLISH_URDU_DICT.get(text.upper().strip(), "🔍 ترجمہ دستیاب نہیں")

def speak_urdu(text):
    tts = gTTS(text=text, lang='ur')
    tts.save("urdu.mp3")
    playsound.playsound("urdu.mp3")

# Pulse visualizer logic
class PulseVisualizer:
    def __init__(self, morse_code):
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
        self.morse_code = morse_code
        self.x_data = []
        self.y_data = []

    def init_plot(self):
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(-0.5, 1.5)
        self.line.set_data([], [])
        return self.line,

    def generate_pulse_data(self):
        unit = 1  # 1 unit per dot
        for symbol in self.morse_code:
            if symbol == '.':
                yield [1] * unit + [0] * unit
            elif symbol == '-':
                yield [1] * (3 * unit) + [0] * unit
            elif symbol == ' ':
                yield [0] * (3 * unit)
            elif symbol == '/':
                yield [0] * (7 * unit)

    def animate(self, frame):
        try:
            pulse = next(self.pulse_gen)
            self.y_data.extend(pulse)
            self.x_data = list(range(len(self.y_data)))
            self.line.set_data(self.x_data, self.y_data)
            self.ax.set_xlim(0, len(self.y_data) + 10)
            return self.line,
        except StopIteration:
            return self.line,

    def show(self):
        self.pulse_gen = self.generate_pulse_data()
        ani = FuncAnimation(self.fig, self.animate, init_func=self.init_plot, interval=100, blit=True)
        plt.title("Morse Code Pulse Visualization")
        plt.xlabel("Time")
        plt.ylabel("Signal")
        plt.show()

def play_morse_and_visualize(morse_code):
    def play_and_visualize():
        # Sound playback (only on Windows)
        if platform.system() == 'Windows':
            unit = 100
            for char in morse_code:
                if char == '.':
                    winsound.Beep(700, unit)
                elif char == '-':
                    winsound.Beep(700, unit * 3)
                elif char == ' ':
                    time.sleep(unit / 1000.0 * 3)
                elif char == '/':
                    time.sleep(unit / 1000.0 * 7)
                time.sleep(unit / 1000.0)
        # Pulse Plot
        visualizer = PulseVisualizer(morse_code)
        visualizer.show()

    threading.Thread(target=play_and_visualize, daemon=True).start()

# GUI Class
class MorseCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code GUI with Sound, Urdu & Pulse View")
        self.root.geometry("760x720")
        self.root.configure(padx=20, pady=20)

        # Text → Morse
        ttk.Label(root, text="Text to Morse Code", font=("Helvetica", 14, "bold")).pack(pady=10)
        self.text_input = tk.Text(root, height=4, width=85, font=("Courier", 11))
        self.text_input.pack()
        ttk.Button(root, text="Encode ➤", command=self.encode).pack(pady=5)
        ttk.Button(root, text="🔊 Play Sound & Visualize", command=self.play_sound_and_visualize).pack(pady=5)
        self.morse_output = tk.Text(root, height=4, width=85, bg="#f0f0f0", font=("Courier", 11))
        self.morse_output.pack()

        ttk.Separator(root, orient='horizontal').pack(fill='x', pady=20)

        # Morse → Text
        ttk.Label(root, text="Morse Code to Text", font=("Helvetica", 14, "bold")).pack(pady=10)
        self.morse_input = tk.Text(root, height=4, width=85, font=("Courier", 11))
        self.morse_input.pack()
        ttk.Button(root, text="⬅ Decode", command=self.decode).pack(pady=5)
        ttk.Button(root, text="🗣️ Speak English", command=self.speak_english).pack(pady=5)
        ttk.Button(root, text="🇵🇰 Translate + Speak Urdu", command=self.translate_and_speak_urdu).pack(pady=5)
        self.text_output = tk.Text(root, height=4, width=85, bg="#f0f0f0", font=("Courier", 11))
        self.text_output.pack()

    def encode(self):
        text = self.text_input.get("1.0", tk.END).strip()
        morse = encode_to_morse(text)
        self.morse_output.delete("1.0", tk.END)
        self.morse_output.insert(tk.END, morse)

    def decode(self):
        code = self.morse_input.get("1.0", tk.END).strip()
        text = decode_from_morse(code)
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, text)

    def speak_english(self):
        text = self.text_output.get("1.0", tk.END).strip()
        if text:
            speak_text(text)

    def translate_and_speak_urdu(self):
        text = self.text_output.get("1.0", tk.END).strip()
        urdu = manual_translate_to_urdu(text)
        speak_urdu(urdu)

    def play_sound_and_visualize(self):
        morse = self.morse_output.get("1.0", tk.END).strip()
        if morse:
            play_morse_and_visualize(morse)

# Launch
if __name__ == "__main__":
    root = tk.Tk()
    app = MorseCodeApp(root)
    root.mainloop()
