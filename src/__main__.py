from glfw.library import glfw
from .Application import *

if __name__ == '__main__':
	app = Application("res/fractal2.fs.glsl", 600, 600, False)
	with app:
		pass

