from display import Display
from buttons import ButtonHandler
import time

menu_options = ["Tools", "Games", "Settings", "About"]
selected = 0

def main():
    display = Display()
    buttons = ButtonHandler()
    display.draw_menu("Main Menu", menu_options, selected)

    try:
        while True:
            btn = buttons.get_pressed()

            if btn == "UP":
                selected = (selected - 1) % len(menu_options)
                display.draw_menu("Main Menu", menu_options, selected)

            elif btn == "DOWN":
                selected = (selected + 1) % len(menu_options)
                display.draw_menu("Main Menu", menu_options, selected)

            elif btn == "OK":
                display.draw_menu("Selected", [menu_options[selected]], 0)
                time.sleep(0.5)

            time.sleep(0.1)
    except KeyboardInterrupt:
        buttons.cleanup()
        display.clear()

if __name__ == "__main__":
    main()