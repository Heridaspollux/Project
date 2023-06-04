#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ipywidgets as widgets
from IPython.display import display

# Create a widget
text_widget = widgets.Text(description='Enter your name:')
button_widget = widgets.Button(description='Greet')

# Define a callback function for the button click event
def greet_button_clicked(b):
    name = text_widget.value
    print(f"Hello, {name}!")

# Register the callback function to the button click event
button_widget.on_click(greet_button_clicked)

# Display the widgets
display(text_widget, button_widget)


# In[ ]:




