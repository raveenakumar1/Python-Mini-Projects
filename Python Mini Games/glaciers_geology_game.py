import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class GlacierQuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Glacier Geology Quiz")
        self.root.geometry("700x600")
        
#glacier themed colors for the ui - dark greens and blues like ice and water
        self.colors = {
            "dark_green": "#2E5266",      #like deep glacial water color
            "medium_green": "#6E9887",    #medium green like glacial algae
            "light_green": "#B9D6BC",     #light green like glacial ice with algae
            "background": "#EAEFD3",      #very light green for the background
            "text": "#1C3144"             #dark blue-green for text
        }
        
        self.root.configure(bg=self.colors["background"])
        
        self.score = 0
        self.current_question = 0
        self.time_limit = 120  #2 minutes total for all 30 questions
        self.time_remaining = self.time_limit
        self.timer_running = False
        
#all the glacier questions with options and correct answers - 30 total
        self.questions = [
            {
                "question": "What is the term for a mass of ice that moves slowly over land?",
                "options": ["Glacier", "Iceberg", "Firn", "Névé"],
                "answer": "Glacier"
            },
            {
                "question": "What type of glacier forms in mountain valleys?",
                "options": ["Valley glacier", "Ice sheet", "Piedmont glacier", "Cirque glacier"],
                "answer": "Valley glacier"
            },
            {
                "question": "What is the name for compressed granular snow that is in transition to glacial ice?",
                "options": ["Firn", "Névé", "Calving", "Moraine"],
                "answer": "Firn"
            },
            {
                "question": "What process occurs when pieces of ice break off from the end of a glacier?",
                "options": ["Calving", "Ablation", "Accumulation", "Plucking"],
                "answer": "Calving"
            },
            {
                "question": "What is the term for the balance between snow accumulation and ice loss in a glacier?",
                "options": ["Glacial budget", "Ice equilibrium", "Mass balance", "Glacial ratio"],
                "answer": "Mass balance"
            },
            {
                "question": "What feature is created when a glacier deposits a ridge of sediment?",
                "options": ["Moraine", "Esker", "Drumlin", "Kettle"],
                "answer": "Moraine"
            },
            {
                "question": "What is the name for a lake that forms in a cirque?",
                "options": ["Tarn", "Kettle lake", "Fjord", "Proglacial lake"],
                "answer": "Tarn"
            },
            {
                "question": "What glacial feature is a long, winding ridge of stratified sand and gravel?",
                "options": ["Esker", "Drumlin", "Arete", "Horn"],
                "answer": "Esker"
            },
            {
                "question": "What is the term for the process where a glacier picks up rocks as it moves?",
                "options": ["Plucking", "Abrasion", "Quarrying", "Scouring"],
                "answer": "Plucking"
            },
            {
                "question": "What type of moraine forms along the sides of a glacier?",
                "options": ["Lateral moraine", "Medial moraine", "Terminal moraine", "Ground moraine"],
                "answer": "Lateral moraine"
            },
            {
                "question": "What is the name for a pyramid-shaped peak formed by glacial erosion?",
                "options": ["Horn", "Arete", "Cirque", "Col"],
                "answer": "Horn"
            },
            {
                "question": "What process describes the melting and evaporation of glacial ice?",
                "options": ["Ablation", "Accumulation", "Calving", "Sublimation"],
                "answer": "Ablation"
            },
            {
                "question": "What is the term for a depression formed by a block of ice left by a glacier?",
                "options": ["Kettle", "Cirque", "Fjord", "Tarn"],
                "answer": "Kettle"
            },
            {
                "question": "What type of glacier spreads out from a central dome?",
                "options": ["Ice sheet", "Valley glacier", "Tidewater glacier", "Piedmont glacier"],
                "answer": "Ice sheet"
            },
            {
                "question": "What is the name for a sharp ridge between two cirques?",
                "options": ["Arete", "Horn", "Col", "Cirque"],
                "answer": "Arete"
            },
            {
                "question": "What glacial feature is a smooth, elongated hill formed by ice movement?",
                "options": ["Drumlin", "Esker", "Kame", "Moraine"],
                "answer": "Drumlin"
            },
            {
                "question": "What is the term for the process of rocks and sediment grinding against bedrock?",
                "options": ["Abrasion", "Plucking", "Quarrying", "Scouring"],
                "answer": "Abrasion"
            },
            {
                "question": "What type of moraine forms when two glaciers merge?",
                "options": ["Medial moraine", "Lateral moraine", "Terminal moraine", "Ground moraine"],
                "answer": "Medial moraine"
            },
            {
                "question": "What is the name for a glacier that ends in the ocean?",
                "options": ["Tidewater glacier", "Valley glacier", "Ice cap", "Piedmont glacier"],
                "answer": "Tidewater glacier"
            },
            {
                "question": "What feature is created when a glacier deposits sediment in a fan shape?",
                "options": ["Outwash plain", "Drumlin field", "Moraine", "Esker"],
                "answer": "Outwash plain"
            },
            {
                "question": "What is the term for the boundary between the zone of accumulation and ablation?",
                "options": ["Equilibrium line", "Terminus", "Ice divide", "Firn limit"],
                "answer": "Equilibrium line"
            },
            {
                "question": "What type of glacier forms at the base of mountains and spreads into lowlands?",
                "options": ["Piedmont glacier", "Valley glacier", "Ice sheet", "Cirque glacier"],
                "answer": "Piedmont glacier"
            },
            {
                "question": "What is the name for a deep crack in a glacier?",
                "options": ["Crevasse", "Bergschrund", "Moulin", "Randkluft"],
                "answer": "Crevasse"
            },
            {
                "question": "What glacial feature is a bowl-shaped depression at the head of a valley?",
                "options": ["Cirque", "Arete", "Horn", "Tarn"],
                "answer": "Cirque"
            },
            {
                "question": "What is the term for sediment deposited directly by glacial ice?",
                "options": ["Till", "Outwash", "Loess", "Varves"],
                "answer": "Till"
            },
            {
                "question": "What type of moraine marks the farthest advance of a glacier?",
                "options": ["Terminal moraine", "Lateral moraine", "Medial moraine", "Ground moraine"],
                "answer": "Terminal moraine"
            },
            {
                "question": "What is the name for a long, deep inlet formed by glacial erosion?",
                "options": ["Fjord", "Tarn", "Cirque", "Kettle"],
                "answer": "Fjord"
            },
            {
                "question": "What process describes the expansion of ice as water freezes in cracks?",
                "options": ["Frost wedging", "Plucking", "Abrasion", "Quarrying"],
                "answer": "Frost wedging"
            },
            {
                "question": "What is the term for a small glacier that occupies a bowl-shaped depression?",
                "options": ["Cirque glacier", "Valley glacier", "Ice cap", "Piedmont glacier"],
                "answer": "Cirque glacier"
            },
            {
                "question": "What feature is created when meltwater deposits sediment in tunnels under a glacier?",
                "options": ["Esker", "Drumlin", "Kame", "Moraine"],
                "answer": "Esker"
            }
        ]
        
