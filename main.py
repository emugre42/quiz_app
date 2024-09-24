#this is for enabling to edit the questions, such as selecting, deleting, updating, etc. In addition, the app should be run on this page.
from cProfile import label
from cgitb import text
from distutils import text_file
from doctest import master
from logging import root
from logging.handlers import QueueListener
from multiprocessing.connection import answer_challenge
from select import select
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox, Treeview
from unicodedata import category
from unittest import result
from question_bank_db import *
from quiz_ui import *
from question_model import Question
from quiz_data import question_data
from quiz_brain import QuizBrain
from random import choices, shuffle
from quiz_ui import QuizInterface
from tkinter.filedialog import asksaveasfile
import html

#for gathering everything from other pages needed to launch the program
question_bank = []
for question in question_data:
    choices = []
    question_text = html.unescape(question["question"])
    correct_answer = html.unescape(question["correct_answer"])
    incorrect_answers = question["incorrect_answers"]
    for ans in incorrect_answers:
        choices.append(html.unescape(ans))
    choices.append(correct_answer)
    shuffle(choices)
    new_question = Question(question_text, correct_answer, choices)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

#the title and the size of the app 
class Root(Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz App for the Coursework")
        self.geometry("800x800")

#the welcome screen of the app
class Main(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.label = Label(self, text="WELCOME TO THE QUIZ", fg="white", bg="blue", width=30, font=("Century Gothic", 15))
        self.label.pack(padx=30, pady=30)

        self.module_button = Button(self, text="Edit your Modules", command=self.edit_module, width=30, height=5)
        self.module_button.pack(padx=30, pady=30)

        self.edit_button = Button(self, text="Edit your Questions", command=self.edit, width=30, height=5)
        self.edit_button.pack(padx=30, pady=30)

        self.result_button = Button(self, text="See your Previous Results", command=self.see_result, width=30, height=5)
        self.result_button.pack(padx=30, pady=30)
        
        self.quiz_button = Button(self, text="Start the Quiz", command=self.start_quiz, width=30, height=5)
        self.quiz_button.pack(padx=30, pady=30)

        self.quit_button = Button(self, text="Quit", command=self.master.destroy, width=30, height=5)
        self.quit_button.pack(padx=30, pady=30)

#to direct to the results page when click on "See the Previous Results" button
    def see_result(self):
        result = Results(root)
        result.pack()
        result.refresh()
        main.pack_forget()     

#to direct to the edit question page when click on "Edit your Questions" button    
    def edit(self):
        question.pack()
        question.refresh()
        main.pack_forget()
    
    def edit_module(self):
        module.pack()
        module.refresh()
        main.pack_forget()

#to start the quiz when clicking on "Start the Quiz" button
    def start_quiz(self):
        quiz_ui = QuizInterface(quiz, root, main)
        quiz_ui.pack()
        self.pack_forget()

root = Root()
main = Main(root)
main.pack()

#functions of the layout of the app
class GenericTree(Frame):
    def __init__(self, master, dict, items):
        Frame.__init__(self, master)
        self.master = master
        keys = dict.keys()
        self.items = items

        self.columns = list(keys)
        self.tree = Treeview(self.master, columns = self.columns, show="headings", height=20)
        self.tree.pack()
        for key in keys:
            self.tree.heading(key, text=dict[key], anchor=CENTER)
        self.refresh(items)

    def insrt(self, values):
        self.tree.insert('', END, values=values)

    def refresh(self, items):
        self.delete_all()
        for item in items:
            self.insrt(item)

    def delete_all(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
    
    def selected_item(self):
        selected_item = self.tree.selection()
        return selected_item

#class for buttons
class GenericButtons(Frame):
    def __init__(self, master, add, delete, answer_button, back):
        Frame.__init__(self, master)
        self.master = master

        self.add_bttn = Button(self, text="Add", command=add)
        self.add_bttn.grid(row=0, column=0)

        self.add_an_answer_button = Button(self, text="Add an Answer", command=answer_button)
        self.add_an_answer_button.grid(row=0, column=1, padx=10)

        delete_button = Button(self, text="Delete", command=delete)
        delete_button.grid(row=0, column=2)

        b_button = Button(self, text="Back", command=back)
        b_button.grid(row=0, column=3, padx=10)

        self.q_button = Button(self, text="Quit", command=self.close)
        self.q_button.grid(row=0, column=4)
    

    def close(self):
        root.destroy()

# functions to add a module
class AddModule(Toplevel):
    def _init_(self, master, module_category, module_type):
        Toplevel.__init__(self, master)
        self.master = master
        self.geometry("600x460")
        label = Label(self, text="Add Question")
        label.pack()

        self.text = Text(self)
        self.text.pack()

        self.module_category = Combobox(self, values=module_category)
        self.module_category.pack()

        self.module_type = Combobox(self, values=module_type)
        self.module_type.pack()
        
        addbttn = Button(self, text="Add", command=self.add)
        addbttn.pack()

    def add(self):
        module_type = self.module_type.get()
        module_category = self.module_category.get()
        text = self.text.get("1.0", 'end')
        insert_question(text, module_category, module_type)
        module.refresh()
        self.destroy()

class Module(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.module_dictionary = {'module' : 'Module Name',
            'module_category': 'Category',
            'module_type': 'Type'
            }
        self.module = get_module()
        self.tree = GenericTree(self, self.module_dictionary, self.module)
        self.tree.pack()
        self.button = GenericButtons(self, self.add_mdl, self.delete_mdl, lambda:None, self.back)
        self.button.add_an_answer_button.destroy()
        self.button.pack()
        
    def back(self):
        main.pack()
        self.pack_forget()

    def add_mdl(self):

        self.module_category = [
            'Science: Computers',
            'Science: Mathematics',
            'General Knowledge']
    
        self.module_type = [
            'Multiple',
            'True/False'
        ]

        AddModule(self, self.module_category, self.module_type)

    def delete_mdl(self):
        item = self.tree.selected_item()[0]
        itm = item
        itm = self.tree.tree.item(itm)['values']
        self.module_category = itm[0]
        self.module_type = itm[2]
        delete_question(self.module_category, self.module_type)
        self.refresh()

    def refresh(self):
        self.tree.refresh(get_module())

#functions to add a question
class AddQuestion(Toplevel):
    def __init__(self, master, question_category, question_type):
        Toplevel.__init__(self, master)
        self.master = master
        self.geometry("600x600")
        label = Label(self, text="Add Question")
        label.pack()

        self.text = Text(self)
        self.text.pack()

        self.question_type = Combobox(self, values=question_type)
        self.question_type.pack()

        self.question_category = Combobox(self, values=question_category)
        self.question_category.pack()

        addbttn = Button(self, text="Add", command=self.add)
        addbttn.pack()
    
    def add(self):
        question_type = self.question_type.get()
        question_category = self.question_category.get()
        text = self.text.get("1.0", 'end')
        insert_question(text, question_category, question_type)
        question.refresh()
        self.destroy()

#functions to add an answer to a question
class AddAnswers(Toplevel):
    def __init__(self, master, answer_is_correct, question_id):
        Toplevel.__init__(self, master)
        self.master = master
        self.geometry("600x460")
        label = Label(self, text="Add an Answer")
        label.pack()

        self.question_id = question_id

        self.answer_description = Text(self)
        self.answer_description.pack()

        self.answer_is_correct = Combobox(self, values=answer_is_correct)
        self.answer_is_correct.pack()

        answer_bttn = Button(self, text="Add", command=self.answer_button)
        answer_bttn.pack()


    def answer_button(self):
        answer_description = self.answer_description.get("1.0", 'end')
        answer_is_correct = self.answer_is_correct.get()
        if answer_is_correct == "Correct":
            insert_answer(answer_description, "Correct", self.question_id)
        elif answer_is_correct == "Wrong":
            insert_answer(answer_description, "Wrong", self.question_id)

        self.master.refresh()
        self.destroy()

#functions to see the results of the quiz
class Results(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.result_list = {'result': 'Result', 
            'date': 'Date'
            }
        self.rslt = get_result()
        self.tree = GenericTree(self, self.result_list, self.rslt)
        self.tree.pack()
        self.bttn = GenericButtons(self, lambda:None, self.dlt_result, lambda:None, self.back)
        self.bttn.add_bttn.destroy()
        self.bttn.add_an_answer_button.destroy()
        self.bttn.q_button.destroy()
        self.bttn.pack()

        #the button to save the result
        print_button = Button(self, text="Save the result", command=self.print)
        print_button.pack(pady=10)

    #the function for saving the result
    def print(self):
        files = [('All Files', '*.*'),
                        ('Python Files', '*.py'),
                        ('Text Document', '*.txt')]
        file = filedialog.asksaveasfile(filetypes=files, defaultextension=files)

    def back(self):
        main.pack()
        self.pack_forget()
    
    def dlt_result(self):
        item = self.tree.selected_item()[0]
        itm = item
        itm = self.tree.tree.item(itm)['values']
        self.rslt = itm[0]
        self.result_date = itm[1]
        delete_result(self.rslt, self.result_date)
        self.refresh()

    def refresh(self):
        self.tree.refresh(get_result())

#functions to see the answers of a question
class Answers(Frame):
    def __init__(self, master, id):
        Frame.__init__(self, master)
        self.master = master
        answer_dictionary = {'description' : 'Description',
                        'is_correct' : 'Correct or Wrong',
                        'question_id': 'Question Number'}
        self.id = id
        self.answers = get_answers(id)

        self.tree = GenericTree(self, answer_dictionary, self.answers)
        self.tree.pack()
        self.button = GenericButtons(self, self.add_answer, self.dlt_answer, self.add_an_answer, self.back)
        self.button.pack()

    def back(self):
        question.pack()
        question.refresh()
        self.pack_forget()

    def add_answer(self):
        AddAnswers(self, ['Correct', 'Wrong'], self.id)

    def dlt_answer(self):
        item = self.tree.selected_item()[0]
        itm = item
        itm = self.tree.tree.item(itm)['values']
        answer_description = itm[0]
        answer_is_correct = itm[1]
        delete_answer(answer_description, answer_is_correct)
        self.refresh()

    def add_an_answer(self):
        pass

    def refresh(self):
        self.answers = get_answers(self.id)
        print(self.answers)
        self.tree.refresh(self.answers)

#functions to see the questions
class Question(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.dictnry = {'question': 'Questions', 
            'category': 'Category',
            'type': 'Type'
            }
        self.result = get_question()
        self.tree = GenericTree(self, self.dictnry, self.result)
        self.tree.pack()
        self.button = GenericButtons(self, self.add, self.delete, self.add_the_answer, self.back)
        self.button.pack()
        
    def back(self):
        main.pack()
        self.pack_forget()

    def add(self):
        self.category = [
            'Science: Computers',
            'Science: Mathematics',
            'General Knowledge']
    
        self.type = [
            'Multiple',
            'True/False'
        ]
        
        AddQuestion(self, self.category, self.type)

    def delete(self):
        item = self.tree.selected_item()[0]
        itm = item
        itm = self.tree.tree.item(itm)['values']
        self.question = itm[0]
        self.category = itm[1]
        self.type = itm[2]
        delete_question(self.question, self.category, self.type)
        self.refresh()
    
    def add_the_answer(self):
        item = self.tree.selected_item()[0]
        itm = item
        itm = self.tree.tree.item(itm)['values']
        question = itm[0]
        category = itm[1]
        type = itm[2]
        id = get_id(question, category, type)
        answer = Answers(root, id)
        answer.pack()
        self.pack_forget()

    def refresh(self):
        self.tree.refresh(get_question())


question = Question(root)
module = Module(root)

root.mainloop()
