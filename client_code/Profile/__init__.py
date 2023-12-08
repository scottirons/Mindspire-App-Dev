from ._anvil_designer import ProfileTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Profile(ProfileTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def buSaveChanges_click(self, **event_args):
    signin = anvil.users.get_user()
    userInfo = app_tables.user.get(userID=signin['email'])
    if userInfo is None:
      app_tables.user.add_row(eloDictonary={}, phone=self.boxPhone.text,
                              email=self.boxEmail.text, firstName=self.boxFirstName.text,
                             lastName=self.boxLastName.text, userID=signin['email'])
    #open_form('Dashboard')
    else:
      userInfo.update(phone=self.boxPhone.text, email=self.boxEmail.text,
                     firstName=self.boxFirstName.text, lastName=self.boxLastName.text)
    open_form('Dashboard')
    return
