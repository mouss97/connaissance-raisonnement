## Create a quiz app with a GUI using Tkinter

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random

class Quiz:
    
    def __init__(self, parent):

        '''Use the init method for all the main containers'''

        self.parent = parent
        self.parent.title("Quiz")
        self.parent.geometry("500x500")
        self.parent.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TFrame", background = "white")
        self.style.configure("TButton", background = "white")
        self.style.configure("TLabel", background = "white", font = ("Arial", 11))
        self.style.configure("Header.TLabel", font = ("Arial", 18, "bold"))

        self.frame_header = ttk.Frame(self.parent)
        self.frame_header.pack()

        self.frame_content = ttk.Frame(self.parent)
        self.frame_content.pack()

        self.logo = PhotoImage(file = "logo.png")
        ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2)
        ttk.Label(self.frame_header, text = "Quiz", style = "Header.TLabel").grid(row = 0, column = 1)
        ttk.Label(self.frame_header, wraplength = 300,
                text = ("Choose the right option from the list to answer the question. "
                        "You can select only one option at a time.")).grid(row = 1, column = 1)

        self.questions = ["What is the capital of France?",
                        "What is the capital of Germany?",
                        "What is the capital of Spain?",
                        "What is the capital of Italy?",
                        "What is the capital of Poland?"]

        self.correct_answers = [2, 3, 1, 2, 1]

        self.answers = [[("Paris", 1), ("Berlin", 2), ("Madrid", 3), ("Rome", 4)],
                        [("Paris", 1), ("Berlin", 2), ("Madrid", 3), ("Rome", 4)],
                        [("Paris", 1), ("Berlin", 2), ("Madrid", 3), ("Rome", 4)],
                        [("Paris", 1), ("Berlin", 2), ("Madrid", 3), ("Rome", 4)],
                        [("Paris", 1), ("Berlin", 2), ("Madrid", 3), ("Rome", 4)]]

        self.var = IntVar()
        self.var.set(0)

        self.question_number = 0
        self.score = 0

        self.question = ttk.Label(self.frame_content, text = self.questions[self.question_number])
        self.question.grid(row = 0, column = 0, padx = 20)

        self.radio_one = ttk.Radiobutton(self.frame_content, text = self.answers[self.question_number][0][0],
                                        variable = self.var, value = self.answers[self.question_number][0][1])
        self.radio_one.grid(row = 1, column = 0, sticky = W, padx = 20)

        self.radio_two = ttk.Radiobutton(self.frame_content, text = self.answers[self.question_number][1][0],
                                        variable = self.var, value = self.answers[self.question_number][1][1])  
        self.radio_two.grid(row = 2, column = 0, sticky = W, padx = 20)

        self.radio_three = ttk.Radiobutton(self.frame_content, text = self.answers[self.question_number][2][0],
                                        variable = self.var, value = self.answers[self.question_number][2][1])
        self.radio_three.grid(row = 3, column = 0, sticky = W, padx = 20)

        self.radio_four = ttk.Radiobutton(self.frame_content, text = self.answers[self.question_number][3][0],
                                        variable = self.var, value = self.answers[self.question_number][3][1])
        self.radio_four.grid(row = 4, column = 0, sticky = W, padx = 20)

        self.button_frame = ttk.Frame(self.frame_content)
        self.button_frame.grid(row = 5, column = 0, pady = 10)

        self.button_submit = ttk.Button(self.button_frame, text = "Submit", command = self.submit)
        self.button_submit.grid(row = 0, column = 0, padx = 50)

        self.button_next = ttk.Button(self.button_frame, text = "Next", command = self.next)
        self.button_next.grid(row = 0, column = 1, padx = 50)

        self.button_quit = ttk.Button(self.button_frame, text = "Quit", command = self.quit)
        self.button_quit.grid(row = 0, column = 2, padx = 50)

    def submit(self):
            
            '''Check the answer and display the result'''
    
            if self.var.get() == self.correct_answers[self.question_number]:
                self.score += 1
                messagebox.showinfo("Correct", "Your answer is correct!")
            else:
                messagebox.showinfo("Incorrect", "Your answer is incorrect!")

    def next(self):
                
        '''Go to the next question'''

        self.var.set(0)
        self.question_number += 1

        if self.question_number == len(self.questions):
            messagebox.showinfo("Quiz completed", "Your score is {}/{}".format(self.score, self.question_number))
            self.parent.destroy()
        else:
            self.question.config(text = self.questions[self.question_number])
            self.radio_one.config(text = self.answers[self.question_number][0][0],
                                value = self.answers[self.question_number][0][1])
            self.radio_two.config(text = self.answers[self.question_number][1][0],
                                value = self.answers[self.question_number][1][1])
            self.radio_three.config(text = self.answers[self.question_number][2][0],
                                value = self.answers[self.question_number][2][1])
            self.radio_four.config(text = self.answers[self.question_number][3][0],
                                value = self.answers[self.question_number][3][1])

    def quit(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = Tk()
    quiz = Quiz(root)
    root.mainloop()

# I have a problem with the code above. I want to make the radio buttons to be disabled after the user submits the answer. I tried to use the state = DISABLED but it doesn't work. I also tried to use the .configure() method but it doesn't work either. I would appreciate any help.


