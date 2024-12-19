from tkinter import *
from tkinter import ttk

class RobotControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Noffys Test GUI")
        self.datalist = []

        self.var = StringVar(value="Drive")
        self.var2 = StringVar(value="")

        self.font = ("Helvetica", 16)

        self.create_main_menu()
        self.create_drive_menu()
        self.create_turn_menu()
        self.create_wait_menu()
        self.create_start_menu()
        self.create_queue_display()

        self.show_main_menu()

    def create_main_menu(self):
        self.main_menu_frame = Frame(self.root)
        self.main_menu_frame.grid(row=0, column=0, sticky="nsew")

        Label(self.main_menu_frame, text="Select an action:", font=self.font).grid(row=0, column=0, columnspan=2, pady=10)
        Radiobutton(self.main_menu_frame, text="Drive", variable=self.var, value="Drive", font=self.font).grid(row=1, column=0, sticky=W, padx=20, pady=5)
        Radiobutton(self.main_menu_frame, text="Turn", variable=self.var, value="Turn", font=self.font).grid(row=2, column=0, sticky=W, padx=20, pady=5)
        Radiobutton(self.main_menu_frame, text="Wait", variable=self.var, value="Wait", font=self.font).grid(row=3, column=0, sticky=W, padx=20, pady=5)
        Radiobutton(self.main_menu_frame, text="Start", variable=self.var, value="Start", font=self.font).grid(row=4, column=0, sticky=W, padx=20, pady=5)
        Button(self.main_menu_frame, text="Next", width=25, command=self.on_select, font=self.font).grid(row=5, column=0, columnspan=2, pady=10)
        Button(self.main_menu_frame, text="Stop", width=25, command=self.root.destroy, font=self.font).grid(row=6, column=0, columnspan=2, pady=10)

    def create_drive_menu(self):
        self.drive_menu_frame = Frame(self.root)
        self.drive_menu_frame.grid(row=0, column=0, sticky="nsew")

        Label(self.drive_menu_frame, text="Select direction:", font=self.font).grid(row=0, column=0, columnspan=2, pady=10)
        Radiobutton(self.drive_menu_frame, text="Forwards", variable=self.var2, value="Forwards", font=self.font).grid(row=1, column=0, sticky=W, padx=20, pady=5)
        Radiobutton(self.drive_menu_frame, text="Backwards", variable=self.var2, value="Backwards", font=self.font).grid(row=2, column=0, sticky=W, padx=20, pady=5)
        Label(self.drive_menu_frame, text="Enter distance (cm):", font=self.font).grid(row=3, column=0, columnspan=2, pady=10)
        self.distance_var = StringVar()
        self.distance_var.trace_add("write", self.update_confirm_button)
        self.distance_entry = Entry(self.drive_menu_frame, textvariable=self.distance_var, font=self.font)
        self.distance_entry.grid(row=4, column=0, columnspan=2, pady=5)
        self.drive_confirm_button = Button(self.drive_menu_frame, text="Confirm", width=25, command=self.on_confirm, font=self.font, state=DISABLED)
        self.drive_confirm_button.grid(row=5, column=0, columnspan=2, pady=10)
        Button(self.drive_menu_frame, text="Back", width=25, command=lambda: self.back_to_main(self.distance_entry), font=self.font).grid(row=6, column=0, columnspan=2, pady=10)

    def create_turn_menu(self):
        self.turn_menu_frame = Frame(self.root)
        self.turn_menu_frame.grid(row=0, column=0, sticky="nsew")

        Label(self.turn_menu_frame, text="Select direction:", font=self.font).grid(row=0, column=0, columnspan=2, pady=10)
        Radiobutton(self.turn_menu_frame, text="Left", variable=self.var2, value="Left", font=self.font).grid(row=1, column=0, sticky=W, padx=20, pady=5)
        Radiobutton(self.turn_menu_frame, text="Right", variable=self.var2, value="Right", font=self.font).grid(row=2, column=0, sticky=W, padx=20, pady=5)
        Label(self.turn_menu_frame, text="Enter angle (degrees):", font=self.font).grid(row=3, column=0, columnspan=2, pady=10)
        self.angle_var = StringVar()
        self.angle_var.trace_add("write", self.update_confirm_button)
        self.angle_entry = Entry(self.turn_menu_frame, textvariable=self.angle_var, font=self.font)
        self.angle_entry.grid(row=4, column=0, columnspan=2, pady=5)
        self.turn_confirm_button = Button(self.turn_menu_frame, text="Confirm", width=25, command=self.on_confirm, font=self.font, state=DISABLED)
        self.turn_confirm_button.grid(row=5, column=0, columnspan=2, pady=10)
        Button(self.turn_menu_frame, text="Back", width=25, command=lambda: self.back_to_main(self.angle_entry), font=self.font).grid(row=6, column=0, columnspan=2, pady=10)

    def create_wait_menu(self):
        self.wait_menu_frame = Frame(self.root)
        self.wait_menu_frame.grid(row=0, column=0, sticky="nsew")

        Label(self.wait_menu_frame, text="Enter wait time (seconds):", font=self.font).grid(row=0, column=0, columnspan=2, pady=10)
        self.wait_time_var = StringVar()
        self.wait_time_var.trace_add("write", self.update_confirm_button)
        self.wait_time_entry = Entry(self.wait_menu_frame, textvariable=self.wait_time_var, font=self.font)
        self.wait_time_entry.grid(row=1, column=0, columnspan=2, pady=5)
        self.wait_confirm_button = Button(self.wait_menu_frame, text="Confirm", width=25, command=self.on_confirm, font=self.font, state=DISABLED)
        self.wait_confirm_button.grid(row=2, column=0, columnspan=2, pady=10)
        Button(self.wait_menu_frame, text="Back", width=25, command=lambda: self.back_to_main(self.wait_time_entry), font=self.font).grid(row=3, column=0, columnspan=2, pady=10)

    def create_start_menu(self):
        self.start_menu_frame = Frame(self.root)
        self.start_menu_frame.grid(row=0, column=0, sticky="nsew")

        Label(self.start_menu_frame, text="Start and Process selected", font=self.font).grid(row=0, column=0, columnspan=2, pady=10)
        Button(self.start_menu_frame, text="Confirm", width=25, command=self.on_confirm, font=self.font).grid(row=1, column=0, columnspan=2, pady=10)
        Button(self.start_menu_frame, text="Back", width=25, command=self.show_main_menu, font=self.font).grid(row=2, column=0, columnspan=2, pady=10)

    def create_queue_display(self):
        self.queue_frame = Frame(self.root)
        self.queue_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        Label(self.queue_frame, text="Command Queue", font=self.font).grid(row=0, column=0, pady=10)
        self.queue_listbox = Listbox(self.queue_frame, font=self.font, width=30, height=20)
        self.queue_listbox.grid(row=1, column=0, pady=10)

        self.current_command_label = Label(self.queue_frame, text="", font=self.font)
        self.current_command_label.grid(row=2, column=0, pady=10)

        self.progress_bar = ttk.Progressbar(self.queue_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=3, column=0, pady=10)

    def show_main_menu(self):
        self.main_menu_frame.tkraise()

    def show_drive_menu(self):
        self.var2.set("")  # Reset the secondary selection variable
        self.drive_menu_frame.tkraise()

    def show_turn_menu(self):
        self.var2.set("")  # Reset the secondary selection variable
        self.turn_menu_frame.tkraise()

    def show_wait_menu(self):
        self.wait_menu_frame.tkraise()

    def show_start_menu(self):
        self.start_menu_frame.tkraise()

    def back_to_main(self, entry_widget):
        entry_widget.delete(0, END)
        self.show_main_menu()

    def on_select(self):
        selection = self.var.get()
        print(f"Selected: {selection}")
        if selection == "Drive":
            self.show_drive_menu()
        elif selection == "Turn":
            self.show_turn_menu()
        elif selection == "Wait":
            self.show_wait_menu()
        elif selection == "Start":
            self.show_start_menu()

    def on_confirm(self):
        main_selection = self.var.get()
        if main_selection == "Drive":
            direction = self.var2.get()
            distance = self.distance_entry.get()
            command = f"Drive {direction} {distance} cm"
            self.datalist.append(command)
            print(f"Confirmed: {command}")
        elif main_selection == "Turn":
            direction = self.var2.get()
            angle = self.angle_entry.get()
            command = f"Turn {direction} {angle} degrees"
            self.datalist.append(command)
            print(f"Confirmed: {command}")
        elif main_selection == "Wait":
            wait_time = self.wait_time_entry.get()
            command = f"Wait {wait_time} seconds"
            self.datalist.append(command)
            print(f"Confirmed: {command}")
        elif main_selection == "Start":
            command = "Start"
            self.datalist.append(command)
            print(f"Confirmed: {command}")
            self.process_commands()  # Start processing commands
        self.update_queue_display()

    def update_queue_display(self):
        self.queue_listbox.delete(0, END)
        for command in self.datalist:
            self.queue_listbox.insert(END, command)

    def update_confirm_button(self, *args):
        if self.var.get() == "Drive":
            self.drive_confirm_button.config(state=NORMAL if self.distance_var.get() else DISABLED)
        elif self.var.get() == "Turn":
            self.turn_confirm_button.config(state=NORMAL if self.angle_var.get() else DISABLED)
        elif self.var.get() == "Wait":
            self.wait_confirm_button.config(state=NORMAL if self.wait_time_var.get() else DISABLED)

    def process_commands(self):
        if self.datalist:
            command = self.datalist.pop(0)
            self.current_command_label.config(text=f"Processing: {command}")
            self.update_queue_display()
            self.progress_bar["value"] = 0
            self.root.after(100, self.update_progress_bar)
            self.root.after(2000, self.process_commands)  # Simulate 2 seconds delay
        else:
            self.current_command_label.config(text="")

    def update_progress_bar(self):
        if self.progress_bar["value"] < 100:
            self.progress_bar["value"] += 5
            self.root.after(100, self.update_progress_bar)

if __name__ == "__main__":
    root = Tk()
    app = RobotControlGUI(root)
    root.mainloop()