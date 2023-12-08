from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    signin = anvil.users.login_with_form()
    user = app_tables.user.search(userID=signin['email'])
    if len(user) != 0:
      self.welcome.content = 'Welcome back, ' + user[0]['firstName'] + '!'
    else:
      self.welcome.content = 'Welcome, new user! Please fill out the profile form to the left.'
      self.skillQuiz.visible = False
      self.fullQuiz.visible = False



# Any code you write here will run before the form opens.

  def profile_click(self, **event_args):
    open_form('Profile')
    pass

  def skillQuiz_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('SkillSelector')
    pass
