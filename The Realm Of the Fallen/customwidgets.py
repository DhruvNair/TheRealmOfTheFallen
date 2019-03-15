
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.properties import StringProperty
Builder.load_string('''
<ScrollableLabel>:
	Label:
		size_hint_y: None
		height: self.texture_size[1]
		text_size: self.width, None
		text: root.text
''')
class ScrollableLabel(ScrollView):
	text = StringProperty('')
class SmallButton(Button):
	text = StringProperty('')
class LargeButton(Button):
	text = StringProperty('')