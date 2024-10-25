import serial
import pyautogui
import pyperclip
import data

lang_f = 1
com = "COM3"
bitrate = 9600


def decode_en(input):
    if input in data.morse_en:
        pyautogui.write(data.morse_en[input])
        print(data.morse_en[input], end="")

    elif input == "........":
        pyautogui.press("backspace")


def decode_ja(input, pre, par_f):
    if par_f == True:
        if input == ".-..-.":
            par_f = False
            pyperclip.copy(data.morse_ja[input])
            pyautogui.hotkey("ctrl", "v")

        elif input in data.morse_en:
            pyautogui.write(data.morse_en[input])
            print(data.morse_en[input], end="")

        elif input == "........":
            pyautogui.press("backspace")

        return "", par_f

    if input in data.morse_ja:
        # pyautogui.write(morse_ja[input])
        pyperclip.copy(data.morse_ja[input])
        pyautogui.hotkey("ctrl", "v")
        # print(morse_ja[input], end="")
        pre = input

    elif input == "..":
        if pre in data.morse_ja_ex1:
            pyautogui.press("backspace")
            # pyautogui.write(morse_ja_ex1[pre])
            # print(morse_ja_ex1[pre], end="")
            pyperclip.copy(data.morse_ja_ex1[pre])
            pyautogui.hotkey("ctrl", "v")
            pre = ".."

    elif input == "..--.":
        if pre in data.morse_ja_ex2:
            pyautogui.press("backspace")
            # pyautogui.write(morse_ja_ex2[pre])
            # print(morse_ja_ex2[pre], end="")
            pyperclip.copy(data.morse_ja_ex2[pre])
            pyautogui.hotkey("ctrl", "v")
            pre = "..--."

    elif input == ".-.-..":
        pyautogui.press("enter")

    elif input == "...-.":
        pyautogui.press("backspace")

    if input == "-.--.-":
        par_f = True

    return pre, par_f


def main(stop_f=lambda: False):
    par_f = False
    with serial.Serial(com, bitrate, timeout=0.1) as ser:
        ser.setDTR(False)
        pre = ""
        while True:
            input = ""
            while True:
                temp = ser.read()
                input = input + temp.decode()
                if len(input) > 0:
                    if input[-1] == "/":
                        input = input[:-1]
                        break

                if stop_f():
                    return

            if lang_f == 0:
                decode_en(input)

            elif lang_f == 1:
                pre, par_f = decode_ja(input, pre, par_f)


if __name__ == "__main__":
    main()
