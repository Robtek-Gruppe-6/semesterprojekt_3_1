import curses
import time

class TerminalUI:
    #Class variables
    
    def __init__(self):
        self.screen = None
        
    
    def start_ui(self):
        #Initialize the curses screen
        self.screen = curses.initscr()
        curses.noecho() #Do not echo key presses
        curses.cbreak() #React to keys immediately without Enter
        self.screen.keypad(True) #Enable special keys (arrows, ect.)
        
    def stop_ui(self):
        #Reset the terminal to its normal state
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
        
    def display_menu(self, title, options):
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(1,2, title, curses.A_BOLD)
        
        #Display menu options
        for idx, option in enumerate(options, start = 2):
            self.screen.addstr(idx, 4, f"{idx - 1}. {option}")
        
        self.screen.refresh()
        
    def get_user_choice(self, num_options):
        choice = -1
        while choice not in range (1, num_options + 1):
            key = self.screen.getch() #Wait for key press
            if key in range(ord('1'), ord(str(num_options +1))):
                choice = key - ord('0') #Convert ASCII to number
        return choice
    
    def display_messeage(self, message, wait_seconds = 2):
        self.screen.clear()
        self.screen.addstr(1, 2, message)
        self.screen.refresh()
        time.sleep(wait_seconds)
        
    def clear_screen(self):
        self.screen.clear()
        self.screen.refresh()
        
    def run_example(self):
        self.start_ui()
        try:
            #Display a sample menu
            self.display_menu("Main Menu", ["Option 1", "Option 2", "Option 3", "Quit"])
            choice = self.get_user_choice(4)
            if choice == 4:
                self.display_messeage("Exiting...")
            else:
                self.display_messeage(f"You selected Option {choice}")
                
        finally:
            #Ensure the terminal is reset even if an error occurs
            self.stop_ui()
            
ui = TerminalUI() #Initialize the UI