from ._anvil_designer import MultiSelectDropDownTemplate
from anvil import *

class MultiSelectDropDown(MultiSelectDropDownTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

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



