from ._anvil_designer import TokenBoxTemplate
from anvil import *

class TokenBox(TokenBoxTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  @property
  def tokens_list(self):
    return self.raw_token_box_1.tokens_list

  @tokens_list.setter
  def tokens_list(self, value):
    print("setting to [{lv}]".format(lv=value))
    if value is not None:
      if type(value) is list:
        self.raw_token_box_1.tokens_list = value
        
  def add(self, text):
    """Add a token to the Flow Panel"""
    self.raw_token_box_1.add(text)
    
  def remove(self, **event_args):
    """Remove a token from the Flow Panel"""
    self.raw_token_box_1.remove(**event_args)

  def raw_token_box_1_x_element_added(self, text, **event_args):
    """This method is called Raised when an element is added to the token box"""
    self.raise_event('x_element_added',text=text)

  def raw_token_box_1_x_element_removed(self, text, **event_args):
    """This method is called Raised when an element is removed from token box"""
    self.raise_event('x_element_removed',text=text)

