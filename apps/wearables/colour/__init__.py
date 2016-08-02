class Colour(object):
	def __init__(self, r=0, g=0, b=0):
		if type(r) is 'str':
			self.set_hex(r)
		else:
			self._colour = [r,g,b]

	def set_hex(self, colourstring):
		colourstring = colourstring.strip()
		if colourstring[0] == '#': colourstring = colourstring[1:]
		r, g, b = colourstring[:2], colourstring[2:4], colourstring[4:]
		r, g, b = [int(n, 16) for n in (r, g, b)]
		self._colour = [r, g, b]

	def get_tuple(self):
		return self._colour

	def get_hex(self):
		return "#%02X%02X%02X" % tuple(self._colour)

	def get_neo(self):
		return int("%02X%02X%02X" % tuple(self._colour), 16)

	def set_r(self, value):
		self._colour[0] = value

	def set_g(self, value):
		self._colour[1] = value

	def set_b(self, value):
		self._colour[2] = value

	def __str__(self):
		return self.get_hex()

class Wheel:
	def Wheel(pos):
		position = 255 - pos

		if (position < 85):
			return Colour(255 - position * 3, 0, position * 3)

		if (position < 170):
			position = position - 85
			return Colour(0, position * 3, 255 - position * 3)

		position = position - 170
		return Colour(position * 3, 255 - position * 3, 0)
