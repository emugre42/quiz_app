#this is the file where the UI is created for the app. this file includes the design and the function of the app

from doctest import master
from random import choice
from re import X
from tkinter import BOTTOM, TOP, Y, Entry, Tk, Canvas, StringVar, Label, Radiobutton, Button, messagebox, Frame
from tkinter.constants import S
from unittest.main import main
from quiz_brain import QuizBrain
from time import time, strftime
from question_bank_db import *

THEME_COLOR = "#375362"

class QuizInterface(Frame):

    def __init__(self, quiz_brain, master, main):
        Frame.__init__(self, master)
        self.main = main
        self.master = master
        self.quiz = quiz_brain

        #Display title
        self.display_title()

        #Creating a canvas for question text, and display question
        self.canvas = Canvas(self, width=800, height=500)
        self.question_text = self.canvas.create_text(400, 80, 
                                                     text="Question here",
                                                     width=680, fill=THEME_COLOR,
                                                     font=('Century Gothic', 15, 'italic')
                                                     )
        self.canvas.pack(side=TOP)
        self.display_question()

        #Declare a StringVar to store the answers
        self.user_answer = StringVar(self)

        #Display four options
        self.opts = self.radio_buttons()
        self.display_options()

        #To show if the answer is correct
        self.feedback = Label(self, font=("ariel", 15, "bold"))
        self.feedback.place(x=300, y=20)

        #Next and Quit Buttons
        self.buttons()

    
    def display_title(self):
        """To display title"""

        #Title
        title = Label(self, text="Quiz Application for the Coursework",
                      width=55, bg="blue", fg="white", font=("Bahnschrift", 20, "bold"))
        title.place(x=0, y=2)
    
    def display_question(self):
        """To display the question"""

        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)
    
    def radio_buttons(self):
        """To create the options"""
        #initialize the list with an empty list
        choice_list = []

        #position of the first option
        y_pos = 115

        #adding the options to the list
        while len(choice_list) < 4:

            #setting the radiobutton properties
            radio_btn = Radiobutton(self, text="", variable=self.user_answer,
                                    value='', font=("Century Gothic", 14))
            radio_btn.place(x=200, y=y_pos)

            #adding the button to the list
            choice_list.append(radio_btn)

            #incrementing the y-axis by 40
            y_pos += 40
            
        return choice_list

    def display_options(self):
        """To display four options"""

        val = 0

        #deselecting the options
        self.user_answer.set(None)

        #looping over the options to be displayed
        for option in self.quiz.current_question.choices:
            self.opts[val] ['text'] = option
            self.opts[val] ['value'] = option
            val += 1

    def next_btn(self):
        """To show feedback and check for more questions"""

        #Check if the answer is correct
        if self.quiz.check_answer(self.user_answer.get()):
            self.feedback["fg"] = "green"
            self.feedback["text"] = 'Great, correct answer! \U0001F44D'
        else:
            self.feedback['fg'] = 'red'
            self.feedback['text'] = ('\u274E Oops!'
                                     f'The right answer is: {self.quiz.current_question.correct_answer}')
        
        if self.quiz.has_more_questions():
            #Moves to the next question
            self.display_question()
            self.display_options()
        else:
            #if no more questions, display the score
            self.display_result()

            #exits the quiz and goes back to the main screen
            self.main.pack()
            self.pack_forget()
    
    def buttons(self):
        """To show the next and quit buttons"""

        #next question
        next_button = Button(self, text="Next", command=self.next_btn,
                             width=10, bg="green", fg="white", font=("ariel", 16, "bold"))
        next_button.place(x=50, y=10)

        #quit button
        quit_button = Button(self, text="Quit", command=self.back,
                             width=5, bg="red", fg="white", font=("ariel", 16, "bold"))
        quit_button.place(x=700, y=10)

    def back(self):
        self.main.pack()
        self.pack_forget()

    def display_result(self):
        """To display the result"""
        correct, wrong, score_percent = self.quiz.get_score()
        
        #saves the result in previus results page
        store_result = "{}/{}".format(correct, correct + wrong)
        date = strftime('%d/%m/%y -- %H:%M:%S:')
        insert_result(store_result, date)

        correct = f"Correct: {correct}"
        wrong = f"Wrong: {wrong}"

        #calculates the percentage of the answers
        result = f"Score: {score_percent}%"

        #shows a message box to display the result
        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")

        #creates a text file where the results are stored
        filename = 'results.txt'
        data = 'Correct Answer: '+correct+'\nWrong Answer: '+wrong+'\nScore: '+str(score_percent)+'%'+'\nCompleted quiz at: '+strftime('%d/%m/%y -- %H:%M:%S:')
        with open(filename, 'a') as file:
            file.write(data)

