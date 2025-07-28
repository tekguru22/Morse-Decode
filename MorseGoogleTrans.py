import tkinter as tk
from tkinter import ttk
import time
import platform
import pyttsx3
from gtts import gTTS
import playsound

# --- Morse Code Dictionary ---
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
    '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..',
    '!': '-.-.--', '/': '-..-.', ' ': '/',
}
REVERSE_MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def encode_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '?') for char in text)

def decode_from_morse(code):
    words = code.strip().split(' / ')
    decoded_words = []
    for word in words:
        letters = word.strip().split()
        decoded_word = ''.join(REVERSE_MORSE_CODE_DICT.get(l, '?') for l in letters)
        decoded_words.append(decoded_word)
    return ' '.join(decoded_words)

def play_morse_sound(morse_code):
    if platform.system() != 'Windows':
        print("Morse sound only supported on Windows.")
        return
    import winsound
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
        else:
            time.sleep(unit / 1000.0)
        time.sleep(unit / 1000.0)

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# --- Manual English to Urdu Dictionary (Sample Only) ---
ENGLISH_URDU_DICT = {
    'HELLO': 'ہیلو',
    'WORLD': 'دنیا',
    'GOOD': 'اچھا',
    'MORNING': 'صبح بخیر',
    'TEST': 'جانچ',
    'LOVE': 'محبت',
    'PEACE': 'امن',
    'HOW ARE YOU': 'آپ کیسے ہیں؟'
}

def manual_translate_to_urdu(text):
    text = text.upper()
    return ENGLISH_URDU_DICT.get(text.strip(), "🔍 ترجمہ دستیاب نہیں")

def speak_urdu_text(urdu_text):
    tts = gTTS(text=urdu_text, lang='ur')
    tts.save("urdu_output.mp3")
    playsound.playsound("urdu_output.mp3")

# --- GUI App ---
class MorseCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code with Urdu Speak (Python 3.13 Safe)")
        self.root.geometry("760x670")
        self.root.configure(padx=20, pady=20)

        ttk.Label(root, text="Text to Morse Code", font=("Helvetica", 14, "bold")).pack(pady=10)
        self.text_input = tk.Text(root, height=4, width=85, font=("Courier", 11))
        self.text_input.pack()
        ttk.Button(root, text="Encode ➤", command=self.encode).pack(pady=5)
        ttk.Button(root, text="🔊 Play Morse Sound", command=self.play_sound).pack(pady=5)
        self.morse_output = tk.Text(root, height=4, width=85, font=("Courier", 11), bg="#f0f0f0")
        self.morse_output.pack()

        ttk.Separator(root, orient='horizontal').pack(fill='x', pady=20)

        ttk.Label(root, text="Morse Code to Text", font=("Helvetica", 14, "bold")).pack(pady=10)
        self.morse_input = tk.Text(root, height=4, width=85, font=("Courier", 11))
        self.morse_input.pack()
        ttk.Button(root, text="⬅ Decode", command=self.decode).pack(pady=5)
        ttk.Button(root, text="🔈 Speak English", command=self.speak_decoded_text).pack(pady=5)
        ttk.Button(root, text="🌐 Translate + Speak Urdu (Demo)", command=self.translate_and_speak_urdu).pack(pady=5)
        self.text_output = tk.Text(root, height=4, width=85, font=("Courier", 11), bg="#f0f0f0")
        self.text_output.pack()

    def encode(self):
        message = self.text_input.get("1.0", tk.END).strip()
        morse = encode_to_morse(message)
        self.morse_output.delete("1.0", tk.END)
        self.morse_output.insert(tk.END, morse)

    def decode(self):
        morse_code = self.morse_input.get("1.0", tk.END).strip()
        text = decode_from_morse(morse_code)
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, text)

    def play_sound(self):
        morse = self.morse_output.get("1.0", tk.END).strip()
        play_morse_sound(morse)

    def speak_decoded_text(self):
        text = self.text_output.get("1.0", tk.END).strip()
        if text:
            speak_text(text)

    def translate_and_speak_urdu(self):
        text = self.text_output.get("1.0", tk.END).strip()
        urdu_translation = manual_translate_to_urdu(text)
        print("✅ Urdu Translation:", urdu_translation)
        speak_urdu_text(urdu_translation)

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MorseCodeApp(root)
    root.mainloop()
