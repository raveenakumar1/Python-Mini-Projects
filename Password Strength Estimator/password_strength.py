import sys
import math
from zxcvbn import zxcvbn
from datetime import datetime, timedelta

#this function takes seconds and makes them into readable time
def format_crack_time(seconds):
    """Convert seconds to a human-readable time format"""
    if seconds < 1:
        return "less than a second"
    
    #break down the seconds into all the different time units
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    months, days = divmod(days, 30)
    years, months = divmod(months, 12)
    
    #build a list of the time parts that have value
    time_units = []
    if years >= 1:
        time_units.append(f"{int(years)} year{'s' if years > 1 else ''}")
    if months >= 1:
        time_units.append(f"{int(months)} month{'s' if months > 1 else ''}")
    if days >= 1:
        time_units.append(f"{int(days)} day{'s' if days > 1 else ''}")
    if hours >= 1 and len(time_units) < 2:
        time_units.append(f"{int(hours)} hour{'s' if hours > 1 else ''}")
    if minutes >= 1 and len(time_units) < 2:
        time_units.append(f"{int(minutes)} minute{'s' if minutes > 1 else ''}")
    if seconds >= 1 and len(time_units) < 2:
        time_units.append(f"{int(seconds)} second{'s' if seconds > 1 else ''}")
    
    #only show the two most significant time units 
    return ", ".join(time_units[:2])

#convert the number score into words 
def get_strength_label(score):
    """Convert numeric score to text label"""
    labels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Good",
        4: "Strong"
    }
    return labels.get(score, "Very Weak")

#get colors for the terminal output based on how good the password is
#red for bad, yellow for okay, green for good passwords
def get_color(score):
    """Get color based on score"""
    colors = {
        0: "\033[91m",  # Red
        1: "\033[91m",  # Red
        2: "\033[93m",  # Yellow
        3: "\033[92m",  # Green
        4: "\033[92m",  # Green
    }
    return colors.get(score, "\033[91m")

#using the zxcvbn library to check password for the work of figuring out how strong the password really is
def analyze_password(password):
    """Analyze password using zxcvbn"""
    if not password:
        return None
    
    results = zxcvbn(password)
    return results

#formatting results
def display_results(results, password):
    """Display results in a formatted way"""
    if not results:
        print("No password provided.")
        return
    
    #extract the important information from the analysis results
    score = results['score']
    crack_time = results['crack_times_display']['offline_slow_hashing_1e4_per_second']
    feedback = results['feedback']['suggestions']
    warning = results['feedback']['warning']
    
    #get the text label and color for the password strength
    strength_label = get_strength_label(score)
    color = get_color(score)
    reset_color = "\033[0m"
    
    #print everything with nice formatting and borders
    print("\n" + "="*60)
    print("PASSWORD STRENGTH ANALYSIS")
    print("="*60)
    print(f"Password: {password}")
    print(f"Strength: {color}{strength_label} ({score}/4){reset_color}")
    print(f"Time to crack: {format_crack_time(results['crack_times_seconds']['offline_slow_hashing_1e4_per_second'])}")
    print(f"Estimated crack time: {crack_time}")
    
    #show any warnings about particularly bad password choices
    if warning:
        print(f"\n\033[91mWarning: {warning}\033[0m")
    
    #give suggestions on how to make the password stronger
    if feedback:
        print(f"\nSuggestions:")
        for suggestion in feedback:
            print(f"  - {suggestion}")
    
    #show what patterns were found in the password if available
    if 'sequence' in results:
        print(f"\nPattern analysis:")
        for i, seq in enumerate(results['sequence']):
            pattern_type = seq.get('pattern', 'unknown').title()
            print(f"  {i+1}. {seq['token']} ({pattern_type})")
    
    print("="*60)

#command line interface option
#it keeps asking for passwords until you tell it to stop
def cli_interface():
    """Command-line interface for password strength checking"""
    print("Password Strength Estimator")
    print("Enter passwords to check their strength (type 'quit' to exit)")
    
    while True:
        password = input("\nEnter password: ").strip()
        
        #let people quit when they're done testing passwords
        if password.lower() in ['quit', 'exit', 'q']:
            break
        
        #analyze the password and show the results
        results = analyze_password(password)
        display_results(results, password)

#make a graphical interface for people who don't like command line
def simple_gui():
    """Simple GUI interface using Tkinter"""
    try:
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        #if tkinter isn't available, just use the command line instead
        print("Tkinter is not available. Using CLI interface instead.")
        cli_interface()
        return
    
    #this function gets called every time someone type in the password box
    #updates the strength display in real time as someone types
    def update_strength(event=None):
        password = password_entry.get()
        if not password:
            #clear everything if there's no password to check
            result_text.delete(1.0, tk.END)
            strength_label.config(text="Strength: N/A", background="light gray")
            return
        
        #analyze the current password and update the display
        results = analyze_password(password)
        if not results:
            return
        
        score = results['score']
        strength_text = get_strength_label(score)
        crack_time = format_crack_time(results['crack_times_seconds']['offline_slow_hashing_1e4_per_second'])
        
        #update the strength label with color coding
        colors = {
            0: "red",
            1: "red",
            2: "orange",
            3: "yellow",
            4: "green"
        }
        strength_label.config(text=f"Strength: {strength_text} ({score}/4)", 
                             background=colors.get(score, "red"))
        
        #update the detailed results text area with all the information
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Time to crack: {crack_time}\n")
        result_text.insert(tk.END, f"Estimated: {results['crack_times_display']['offline_slow_hashing_1e4_per_second']}\n\n")
        
        #show any warnings about the password
        if results['feedback']['warning']:
            result_text.insert(tk.END, f"Warning: {results['feedback']['warning']}\n\n")
        
        #show suggestions for improving the password
        if results['feedback']['suggestions']:
            result_text.insert(tk.END, "Suggestions:\n")
            for suggestion in results['feedback']['suggestions']:
                result_text.insert(tk.END, f"• {suggestion}\n")
    
    #create the main application window
    root = tk.Tk()
    root.title("Password Strength Estimator")
    root.geometry("600x500")
    root.resizable(True, True)
    
    #create a frame to hold all the widgets with some padding
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    #add a title label at the top
    title_label = ttk.Label(main_frame, text="Password Strength Estimator", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    #label for the password entry box
    ttk.Label(main_frame, text="Enter password:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
    
    #the text box where you type your password to test it
    password_entry = ttk.Entry(main_frame, width=40, show="•")
    password_entry.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    password_entry.bind("<KeyRelease>", update_strength)
    
    #label that shows the strength result with color coding
    strength_label = ttk.Label(main_frame, text="Strength: N/A", background="light gray", 
                              font=("Arial", 12, "bold"))
    strength_label.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    
    #text area that shows all the detailed analysis results
    result_text = tk.Text(main_frame, width=60, height=20, wrap=tk.WORD)
    result_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
    
    #configure the layout to resize properly when the window is resized
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(4, weight=1)
    
    #start the application and wait for user interaction
    root.mainloop()

#this is where the program actually starts running when you execute it
if __name__ == "__main__":
    #check if a password was provided as a command line argument
    if len(sys.argv) > 1:
        password = " ".join(sys.argv[1:])
        results = analyze_password(password)
        display_results(results, password)
    else:
        #if no password was provided, start the interactive interface
        #try to use the graphical interface first, fall back to command line
        try:
            simple_gui()
        except:
            cli_interface()
