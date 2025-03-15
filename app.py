import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime
import pytz

# Location of txt files used in this code: C:\Users\Ryan's PC

LARGEFONT = ("Verdana", 35)

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initializing frames
        self.frames = {}

        # Adding frames to the container
        for F in (StartPage, NewAcc, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # Function to show a frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# StartPage class with username and password input fields
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Label for the StartPage
        label = ttk.Label(self, text="Time Sheet", font=LARGEFONT)
        label.grid(row=0, column=0)

        # Username Label and Entry
        name_label = ttk.Label(self, text="Username", font=('calibre', 10, 'bold'))
        name_label.grid(row=1, column=0)

        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(self, textvariable=self.name_var, font=('calibre', 10, 'normal')) # Label styling
        name_entry.grid(row=1, column=1)                                       # Label position

        # Password Label and Entry
        passw_label = ttk.Label(self, text="Password", font=('calibre', 10, 'bold')) # Label styling
        passw_label.grid(row=2, column=0)                          # Label position

        self.passw_var = tk.StringVar()
        passw_entry = ttk.Entry(self, textvariable=self.passw_var, font=('calibre', 10, 'normal'), show='*')
        passw_entry.grid(row=2, column=1)

        # Submit Button
        sub_btn = ttk.Button(self, text="Submit", command=self.submit)
        sub_btn.grid(row=3, column=1)

        # Buttons to navigate to other pages
        button1 = ttk.Button(self, text="New Account", command=lambda: controller.show_frame(NewAcc))
        button1.grid(row=4, column=1)

        button2 = ttk.Button(self, text="Page 2", command=lambda: controller.show_frame(Page2))
        button2.grid(row=5, column=1)

    # Submit function
    def submit(self):
        name = self.name_var.get()
        password = self.passw_var.get()

        print("The name is: " + name)
        print("The password is: " + password)

        # Write to a text file
        try:
            with open('info.txt', 'w') as info:
                info.write(f"Username: {name}\nPassword: {password}")
        except Exception as e:
            print("Problem submitting info:", str(e))

        # Clear the input fields
        self.name_var.set("")
        self.passw_var.set("")


# NewAcc class
class NewAcc(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Create Your Account")
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=1, padx=10, pady=10)



# Page2 class
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Clock in and out")
        label.grid(row=0, column=4, padx=10, pady=10)

        # Stopwatch Label
        self.time_label = ttk.Label(self, text="00:00:00", font=("Arial", 24))
        self.time_label.grid(row=1, column=4, padx=10, pady=10)

        # Start Button
        self.start_button = ttk.Button(self, text="Start", command=self.start_stopwatch)
        self.start_button.grid(row=2, column=3, padx=10, pady=10)

        # Stop Button
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_stopwatch, state=tk.DISABLED)
        self.stop_button.grid(row=2, column=5, padx=10, pady=10)

        # Button to go back to StartPage
        button1 = ttk.Button(self, text="Startpage", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=3, column=4, padx=10, pady=10)

        # Variables for stopwatch
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def start_stopwatch(self):
        """Start the stopwatch."""
        if not self.running:
            self.start_time = time.time() - self.elapsed_time  # Adjust start time if resuming
            self.running = True
            self.start_button.config(state=tk.DISABLED)  # Disable Start button
            self.stop_button.config(state=tk.NORMAL)  # Enable Stop button
            self.update_time()
            
            try:
                # Open the file in write mode ('w')
                with open("time.txt", "a") as file:
                    # Write the string to the file
                    current_dateTime = datetime.now() # Get current clock time
                    file.write("Start: " + str(current_dateTime) + "\n")
            except IOError as e:
                print(f"An error occurred: {e}")
            

    # Function that activates when pressing "Stop" button
    def stop_stopwatch(self):
        """Stop the stopwatch."""
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time  # Save elapsed time
            self.start_button.config(state=tk.NORMAL)  # Enable Start button
            self.stop_button.config(state=tk.DISABLED)  # Disable Stop button
            
            try:
                # Open the file in write mode ('w')
                with open("time.txt", "a") as file:
                    # Write the string to the file
                    current_dateTime = datetime.now() # Get current clock time
                    file.write("End: " + str(current_dateTime) + "\n" + "---------------------------------" + "\n")
            except IOError as e:
                print(f"An error occurred: {e}")

    def update_time(self):
        """Update the stopwatch display."""
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            formatted_time = self.format_time(self.elapsed_time)
            self.time_label.config(text=formatted_time)
            self.after(100, self.update_time)  # Update every 100ms

    def format_time(self, elapsed_time):
        """Format elapsed time into HH:MM:SS."""
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"


# Driver Code
app = tkinterApp()
app.mainloop()