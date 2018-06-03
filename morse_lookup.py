#!/usr/bin/python3
import sys

morse_code_lookup = {
    ".-":    "A",
    "-...":    "B",
    "-.-.":    "C",
    "-..":    "D",
    ".":    "E",
    "..-.":    "F",
    "--.":    "G",
    "....":    "H",
    "..":    "I",
    ".---":    "J",
    "-.-":    "K",
    ".-..":    "L",
    "--":    "M",
    "-.":    "N",
    "---":    "O",
    ".--.":    "P",
    "--.-":    "Q",
    ".-.":    "R",
    "...":    "S",
    "-":    "T",
    "..-":    "U",
    "...-":    "V",
    ".--":    "W",
    "-..-":    "X",
    "-.--":    "Y",
    "--..":    "Z",
    ".----":    "1",
    "..---":    "2",
    "...--":    "3",
    "....-":    "4",
    ".....":    "5",
    "-....":    "6",
    "--...":    "7",
    "---..":    "8",
    "----.":    "9",
    "-----":    "0",
    ".-.-.-":    ".",
    "--..--":    ",",
    "..--..":    "?"
}

def try_decode(bit_string):
    if bit_string in morse_code_lookup.keys():
        char = morse_code_lookup[bit_string]
        print(char)
        return char
    #sys.stdout.write(morse_code_lookup[bit_string])
    #sys.stdout.flush()
def to_keys(char):
    try:
        return list(morse_code_lookup.keys()) \
            [list(morse_code_lookup.values()).index(char.upper())]
    except:
        return None
