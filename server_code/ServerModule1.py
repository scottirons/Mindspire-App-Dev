import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime as dt
from random import shuffle

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
@anvil.server.callable
def getQuestions(tag, studentID):
  answers = ['A', 'B', 'C', 'D']
  questions = app_tables.question.search(questionTags=q.like(f'%{tag}%'))
  studentELO = app_tables.user.get(userID=studentID)['eloDictonary'][tag]
  questionList = []
  for question in questions:
    questionData = {}
    questionData['questionID'] = question['questionID']
    questionData['questionText'] = question['questionText']
    questionData['answerA'] = question['answerA']
    questionData['answerB'] = question['answerB']
    questionData['answerC'] = question['answerC']
    questionData['answerD'] = question['answerD']
    questionData['explanationA'] = question['explanationA']
    questionData['explanationB'] = question['explanationB']
    questionData['explanationC'] = question['explanationC']
    questionData['explanationD'] = question['explanationD']
    questionData['correctAnswer'] = question['correctAnswer']
    shuffle(answers)
    questionData['order'] = "".join(answers)
    p = 1
    p *= pFromELO(studentELO, question['elo'])
    pFromRecency(studentID, question['questionID'])
    questionData['p'] = p
    questionList.append(questionData)
  totalP = sum([question['p'] for question in questionList])
  for question in questionList:
    question['p'] /= totalP
  return questionList

@anvil.server.callable
def pFromRecency(student, question):
  p = 1
  responses = app_tables.responses.search(questionID = question, userID = student)
  if len(responses) == 0:
    return p
  maxDate = max(response['date'] for response in responses)
  if (maxDate - dt.date.today()).days <= 3:
    p *= 0.1
  elif (maxDate - dt.date.today()).days <= 7:
    p *= 0.4
  else:
    p *= 0.75
  return p

@anvil.server.callable
def pFromELO(studentELO, qELO):
  # if a question is 100 ELO points above or below the elo of the student, it is half as likely to come up
  # this is cumulative; an 1800 elo stuent is only 12.5 as likely to get a 1500 elo question as a 1500 elo student
  eloDiff = abs(studentELO - qELO)
  return 0.5 ** (eloDiff / 100)