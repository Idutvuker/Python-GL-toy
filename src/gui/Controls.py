import imgui

class Control:
	def __init__(self, export, uniform, type_str: str):
		self.name = export["name"]
		self.min = export["min"]
		self.max = export["max"]
		self.power = export.get("power", 1.0)

		self.uniform = uniform

		self._draw = {
			"float": lambda: imgui.slider_float(self.name, self.uniform.value, self.min, self.max, "%.5f", self.power),
			"int": lambda: imgui.slider_int(self.name, self.uniform.value, self.min, self.max)
		}[type_str]

	def update(self):
		changed, self.uniform.value = self._draw()
		if changed:
			self.uniform.update()
