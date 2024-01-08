from ._anvil_designer import HistoryTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

class History(HistoryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    curr_user = anvil.users.get_user()
    user_email = curr_user['email'] if curr_user else "karl.zipple@gmail.com"
    matching_responses = app_tables.responses.search(
        tables.order_by("datetime", ascending=False),
        userID=user_email
    )
    for r in matching_responses:
      print(r)


  
