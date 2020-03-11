from glfw.library import glfw
from .Application import *

if __name__ == '__main__':
	app = Application(500, 500)
	with app:
		pass

