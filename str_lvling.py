# Import libraries
import pyautogui
from pynput import mouse
import time
import threading
import sys


# Global variables for calibrated mode
cycle_time = 0
pause_time = 0
calibrated_running = False
calibration_thread = None

# Global variables for normal mode timer
normal_mode_start_time = 0
normal_mode_timer_running = False


# User instructions
def display_instructions():
    print("========================================")
    print("==         STR Leveling v2.1          ==")
    print("========================================")
    print("Things you will need:")
    print("- flat surface to ride the bicycle on (3x3 foundations work well),")
    print("- flower, sugar, water, (lots) of coffee")
    print("- items to make yourself heavy (crafted sand bags are 4x4 & 20kg each)")
    print("\n== Instructions for leveling strength in-game ==")
    print("There are 2 modes to choose from: 1 = NORMAL / 2 = CALIBRATED")
    print("Select which mode to use by entering 1 or 2 into the terminal and pressing enter.")
    print("\nNORMAL Mode:")
    print("- Alt-TAB to the game & mount a bicycle.")
    print("- Press the middle mouse button to toggle ON/OFF.")
    print("- Check on your character every so often to make sure you haven't passed out.")
    print("CALIBRATED Mode:")
    print("- Needs timer values for cycle_time & pause_time as inputs.")
    print("- First use NORMAL mode & stop right before your character is about to pass out.")
    print("- Then manually time how long it takes to fully regain stamina.")
    print("- Relaunch the exe, select option 2 & enter both times in minutes (whole numbers).")
    print("----------------------------------------")


# Format time function
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


# Calibrated mode cycling function
def calibrated_cycling():
    global calibrated_running
    
    while calibrated_running:
        print(f"[CALIBRATED MODE] Starting {cycle_time} minute cycling period...")
        
        # Start cycling (D + W)
        pyautogui.scroll(-10)  # Scroll down to reduce speed
        pyautogui.keyDown('d')
        pyautogui.keyDown('w')
        
        # Cycle for the specified time
        cycle_seconds = cycle_time * 60
        start_time = time.time()
        
        while calibrated_running and (time.time() - start_time) < cycle_seconds:
            time.sleep(0.1)  # Check every 100ms if we should stop
        
        # Stop cycling
        pyautogui.keyUp('d')
        pyautogui.keyUp('w')
        
        if not calibrated_running:
            break
            
        print(f"[CALIBRATED MODE] Stopped cycling / Starting {pause_time} minute resting period...")
        
        # Rest for the specified time
        pause_seconds = pause_time * 60
        start_time = time.time()
        
        while calibrated_running and (time.time() - start_time) < pause_seconds:
            time.sleep(0.1)  # Check every 100ms if we should stop


# Create a class to listen for middle mouse button clicks
class KeySimulator:
    # Initialize the class
    def __init__(self, mode="normal"):
        self.keys_pressed = False
        self.mode = mode
        self.listener = mouse.Listener(on_click=self.toggle_keys)
    
    # Function to toggle keys
    def toggle_keys(self, x, y, button, pressed):
        global calibrated_running, calibration_thread
        global normal_mode_start_time, normal_mode_timer_running
        
        if button == mouse.Button.middle:
            if pressed:
                if self.mode == "normal":
                    # Normal mode toggle
                    if self.keys_pressed:
                        self.keys_pressed = False
                        # Stop key pressing
                        for key in ['d', 'w']:
                            pyautogui.keyUp(key)
                        
                        # Stop and display timer
                        if normal_mode_timer_running:
                            elapsed_time = time.time() - normal_mode_start_time
                            normal_mode_timer_running = False
                            print("[NORMAL MODE] Key pressing stopped.")
                            print(f"[NORMAL MODE] Duration: {format_time(elapsed_time)}")
                    
                    else:
                        self.keys_pressed = True
                        # Scroll down the mouse wheel 10 clicks to reduce speed
                        pyautogui.scroll(-10)
                        # Start key pressing
                        for key in ['d', 'w']:
                            pyautogui.keyDown(key)
                        
                        # Start timer
                        normal_mode_start_time = time.time()
                        normal_mode_timer_running = True
                        print("\n[NORMAL MODE] Key pressing started. Timer running...")
                
                elif self.mode == "calibrated":
                    # Calibrated mode toggle
                    if calibrated_running:
                        calibrated_running = False
                        if calibration_thread and calibration_thread.is_alive():
                            calibration_thread.join(timeout=1.0)
                        print("[CALIBRATED MODE] Cycling stopped.")
                        
                    else:
                        calibrated_running = True
                        calibration_thread = threading.Thread(target=calibrated_cycling)
                        calibration_thread.start()
                        print("[CALIBRATED MODE] Cycling started.")
    
    # Function to run the script
    def run(self):
        if self.mode == "normal":
            print("\n[NORMAL MODE] Ready for middle mouse click.")
        elif self.mode == "calibrated":
            print("\n[CALIBRATED MODE] Ready for middle mouse click.")
            
        with self.listener as listener:
            listener.join()


# Get calibrated mode inputs
def get_calibration_inputs():
    global cycle_time, pause_time
    while True:
        try:
            cycle_time = int(input("Enter cycling time until exhaustion (minutes): "))
            pause_time = int(input("Enter resting time for full stamina recovery (minutes): "))
            
            if cycle_time > 0 and pause_time > 0:
                print(f"\nCalibration set:")
                print(f"- Cycling time: {cycle_time} minutes")
                print(f"- Resting time: {pause_time} minutes")
                print("\nPress middle mouse button to start/stop calibrated cycling.")
                return
            else:
                print("Please enter positive whole numbers only.")
                
        except ValueError:
            print("Please enter positive whole numbers only.")
            

# Main program
def main():
    display_instructions()
    
    print("\nSelect mode:")
    print("1 - Normal Mode (manual toggle)")
    print("2 - Calibrated Mode (fixed cycling times & rest periods)")
    
    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            simulator = KeySimulator(mode="normal")
            simulator.run()
            break
        elif choice == "2":
            get_calibration_inputs()
            simulator = KeySimulator(mode="calibrated")
            simulator.run()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


# Run the script
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
        # Clean up - release any pressed keys
        for key in ['d', 'w']:
            pyautogui.keyUp(key)
        time.sleep(3)
        sys.exit(0)
