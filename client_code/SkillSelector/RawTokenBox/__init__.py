from ._anvil_designer import RawTokenBoxTemplate
from anvil import *

class RawTokenBox(RawTokenBoxTemplate):
  token_texts_list = []
  
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)
    
    self.token_texts_list = []
    
  def add(self, text):
    """Add a token to the Flow Panel (and call the add_callback)."""
    token = Button(
      text=text['tagExplanation'],
      icon="fa:times",
      icon_align="left",
      role="primary-color",
    )
    # used for removal, but only the descriptive name is actually shown
    token.tag_data = text
    
    token.set_event_handler("click", self.remove)
    self.flow_panel_1.add_component(token)
    self.token_texts_list.append(text)
    self.raise_event('x_element_added',text=text)

  def remove(self, **event_args):
    """Remove a token from the Flow Panel (and call the remove_callback)."""
    token = event_args['sender']
    self.raise_event('x_element_removed',text=token.tag_data)
    token.remove_from_parent()
    self.token_texts_list.remove(token.tag_data)
    
  @property
  def tokens_list(self):
    return self.token_texts_list

  @tokens_list.setter
  def tokens_list(self, value):
    if value is not None:
      if type(value) is list:
        self.flow_panel_1.clear()
        self.token_texts_list = []
        for v in value:
          self.add(v)