#shuffle the questions so they appear in random order each time
        random.shuffle(self.questions)
        
        self.create_widgets()
        self.start_timer()
        self.show_question()
    
    def create_widgets(self):
#main title label at the top of the quiz window
        title_label = tk.Label(
            self.root, 
            text="Glacier Geology Quiz", 
            font=("Arial", 20, "bold"),
            fg=self.colors["text"],
            bg=self.colors["background"],
            pady=10
        )
        title_label.pack(pady=10)
        
#frame to hold the timer and score labels at the top
        info_frame = tk.Frame(self.root, bg=self.colors["background"])
        info_frame.pack(pady=5, fill=tk.X)
        
#label that shows the remaining time counting down
        self.timer_label = tk.Label(
            info_frame,
            text=f"Time: {self.time_remaining}s",
            font=("Arial", 14, "bold"),
            fg=self.colors["dark_green"],
            bg=self.colors["background"]
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)
        
#label that shows the current score out of total questions
        self.score_label = tk.Label(
            info_frame,
            text=f"Score: {self.score}/30",
            font=("Arial", 14, "bold"),
            fg=self.colors["dark_green"],
            bg=self.colors["background"]
        )
        self.score_label.pack(side=tk.RIGHT, padx=20)
        
#progress bar that shows how many questions have been completed
        self.progress = ttk.Progressbar(
            self.root,
            orient=tk.HORIZONTAL,
            length=600,
            mode='determinate',
            maximum=30
        )
        self.progress.pack(pady=10)
        
#label that shows current question number out of total
        self.question_number_label = tk.Label(
            self.root,
            text="Question 1 of 30",
            font=("Arial", 12),
            fg=self.colors["text"],
            bg=self.colors["background"]
        )
        self.question_number_label.pack(pady=5)
        
