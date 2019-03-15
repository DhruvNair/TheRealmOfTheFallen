from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import LabelBase
from kivy.config import Config
from functools import partial
from kivy.uix.image import Image
from customwidgets import ScrollableLabel
from customwidgets import SmallButton
from customwidgets import LargeButton
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
import os.path
import sys
import pickle

LabelBase.register(name="Myfont", fn_regular="data/font.ttf")
Config.set('kivy','window_icon','/data/icon.ico')
music = SoundLoader.load('data/music.wav')

class Realm(FloatLayout):
	class character(object):
		def __init__ (self,name,gender,health,wisdom,agility,buffs,gear,spab,attrib):
			self.name=name
			self.health=health
			self.wisdom=wisdom
			self.mana=wisdom*2
			self.agility=agility
			self.damage=attrib['Weapons']*1
			self.gender=gender
			self.armour=0

	def __init__(self,**kwargs):
		self.path = './story'
		self.glgear=('Ragged Clothes','Wooden Knife','Casual Clothes','Torn Chainmail','Rusty Sword','Chainmail Armour','Iron Sword','Blessed Chainmail Armour','Steel Sword','Silver Sword','Silver Bow')
		self.glbuffs=(' ',' ',' ','arm,1','dam,1','arm,2','dam,2','arm,2','dam,3','dam,3',' ')
		self.glspab=('Damage Reduction','Damage Upgrade','Ignore Armour','Increase Proficiency','Deadly aim')
		self.glattrib={'Premonition':0,'Weapons':0,'Arcane':0,'Literature':0,'Ranged':0}
		super(Realm, self).__init__(**kwargs)

		#labels
		self.main_label = ScrollableLabel(size_hint=(1,.3), pos_hint={'x':0,'y':.55})
		self.name_label = Label(size_hint=(.5,None), pos_hint={'x':.25,'y':.7})
		self.health_label = Label(size_hint=(.5,None), pos_hint={'x':.25,'y':.6})
		self.wisdom_label = Label(size_hint=(.5,None), pos_hint={'x':.25,'y':.5})
		self.mana_label = Label(size_hint=(.5,None), pos_hint={'x':.25,'y':.4})
		self.agility_label = Label(size_hint=(.5,None), pos_hint={'x':.25,'y':.3})
		self.armour_label = Label(size_hint=(.5,None), pos_hint={'x':.25,'y':.2})
		self.warning_label = Label(size_hint=(.8,None), pos_hint={'x':.1,'y':.43})

		#buttons
		self.btn1 = LargeButton(text = "Button 1", size_hint=(1,.1), pos_hint={'x':0,'y':.35}, on_release=partial(self.select,'1'))
		self.btn2 = LargeButton(text = "Button 2", size_hint=(1,.1), pos_hint={'x':0,'y':.25}, on_release=partial(self.select,'2'))
		self.btn3 = LargeButton(text = "Button 3", size_hint=(1,.1), pos_hint={'x':0,'y':.15}, on_release=partial(self.select,'3'))
		self.btn4 = LargeButton(text = "Button 4", size_hint=(1,.1), pos_hint={'x':0,'y':.05}, on_release=partial(self.select,'4'))
		self.stats_btn = SmallButton(text = "Stats", size_hint=(.1,.05), pos_hint={'x':.85,'y':.9}, on_release = self.showstats)
		self.back_btn = SmallButton(text = "Back", size_hint=(.1,.05), pos_hint={'x':.05,'y':.9}, on_release = self.update)
		self.exit_btn = SmallButton(text = "Exit", size_hint=(.1,.05), pos_hint={'x':.05,'y':.9}, on_release = self.mainmenu)
		self.save_btn = SmallButton(text="Save", size_hint=(.1,.05), pos_hint={'x':.45, 'y':.9}, on_release = self.save)
		self.load_btn = LargeButton(text = "Load", size_hint=(.5,.1), pos_hint={'x':.25, 'y':.2}, on_release= self.tryload)
		self.continue_btn = LargeButton(text = "Continue", size_hint=(.5,.1), pos_hint={'x':.25, 'y':.5}, on_release= self.update)
		self.new_btn = LargeButton(text = "New Game", size_hint=(.5,.1), pos_hint={'x':.25, 'y':.35}, on_release= self.newgame)
		self.close_btn = LargeButton(text = "Close", size_hint=(.5,.1), pos_hint={'x':.25, 'y':.05}, on_release= self.close)
		self.load_proceed_btn = LargeButton(text = "Proceed", size_hint=(.5,.1), pos_hint={'x':.25,'y':.15}, on_release=self.checkload)
		self.new_proceed_btn = LargeButton(text = "Proceed", size_hint=(.5,.1), pos_hint={'x':.25,'y':.15}, on_release=self.checknew)
		self.yes_btn = LargeButton(text = "Yes", size_hint=(.25,.1), pos_hint={'x':.2,'y':.15}, on_release=self.startgame)
		self.no_btn = LargeButton(text = "No", size_hint=(.25,.1), pos_hint={'x':.55,'y':.15}, on_release=self.newgame)

		#image
		self.name_img = Image(source= 'data/name.png', size_hint=(1,.4), pos_hint={'x':0,'y':.6})

		#misc
		self.buttons = {self.btn1 : 'button1', self.btn2 : 'button2', self.btn3 : 'button3', self.btn4 : 'button4'}
		self.stats_analogy = {self.name_label : "Name", self.health_label : "Health", self.wisdom_label : "Wisdom", self.mana_label : "Mana", self.agility_label : "Agility", self.armour_label : "Armour"}
		self.hero = self.character('Alexander','he',30,10,15,self.glbuffs,self.glgear,self.glspab,self.glattrib)

		#input box
		self.load_name_in = TextInput(multiline=False, size_hint=(.8,.1), pos_hint={'x':.1,'y':.35}, on_text_validate=self.checkload)
		self.new_name_in = TextInput(multiline=False, size_hint=(.8,.1), pos_hint={'x':.1,'y':.35},on_text_validate=self.checknew)

		#grouping pages
		self.homepage = [self.load_btn, self.continue_btn, self.new_btn, self.close_btn, self.name_img]
		self.gamepage = [self.main_label, self.stats_btn, self.save_btn, self.exit_btn]
		self.statspage = [self.back_btn, self.name_label, self.health_label, self.wisdom_label, self.mana_label, self.agility_label, self.armour_label]
		self.conformationpage = [self.warning_label, self.yes_btn, self.no_btn]
		self.stats_default = {self.hero.health : 30, self.hero.wisdom : 10, self.hero.mana : 15, self.hero.agility : 15, self.hero.armour : 0}
		self.load_validation_page = [self.load_proceed_btn, self.load_name_in, self.exit_btn, self.main_label]
		self.new_validation_page = [self.new_proceed_btn, self.new_name_in, self.exit_btn, self.main_label]
		self.all_widgets = self.homepage + self.gamepage + self.statspage + self.load_validation_page + self.new_validation_page + self.conformationpage + [self.btn1, self.btn2, self.btn3, self.btn4]

		#functions
		if music:
			music.play()
		self.mainmenu()

	def getData(self,dname):
		f = open(self.path+'/data.txt', 'r')
		text=''
		read=0
		for i in f:
			if i=='stop\n' and read:
				read=0
				break
			if read:
				text+=i
			if i==dname+'\n':
				read=1
		f.close()
		text=text[:-1]
		if text=='':
			return None
		return text

	def save(self, *args):
		self.clear()
		savefile = self.path, self.hero
		pickle.dump(savefile, open("savedfiles/"+self.hero.name+".rlm", "wb"))
		self.main_label.text = "Game saved successfully!\nName of saved game : "+self.hero.name
		self.show([self.main_label, self.back_btn])

	def show(self, page):
		for widget in page:
			self.add_widget(widget)

	def tryload(self, *args):
		self.clear()
		self.main_label.text = "You say you have played before?\nWhat were you called?"
		self.show(self.load_validation_page)

	def checkload(self, *args):
		if os.path.isfile("savedfiles/"+self.load_name_in.text+".rlm"):
			loadfile=pickle.load(open("savedfiles/"+self.load_name_in.text+".rlm","rb"))
			self.path = loadfile[0]
			self.hero = loadfile[1]
			self.clear()
			self.show(self.homepage)
			self.continue_btn.disabled = False
		else:
			self.warning_label.text = "We couldn\'t find this name in our records!"
			self.add_widget(self.warning_label)

	def close(self, *args):
		App.get_running_app().stop()
		Window.close()

	def newgame(self, *args):
		self.clear()
		self.path = './story'
		self.main_label.text = "Hello contender,\nWhat would you like to be called?"
		self.new_name_in.text = ""
		self.show(self.new_validation_page)
	def checknew(self, *args):
		if self.new_name_in.text!='':
			self.hero.name = self.new_name_in.text
			if os.path.isfile("savedfiles/"+self.new_name_in.text+".rlm"):
				self.clear()
				self.warning_label.text = "This name seems to be taken! Would you like to overwrite the save?"
				self.show(self.conformationpage)
			else:
				self.startgame()

	def startgame(self, *args):
		self.hero.name = self.new_name_in.text
		for stat in self.stats_default:
			stat = self.stats_default[stat]
		self.update()

	def mainmenu(self, *args):
		self.clear()
		if self.path == './story':
			self.continue_btn.disabled = True
		else:
			self.continue_btn.disabled = False
		self.show(self.homepage)

	def clear(self):
		for widget in self.all_widgets:
			self.remove_widget(widget)

	def checkoptions(self):
		for button in self.buttons:
			if self.getData(self.buttons[button])!=None:
				button.text = self.getData(self.buttons[button])
				self.add_widget(button)
	def changestats(self):
		f = open(self.path+'/data.txt', 'r')
		for i in f:
			if i=='#health++\n':
				self.hero.health+=1
			if i=='#wisdom++\n':
				self.hero.wisdom+=1
				self.hero.mana+=2
			if i=='#agility++\n':
				self.hero.agility+=1

	def update(self,*args):
		self.clear()
		self.changestats()
		self.main_label.text = self.getData('label')
		code = self.getData('code')
		fight = self.getData('fight')
		if fight==None: 
			self.checkoptions()
			self.show(self.gamepage)

	def select(self,selected,*args):
		self.path += '/'+selected
		self.update()

	def updatestats(self):
		self.stats_value = {self.name_label : self.hero.name, self.health_label : self.hero.health, self.wisdom_label : self.hero.wisdom, self.mana_label : self.hero.mana, self.agility_label : self.hero.agility, self.armour_label : self.hero.armour}
		for stat in self.stats_value:
			stat.text = self.stats_analogy[stat]+"  :  "+str(self.stats_value[stat])

	def showstats(self,*args):
		self.clear()
		self.updatestats()
		self.show(self.statspage)
class mainApp(App):
	title = "The Realm of the fallen"
	icon = "data/icon.png"
	def build(self):
		return Realm()

mainApp().run()