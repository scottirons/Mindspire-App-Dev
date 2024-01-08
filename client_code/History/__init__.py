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
    print(self.responses)
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
      readable_date = response['datetime_field'].strftime("%Y-%m-%d %H:%M:%S")

        # Retrieve the associated question
        question = response['questionID']['questionText']

        # Get the chosen and correct answers
        chosen_answer = response['chosen_answer']
        correct_answer = response['correct_answer']  # Adjust how you retrieve this as necessary

        # Combine all needed information into a single dictionary
        processed_response = {
            'readable_date': readable_date,
            'question': question,
            'chosen_answer': chosen_answer,
            'correct_answer': correct_answer
        }

        processed_responses.append(processed_response)


  
