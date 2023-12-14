from ._anvil_designer import TutorStudentDataTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TutorStudentData(TutorStudentDataTemplate):
  def __init__(self, user = 'karl.zipple@gmail.com', **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user
    self.rtTitle.content = '## Welcome back, ' + app_tables.user.get(userID=user)['firstName'] + '!'
    item_list = ['']
    for row in app_tables.user.search(tutorID = self.user):
      item_list.append((row['firstName'] + ' ' + row['lastName'], row))
    self.ddStudent.items = item_list

    # Any code you write here will run before the form opens.
