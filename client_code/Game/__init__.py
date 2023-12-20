from ._anvil_designer import GameTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import random
import datetime
import base64
from anvil.tables import app_tables

class Game(GameTemplate):
  def __init__(self, user = 'karl.zipple@gmail.com', qList = [], game = '', lives = 3, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.q = app_tables.question.get(questionID="1")
    self.correct = 0
    self.incorrect = 0
    self.missed = []
    self.game = game
    self.qList = qList
    self.lives = lives
    # self.q = self.randomQ()
    self.submitted = False
    self.missed = []
    self.imLives.source = app_tables.images.get(name=str(self.lives))['image']
    self.gameID = base64.b64encode((user + str(datetime.datetime.now())).encode()).decode()
    print(self.gameID)
    # self.update_display()

  def update_display(self):
    # this handles a variety of small tasks that need to be performed when a new question loads.
    # set question and answer texts
    self.correctAnswer = self.q["order"].index(self.q["correctAnswer"])
    self.question.content = self.q["questionText"].replace('<u></u>', '<u>'
                                                           + self.getAnswer(self.q['order'][0])
                                                           + '</u>' )
    self.radio_A.text = 'No Change'
    self.radio_B.text = self.getAnswer(self.q['order'][1])
    self.radio_C.text = self.getAnswer(self.q['order'][2])
    self.radio_D.text = self.getAnswer(self.q['order'][3])
    # update the score
    self.score.text = f'Correct: {self.correct}, Incorrect: {self.incorrect}'
    # clear the previous selection
    self.radio_A.selected = False
    self.radio_B.selected = False
    self.radio_C.selected = False
    self.radio_D.selected = False
    self.answerRT.visible = False
    self.answerRT.content = "<h2>Answer</h2>"
    self.submit.text = 'Submit'
    self.submitted = False

  def radio_button_1_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    pass

  def submit__click(self, **event_args):
    if self.radio_A.get_group_value() is None:
      return
    if not self.submitted:
      selected = int(self.radio_A.get_group_value())
      if selected == self.correctAnswer:
        self.correct +=1
        self.updateELO(1)
      else:
        self.updateELO(0)
        self.incorrect += 1
        self.missed.append(self.q)
      app_tables.responses.add_row(date=datetime.date.today(), correct= selected == self.correctAnswer, questionID=self.q['questionID'], response=self.q['order'][selected], userID='karl.zipple@gmail.com')
      self.qList.pop(self.qList.index(self.q))
      self.renorm()
      self.answerRT.visible = True
      for i in range(4):
        self.answerRT.content += '\n' + self.q['explanation' + self.q['order'][i]].replace('~~', 'ABCD'[i])
      self.submit.text = 'Next'
      self.submitted = True
    else:
      self.q = self.randomQ()
      self.update_display()
    pass

  def randomQ(self):
    if len(self.qList) == 0:
      open_form('Dashboard')
    x = random.random()
    qlIndex = 0
    running_total = 0
    while running_total < x:
      result = self.qList[qlIndex]
      running_total += self.qList[qlIndex]['p']
      qlIndex += 1
    return result

  def getAnswer(self, option):
    if option == 'A':
      return self.q['answerA']
    elif option == 'B':
      return self.q['answerB']
    elif option == 'C':
      return self.q['answerC']
    elif option == 'D':
      return self.q['answerD']
    return

  def updateELO(self, result):
    k = 18
    tag = app_tables.question.get(questionID = self.q['questionID'])['questionTags']
    studentRow = app_tables.user.get(userID='karl.zipple@gmail.com')
    studentELODictionary = studentRow['eloDictonary']
    studentELO = studentELODictionary[tag]
    questionRow =  app_tables.question.get(questionID = self.q['questionID'])
    questionELO = questionRow['elo']
    qStudent = 10 ** ((studentELO + 200) / 400)
    qQuestion = 10 ** (questionELO / 400)
    eStudent = qStudent / (qStudent + qQuestion)
    eQuestion = qQuestion / (qStudent + qQuestion)
    studentELO += k * (result - eStudent)
    questionELO += k * (1 - result - eQuestion)
    studentELODictionary[tag]  = studentELO

    studentRow['eloDictonary'] = studentELODictionary
    questionRow['elo'] = questionELO
    pass

  def dashboard_click(self, **event_args):
    open_form('Dashboard')
    pass

  def renorm(self):
    totalp = sum(q['p'] for q in self.qList)
    for q in self.qList:
      q['p'] /= totalp
