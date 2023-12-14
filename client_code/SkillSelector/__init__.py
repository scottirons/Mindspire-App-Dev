from ._anvil_designer import SkillSelectorTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import MultiSelectDropDown

class SkillSelector(SkillSelectorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    # item_list = []
    # for row in app_tables.tag.search():
    #   item_list.append((row['tagExplanation'], row))
    # self.ddSkill.items = item_list
    self.init_components(**properties)

    self.multi_select_dropdown = MultiSelectDropDown()

    # populate rows in dropdown
    item_list = [(row['tagExplanation'], row) for row in app_tables.tag.search()]
    self.multi_select_dropdown.items = item_list

    self.add_component(self.multi_select_dropdown)

    # Any code you write here will run before the form opens.
    #questions = anvil.server.call('getQuestions','e11')

  def buStart_click(self, **event_args):
    # TODO: figure out how to raise an alert "You must select at least one skill"
    if not self.multi_select_dropdown.selected_items:
      print("You must select at least one item!")
    
    selected_tags = self.multi_select_dropdown.selected_items
    
    #if anvil.users.get_user() is None:
    #  signin = anvil.users.login_with_form()
    if self.ddSkill.selected_value is None:
      print('Stop that')
      pass
    else:
      skill = self.ddSkill.selected_value[0][1]
      qList = anvil.server.call('getQuestions', skill, 'karl.zipple@gmail.com')
      print(len(qList))
      open_form('Question', qList, game = 'game')
      return
    pass

  def getTag(self, skill):
    return app_tables.tag.search(tagExplanation=skill)[0]['tagID']
