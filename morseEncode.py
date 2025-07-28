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
    '9': '----.',
    '&': '.-...',  "'": '.----.', '@': '.--.-.',
    ')': '-.--.-', '(': '-.--.', ':': '---...',
    ',': '--..--', '=': '-...-', '!': '-.-.--',
    '.': '.-.-.-', '-': '-....-', '+': '.-.-.',
    '"': '.-..-.', '?': '..--..', '/': '-..-.',
    ' ': '/',     # Use / for space between words
}

def text_to_morse(message):
    morse_message = ''
    for char in message.upper():
        if char in MORSE_CODE_DICT:
            morse_message += MORSE_CODE_DICT[char] + ' '
        else:
            morse_message += '? '  # Unknown character placeholder
    return morse_message.strip()

# Example usage
text = input("Enter a message to convert to Morse Code: ")
morse = text_to_morse(text)
print("Morse Code:", morse)
