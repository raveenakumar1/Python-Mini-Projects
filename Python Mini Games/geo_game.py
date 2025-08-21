
import tkinter as tk
from tkinter import messagebox
import random
import math

class GeometryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Geometry Math Game")
        self.root.geometry("550x450")
        
#green colors for the game interface
        self.colors = {
            "dark_green": "#2E8B57",      
            "medium_green": "#66CDAA",    
            "light_green": "#98FB98",     
            "background": "#F5F5F5",      
            "text": "#003300"             
        }
        
        self.root.configure(bg=self.colors["background"])
        
        self.score = 0
        self.total_questions = 0
        self.current_problem = None
        
        self.create_widgets()
        self.generate_problem()
    
    def create_widgets(self):
#main title label for the game
        title_label = tk.Label(
            self.root, 
            text="Geometry Math Challenge", 
            font=("Arial", 18, "bold"),
            fg=self.colors["text"],
            bg=self.colors["background"],
            pady=10
        )
        title_label.pack(pady=10)
        
#frame where the problem will be displayed
        self.problem_frame = tk.Frame(
            self.root, 
            bg=self.colors["medium_green"],
            padx=20,
            pady=20,
            relief=tk.RAISED,
            bd=3
        )
        self.problem_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.problem_label = tk.Label(
            self.problem_frame,
            text="",
            font=("Arial", 14),
            wraplength=450,
            justify=tk.LEFT,
            bg=self.colors["medium_green"],
            fg=self.colors["text"]
        )
        self.problem_label.pack(pady=10)
        
#frame for the answer input area
        answer_frame = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )
        answer_frame.pack(pady=10)
        
        tk.Label(
            answer_frame,
            text="Your Answer:",
            font=("Arial", 12, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(side=tk.LEFT, padx=5)
        
        self.answer_entry = tk.Entry(
            answer_frame,
            font=("Arial", 12),
            width=15,
            bg=self.colors["light_green"]
        )
        self.answer_entry.pack(side=tk.LEFT, padx=5)
        self.answer_entry.bind("<Return>", self.check_answer)
        
#buttons for checking answer and getting next problem
        button_frame = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )
        button_frame.pack(pady=10)
        
        check_button = tk.Button(
            button_frame,
            text="Check Answer",
            font=("Arial", 12),
            bg=self.colors["dark_green"],
            fg="white",
            command=self.check_answer,
            padx=15,
            pady=5,
            activebackground=self.colors["medium_green"]
        )
        check_button.pack(side=tk.LEFT, padx=5)
        
        next_button = tk.Button(
            button_frame,
            text="Next Problem",
            font=("Arial", 12),
            bg=self.colors["medium_green"],
            fg=self.colors["text"],
            command=self.generate_problem,
            padx=15,
            pady=5,
            activebackground=self.colors["light_green"]
        )
        next_button.pack(side=tk.LEFT, padx=5)
        
#score display at the bottom
        score_frame = tk.Frame(
            self.root,
            bg=self.colors["dark_green"],
            padx=10,
            pady=5
        )
        score_frame.pack(pady=10)
        
        self.score_label = tk.Label(
            score_frame,
            text="Score: 0/0",
            font=("Arial", 12, "bold"),
            bg=self.colors["dark_green"],
            fg="white"
        )
        self.score_label.pack()
    
    def generate_problem(self):
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        
#randomly pick a type of geometry problem
        problem_type = random.choice([
            "circle_area", 
            "circle_circumference", 
            "triangle_area", 
            "rectangle_area",
            "pythagorean",
            "volume_cube",
            "volume_sphere"
        ])
        
        if problem_type == "circle_area":
            radius = random.randint(1, 20)
            correct_answer = math.pi * radius ** 2
            self.current_problem = {
                "question": f"Calculate the area of a circle with radius {radius} units.",
                "answer": round(correct_answer, 2)
            }
            
        elif problem_type == "circle_circumference":
            radius = random.randint(1, 15)
            correct_answer = 2 * math.pi * radius
            self.current_problem = {
                "question": f"Find the circumference of a circle with radius {radius} units.",
                "answer": round(correct_answer, 2)
            }
            
        elif problem_type == "triangle_area":
            base = random.randint(5, 20)
            height = random.randint(5, 20)
            correct_answer = 0.5 * base * height
            self.current_problem = {
                "question": f"Calculate the area of a triangle with base {base} units and height {height} units.",
                "answer": round(correct_answer, 2)
            }
            
        elif problem_type == "rectangle_area":
            length = random.randint(5, 25)
            width = random.randint(5, 25)
            correct_answer = length * width
            self.current_problem = {
                "question": f"Find the area of a rectangle with length {length} units and width {width} units.",
                "answer": correct_answer
            }
            
        elif problem_type == "pythagorean":
            a = random.randint(3, 12)
            b = random.randint(3, 12)
            c = math.sqrt(a**2 + b**2)
#sometimes ask for hypotenuse, sometimes for a side
            choice = random.randint(1, 3)
            if choice == 1:
                self.current_problem = {
                    "question": f"In a right triangle, if side a = {a} and side b = {b}, what is the length of the hypotenuse?",
                    "answer": round(c, 2)
                }
            else:
                c = random.randint(5, 15)
                a = random.randint(3, c-1)
                b = math.sqrt(c**2 - a**2)
                self.current_problem = {
                    "question": f"In a right triangle, if side a = {a} and hypotenuse c = {c}, what is the length of side b?",
                    "answer": round(b, 2)
                }
            
        elif problem_type == "volume_cube":
            side = random.randint(3, 15)
            correct_answer = side ** 3
            self.current_problem = {
                "question": f"Calculate the volume of a cube with side length {side} units.",
                "answer": correct_answer
            }
            
        elif problem_type == "volume_sphere":
            radius = random.randint(2, 10)
            correct_answer = (4/3) * math.pi * radius ** 3
            self.current_problem = {
                "question": f"Find the volume of a sphere with radius {radius} units.",
                "answer": round(correct_answer, 2)
            }
        
        self.problem_label.config(text=self.current_problem["question"])
    
    def check_answer(self, event=None):
        if self.current_problem is None:
            return
            
        user_answer = self.answer_entry.get()
        if not user_answer:
            messagebox.showwarning("Input Error", "Please enter an answer.")
            return
            
        try:
            user_answer = float(user_answer)
            correct_answer = self.current_problem["answer"]
            
#allow for small rounding differences in floating point answers
            is_correct = abs(user_answer - correct_answer) < 0.1
            
            self.total_questions += 1
            if is_correct:
                self.score += 1
                messagebox.showinfo("Result", "Correct! 🎉")
            else:
                messagebox.showerror("Result", f"Incorrect. The correct answer is {correct_answer}.")
                
            self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number.")
            return

if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryGame(root)
    root.mainloop()