from scene import *
from functools import partial
import os

class Skat(Scene):
	def setup(self):
		self.root_layer = Layer(self.bounds)
		self.deal()
		
	def deal(self):
		images_root = os.path.expanduser('~/Documents/Images')
		image_name = '_01c.gif' # gif is NOT the extension
		image_path = os.path.join(images_root, image_name + '.png') # png is used instead
		image_name = load_image_file(image_path)
		self.cards = []
		self.selected = []
		card_width = 90
		card_height = 140
		gap = 10
		width  = 8 * (card_width  + gap)
		height = 4 * (card_height + gap)
		offset = Point((self.size.w - width)  / 2,
		               (self.size.h - height) / 2)
		for i in range(8):
			for j in range(4):
				card = Layer(Rect(offset.x + (card_width  + gap) * i,
				                       offset.y + (card_height + gap) * j,
				                       90, 140))
				card.card_image = image_name
				card.background = Color(0.9, 0.9, 0.9)
				card.stroke = Color(1, 1, 1)
				card.stroke_weight = 4.0
				self.add_layer(card)
				self.cards.append(card)
		self.touch_disabled = False
	
	def touch_began(self, touch):
		if self.touch_disabled:
			return
		if len(self.selected) == 2:
			self.discard_selection()
			return
		for card in self.cards:
			if card in self.selected or len(self.selected) > 1:
				continue
			if touch.location in card.frame:
				def reveal_card():
					card.image = card.card_image
					card.animate('scale_x', 1.0, 0.15, completion=self.check_selection)
				self.selected.append(card)
				card.animate('scale_x', 0.0, 0.15, completion=reveal_card)
				card.scale_y = 1.0
				card.animate('scale_y', 0.9, 0.15, autoreverse=True)
	
	def discard_selection(self):
		for card in self.selected:
			def conceal(card):
				card.image = None
				card.animate('scale_x', 1.0, 0.15)
			card.animate('scale_x', 0.0, 0.15,
			             completion=partial(conceal, card))
			card.scale_y = 1.0
			card.animate('scale_y', 0.9, 0.15, autoreverse=True)
		self.selected = []
		
	def check_selection(self):
		for c in self.selected:
			c.animate('background', Color(0.0, 0.0, 0.0))
		
	def draw(self):
		background(0.2, 0.6, 0.2)
		self.root_layer.update(self.dt)
		self.root_layer.draw()

	def new_game(self):
		self.deal()
		self.root_layer.animate('scale_x', 1.0)
		self.root_layer.animate('scale_y', 1.0)

run(Skat())
#print(dir(Scene))
