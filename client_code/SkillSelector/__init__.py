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
    self.token_box.set_event_handler('x_element_added', self.token_box_x_element_added)
    self.token_box.set_event_handler('x_element_removed', self.token_box_x_element_removed)

    # populate rows in dropdown
    item_list = [(row['tagExplanation'], row) for row in app_tables.tag.search()]
    # print(item_list)
    self.drop_down.items = [self.drop_down.placeholder] + item_list if self.drop_down.placeholder else item_list

    # Any code you write here will run before the form opens.
    #questions = anvil.server.call('getQuestions','e11')

  @property
  def items(self):
    return self.drop_down.items
  
  def add_to_dropdown(self, value):
    """Add an item to the DropDown's items list."""
    self.drop_down.items = self.drop_down.items + [(value['tagExplanation'], value)]

  def remove_from_dropdown(self, text):
    """Remove an item from the DropDown's items list."""
    items = self.drop_down.items
    items.remove((text['tagExplanation'], text))
    self.drop_down.items = items

  def drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    ele = event_args['sender'].selected_value
    # Make it so the token_box holds the whole object, but just displays the tag information. Then when send is called, it sends the full object so it can use the tags
    self.token_box.add(ele)
    self.drop_down.selected_value = self.drop_down.placeholder

  @property
  def selected_items(self):
    return self.token_box.tokens_list

  @selected_items.setter
  def selected_items(self, value):
    self.token_box.tokens_list = []
    if value is not None:
      if type(value) is list:
        for v in value:
          self.token_box.add(v)
      
  def token_box_x_element_added(self, text, **event_args):
    """This method is called Raised when an element is added to the token box"""
    self.remove_from_dropdown(text)

  def token_box_x_element_removed(self, text, **event_args):
    """This method is called Raised when an element is removed from token box"""
    self.add_to_dropdown(text)

  def buStart_click(self, **event_args):
    # TODO: figure out how to raise an alert "You must select at least one skill"
    if not self.token_box.tokens_list:
      print("You must select at least one item!")
      return
    
    selected_tags = self.token_box.tokens_list
    
    #if anvil.users.get_user() is None:
    #  signin = anvil.users.login_with_form()
    q_list = []
    for tag in selected_tags:
      skill = tag[1][1]
      q_list += anvil.server.call('getQuestions', skill, 'karl.zipple@gmail.com')
      
    if q_list:
      open_form('Question', q_list, game = 'game')

  def getTag(self, skill):
    return app_tables.tag.search(tagExplanation=skill)[0]['tagID']
