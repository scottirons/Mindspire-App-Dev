from ._anvil_designer import SkillSelectorTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class SkillSelector(SkillSelectorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    # item_list = []
    # for row in app_tables.tag.search():
    #   item_list.append((row['tagExplanation'], row))
    # self.ddSkill.items = item_list
    self.init_components(**properties)

    # populate rows in dropdown
    item_list = [(row['tagExplanation'], row) for row in app_tables.tag.search()]
    self.drop_down.items = item_list

    self.add_component(self.drop_down)

    # Any code you write here will run before the form opens.
    #questions = anvil.server.call('getQuestions','e11')

  @property
  def items(self):
    return self.drop_down.items

  @items.setter
  def items(self, value):
    if len(value) and value[0] is not self.placeholder:
      self.drop_down.items = [self.placeholder] + value
    else:
      self.drop_down.items = value
  
  def add_to_dropdown(self, value):
    """Add an item to the DropDown's items list."""
    self.drop_down.items = self.drop_down.items + [value]

  def remove_from_dropdown(self, text):
    """Remove an item from the DropDown's items list."""
    items = self.drop_down.items
    if text in items:
      items.remove(text)
    self.drop_down.items = items

  def drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.token_box.add(event_args['sender'].selected_value)
    # Go back to having self.placeholder selected, to allow the same value 
    # to be selected multiple times.
    self.drop_down.selected_value = self.placeholder

  @property
  def selected_items(self):
    return self.token_box.tokens_list

  @selected_items.setter
  def selected_items(self,value):
    self.token_box.tokens_list = []
    if value is not None:
      if type(value) is list:
        for v in value:
          self.token_box.add(v)
      
  def token_box_x_element_added(self, text, **event_args):
    """This method is called Raised when an element is added to the token box"""
    if self.unique:
      self.remove_from_dropdown(text)
    self.raise_event('x_element_selected',text=text)

  def token_box_x_element_removed(self, text, **event_args):
    """This method is called Raised when an element is removed from token box"""
    if self.unique:
      self.add_to_dropdown(text)
    self.raise_event('x_element_deselected',text=text)





  def buStart_click(self, **event_args):
    # TODO: figure out how to raise an alert "You must select at least one skill"
    if not self.multi_select_dropdown.selected_items:
      print("You must select at least one item!")
      return
    
    selected_tags = self.multi_select_dropdown.selected_items
    
    #if anvil.users.get_user() is None:
    #  signin = anvil.users.login_with_form()
    q_list = []
    for tag in selected_tags:
      skill = tag[1]
      qList += anvil.server.call('getQuestions', skill, anvil.users.get_user())
      
    if q_list:
      open_form('Question', q_list, game = 'game')

  def getTag(self, skill):
    return app_tables.tag.search(tagExplanation=skill)[0]['tagID']