#frame where the actual question text is displayed
        self.question_frame = tk.Frame(
            self.root, 
            bg=self.colors["medium_green"],
            padx=20,
            pady=20,
            relief=tk.RAISED,
            bd=3
        )
        self.question_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
#label that shows the current question text
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=("Arial", 14),
            wraplength=600,
            justify=tk.LEFT,
            bg=self.colors["medium_green"],
            fg=self.colors["text"]
        )
        self.question_label.pack(pady=10)
        
#frame where the multiple choice option buttons are placed
        self.options_frame = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )
        self.options_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
#variable to track which option the user has selected
        self.selected_option = tk.StringVar()
        self.selected_option.set(None)
        
#button to submit the answer - starts disabled until an option is picked
        self.submit_button = tk.Button(
            self.root,
            text="Submit Answer",
            font=("Arial", 14),
            bg=self.colors["dark_green"],
            fg="white",
            command=self.check_answer,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.submit_button.pack(pady=10)
    
    def show_question(self):
#clear any previous option buttons from the options frame
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            
#update the question label with the current question text
            self.question_label.config(text=question_data["question"])
            
#update the question number label to show current progress
            self.question_number_label.config(text=f"Question {self.current_question + 1} of 30")
            
#update the progress bar to show how far along the user is
            self.progress['value'] = self.current_question
            
#get the options for this question and shuffle them
            options = question_data["options"]
            random.shuffle(options)
            
#create radio buttons for each option
            for option in options:
                rb = tk.Radiobutton(
                    self.options_frame,
                    text=option,
                    variable=self.selected_option,
                    value=option,
                    font=("Arial", 12),
                    bg=self.colors["background"],
                    fg=self.colors["text"],
                    selectcolor=self.colors["light_green"],
                    activebackground=self.colors["light_green"],
                    command=self.enable_submit
                )
                rb.pack(anchor=tk.W, pady=5, padx=50)
        
        else:
            self.end_quiz()
    
    def enable_submit(self):
#enable the submit button once user has selected an option
        self.submit_button.config(state=tk.NORMAL)
    
    def check_answer(self):
        selected = self.selected_option.get()
        correct = self.questions[self.current_question]["answer"]
        
        if selected == correct:
            self.score += 1
            messagebox.showinfo("Result", "Correct! ✅")
        else:
            messagebox.showerror("Result", f"Incorrect. The correct answer is: {correct}")
        
        self.current_question += 1
        self.score_label.config(text=f"Score: {self.score}/30")
        self.selected_option.set(None)
        self.submit_button.config(state=tk.DISABLED)
        
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.end_quiz()
    
    def start_timer(self):
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        if self.timer_running and self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.config(text=f"Time: {self.time_remaining}s")
            self.root.after(1000, self.update_timer)
        elif self.time_remaining <= 0:
            self.timer_running = False
            messagebox.showwarning("Time's Up!", "Time has run out!")
            self.end_quiz()
    
    def end_quiz(self):
        self.timer_running = False
        
#calculate the percentage score based on correct answers
        percentage = (self.score / 30) * 100
        
#determine the letter grade based on percentage
        if percentage >= 90:
            grade = "A"
            message = "Excellent! You're a glacier expert! ❄️"
        elif percentage >= 80:
            grade = "B"
            message = "Great job! You know your glaciers! ⛰️"
        elif percentage >= 70:
            grade = "C"
            message = "Good effort! Keep learning about glaciers! 🌊"
        elif percentage >= 60:
            grade = "D"
            message = "Not bad, but you could use more study! 📚"
        else:
            grade = "F"
            message = "Keep studying glaciers - you'll get there! 💪"
        
#show the final results with score, percentage, and grade
        result_text = f"Quiz Complete!\n\nScore: {self.score}/30\nPercentage: {percentage:.1f}%\nGrade: {grade}\n\n{message}"
        messagebox.showinfo("Quiz Results", result_text)
        
#ask if the user wants to play the quiz again
        play_again = messagebox.askyesno("Play Again?", "Would you like to play again?")
        if play_again:
            self.reset_quiz()
        else:
            self.root.quit()
    
    def reset_quiz(self):
#reset all game variables to start a new quiz
        self.score = 0
        self.current_question = 0
        self.time_remaining = self.time_limit
        random.shuffle(self.questions)
        self.score_label.config(text=f"Score: {self.score}/30")
        self.timer_label.config(text=f"Time: {self.time_remaining}s")
        self.progress['value'] = 0
        self.start_timer()
        self.show_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = GlacierQuizGame(root)
    root.mainloop()