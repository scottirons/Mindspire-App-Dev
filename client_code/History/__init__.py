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
    self.email = curr_user['email'] if curr_user else "karl.zipple@gmail.com"
    self.responses = self.find_matching_responses()
    self.formatted_responses = self.format_responses(self.responses)
    self.repeating_panel_1.items = self.responses
    

  def find_matching_responses(self):
    matching_responses = app_tables.responses.search(
        tables.order_by("datetime", ascending=False),
        userID=self.email
    )
    return matching_responses

  def format_responses(self, responses):
    processed_responses = []
    for response in responses:
      readable_date = response['datetime'].strftime("%Y-%m-%d %H:%M:%S")

      question = list(app_tables.question.search(questionID=response['questionID']))[0]['questionText']
      correct = response['correct']
      chosen = response['response'] 

      processed_response = {
          'date': readable_date,
          'question': question,
          'correct': correct,
          'chosen': chosen
      }

      processed_responses.append(processed_response)
    return processed_responses


  
