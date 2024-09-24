#this file is for storing the questions and the options for the quiz

import requests

parameters = {
    "amount" : 5,
    "type" : "multiple"
}

#the program will take the questions from the php page created
response = requests.get(url="https://opentdb.com/api.php?amount=5&category=18&difficulty=easy&type=multiple", params=parameters)
question_data = response.json() ["results"]

#These are the sample questions in the quiz.
"""
{"response_code":0,"results":[
    {"category":"Science: Computers","type":"multiple","difficulty":"easy","question":"What amount of bits commonly equals one byte?","correct_answer":"8","incorrect_answers":["1","2","64"]},
    {"category":"Science: Computers","type":"multiple","difficulty":"easy","question":"What is the domain name for the country Tuvalu?","correct_answer":".tv","incorrect_answers":[".tu",".tt",".tl"]},
    {"category":"Science: Computers","type":"multiple","difficulty":"easy","question":"In &quot;Hexadecimal&quot;, what color would be displayed from the color code? &quot;#00FF00&quot;?","correct_answer":"Green","incorrect_answers":["Red","Blue","Yellow"]},
    {"category":"Science: Computers","type":"multiple","difficulty":"easy","question":"How many values can a single byte represent?","correct_answer":"256","incorrect_answers":["8","1","1024"]},{"category":"Science: Computers","type":"multiple","difficulty":"easy","question":"Which programming language shares its name with an island in Indonesia?","correct_answer":"Java","incorrect_answers":["Python","C","Jakarta"]}
    ]}
"""