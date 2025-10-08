# Import libraries
import pyautogui
from pynput import mouse


# User instructions
def display_instructions():
    print("========================================")
    print("==         STR Leveling v2.0          ==")
    print("========================================")
    print("Things you will need:")
    print("- flat surface to ride the bicycle on (3x3 foundations work well),")
    print("- flower, sugar, water, (lots) of coffee")
    print("- items to make yourself heavy (crafted sand bags are 4x4 & 20kg each)")
    print("\nInstructions for leveling strength in-game:")
    print("- Alt-TAB to the game & mount a bicycle.")
    print("- Press the middle mouse button to toggle ON/OFF.")
    print("- Check on your character every 30-40min.")
    print("----------------------------------------")


# Create a class to listen for middle mouse button clicks
class KeySimulator:
    # Initialize the class
    def __init__(self):
        self.keys_pressed = False
        self.listener = mouse.Listener(on_click=self.toggle_keys)
    
    # Function to toggle keys
    def toggle_keys(self, x, y, button, pressed):
        if button == mouse.Button.middle:
            if pressed:
                if self.keys_pressed:
                    self.keys_pressed = False
                    for key in ['d', 'w']:
                        pyautogui.keyUp(key)
                    print("Key pressing stopped.")
                else:
                    self.keys_pressed = True
                    # Scroll down the mouse wheel 10 clicks to reduce speed
                    pyautogui.scroll(-10)
                    for key in ['d', 'w']:
                        pyautogui.keyDown(key)
                    print("Key pressing started.")
    
    # Function to run the script
    def run(self):
        print("\nReady for middle mouse click.")
        with self.listener as listener:
            listener.join()


# Run the script
if __name__ == "__main__":
    display_instructions()
    simulator = KeySimulator()
    simulator.run()
