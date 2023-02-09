## Create a quiz app with a GUI using Tkinter

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import pandas as pd

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

        #self.logo = PhotoImage(file = "logo.png")
        #ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2)
        ttk.Label(self.frame_header, text = "Quiz", style = "Header.TLabel").grid(row = 0, column = 1)
        ttk.Label(self.frame_header, text = "").grid(row = 1, column = 2)

        self.bank = self.quiz_bank()
        self.questions = []
        self.correct_answers = []
        self.answers = []
        
        for k in list(self.bank.keys())[-1:0:-1]:
            print(k)
            self.questions += self.bank[k]['Question']
            self.correct_answers += self.bank[k]['Correct Answer'] 
            self.answers += self.bank[k]['answers']
        

        self.edition = -1
        self.var = StringVar()
        self.var.set('0')

        self.question_number = 0
        self.score = 0

        # Edition 
        ttk.Label(self.frame_header, wraplength = 300,
                text = (list(self.bank.keys())[-1])).grid(row = 1, column = 1)

        # Add left and right padding to the frame
        self.frame_content.grid_columnconfigure(0, weight = 1)
        self.frame_content.grid_columnconfigure(1, weight = 1)
        self.frame_content.grid_columnconfigure(2, weight = 1)


        self.question = ttk.Label(self.frame_content, text = self.questions[self.question_number])
        self.question.grid(row = 0, column = 0,  pady = 20)
        self.radio_one = ttk.Radiobutton(self.frame_content, text = self.answers[self.question_number][0],
                                        variable = self.var, value = self.answers[self.question_number][0])
        self.radio_one.grid(row = 1, column = 0, sticky = W, padx = 20)

        self.radio_two = ttk.Radiobutton(self.frame_content, text = self.answers[self.question_number][1],
                                        variable = self.var, value = self.answers[self.question_number][1])  
        self.radio_two.grid(row = 2, column = 0, sticky = W, padx = 20)

        self.radio_three = ttk.Radiobutton(self.frame_content, text = self.answers[self.question_number][2],
                                        variable = self.var, value = self.answers[self.question_number][2])
        self.radio_three.grid(row = 3, column = 0, sticky = W, padx = 20)

        self.radio_four = ttk.Radiobutton(self.frame_content, text = self.answers[self.question_number][3],
                                        variable = self.var, value = self.answers[self.question_number][3])
        self.radio_four.grid(row = 4, column = 0, sticky = W, padx = 20)


        self.button_frame = ttk.Frame(self.frame_content)
        self.button_frame.grid(row = 5, column = 0, pady = 10)
        # Add left and right padding to the frame
        self.button_frame.grid_columnconfigure(0, weight = 1)
        self.button_frame.grid_columnconfigure(1, weight = 1)
        self.button_frame.grid_columnconfigure(2, weight = 1)


        self.button_submit = ttk.Button(self.button_frame, text = "Submit", command = self.submit)
        self.button_submit.grid(row = 0, column = 0, padx = 20)

        self.button_next = ttk.Button(self.button_frame, text = "Next", command = self.next)
        self.button_next.grid(row = 0, column = 1, padx = 20)

        self.button_quit = ttk.Button(self.button_frame, text = "Quit", command = self.quit)
        self.button_quit.grid(row = 0, column = 2, padx = 20)

    
        # Add score label
        self.score_label = ttk.Label(self.frame_content, text = "Score: 0")
        self.score_label.grid(row = 7, column = 0, pady = 20)


    def quiz_bank(self):
        """
        After means that there are specific questions asked from 1966
        """
        # Questions
        question_1,question_2,question_3,question_4, question_5 = "Quel est le pays organisateur ?",
        "Quel est le pays vainqueur ?",
        "Quel est le nombre de pays participants ?",
        "Qui était le meilleur buteur ?",
        "Quelle est la mascotte ?"

        questions = [question_1, question_2, question_3, question_4]
        questions_after = [question_1, question_2, question_5, question_4]
    
        def fill_answers(df, val, after=False):
            if after:
                col=['countryLabel', 'winnerLabel','mascotLabel','leaderLabel']
            else:
                col=['countryLabel','winnerLabel','participantsLabel','leaderLabel']

            dict={}
            for col in col:
                answers=df[df[col]!=val[col]][col].to_list()
                unique_answers=list(set(answers))
                alt_answers=random.sample(unique_answers,3)
                alt_answers.append(val[col])
                random.shuffle(alt_answers)
                dict[col]=alt_answers
                
            return list(dict.values())

    
        df = pd.read_csv('data.csv')
        df['participantsLabel'] = df['participantsLabel'].astype(str)
        quiz_bank = {}
        for _,val in df.iterrows(): #['itemLabel.value'].unique():
            r_answer_1,r_answer_2,r_answer_3,r_answer_4, r_answer_5 = val['countryLabel'],val['winnerLabel'],val['participantsLabel'],val['leaderLabel'], val['mascotLabel']
            answers = [r_answer_1,r_answer_2,r_answer_3,r_answer_4]
            alt_answers=fill_answers(df,val)
            answers_after = [r_answer_1,r_answer_2,r_answer_5,r_answer_4]
            alt_answers_after =fill_answers(df,val)

            # differentiate between before 1966 and after
            if val['itemLabel'] < '1966 FIFA World Cup':
                quiz_bank[val['itemLabel']] = {"Question": questions, "Correct Answer": answers, "answers": alt_answers}

            else:
                quiz_bank[val['itemLabel']] = {"Question": questions_after, "Correct Answer": answers_after, "answers": alt_answers_after}

        return quiz_bank

    def submit(self):
            '''Check the answer and display the result'''
    
            if self.var.get() == self.correct_answers[self.question_number]:
                self.score += 1
                self.score_label.config(text = "Score: {}".format(self.score))
                # messagebox.showinfo("Correct", "Your answer is correct!")
                self.next()
            # else:
                # messagebox.showinfo("Incorrect", "Your answer is incorrect!, Try again ...")

    def next(self):
        '''Go to the next question'''
        #print(self.var.get(),self.question_number)
        self.var.set(0)
        self.question_number += 1
        # Update edition
        if self.question_number %4 == 0:
            self.edition -= 1
            ttk.Label(self.frame_header, wraplength = 300,
                text = (list(self.bank.keys())[self.edition])).grid(row = 1, column = 1)

        if self.question_number == len(self.questions):
            messagebox.showinfo("Quiz completed", "Your score is {}/{}".format(self.score, self.question_number))
            if self.score == self.question_number:
                messagebox.showinfo("Congratulations", "And you got a Strike !")
            self.parent.destroy()
        else:
            self.question.config(text = self.questions[self.question_number])
            self.radio_one.config(text = self.answers[self.question_number][0],
                                value = self.answers[self.question_number][0])
            self.radio_two.config(text = self.answers[self.question_number][1],
                                value = self.answers[self.question_number][1])
            self.radio_three.config(text = self.answers[self.question_number][2],
                                value = self.answers[self.question_number][2])
            self.radio_four.config(text = self.answers[self.question_number][3],
                                value = self.answers[self.question_number][3])

    def quit(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = Tk()
    quiz = Quiz(root)
    root.mainloop()


