import os

import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader
from glm import *

from src.common import Program


def init_program():
	vs_s = include_str("res/test.vs.glsl")
	fs_s = include_str("res/fractal.fs.glsl")

	vs = compileShader(vs_s, GL_VERTEX_SHADER)
	fs = compileShader(fs_s, GL_FRAGMENT_SHADER)
	return Program(vs, fs)


class Application:
	def _draw(self):
		glDrawArrays(GL_QUADS, 0, 4)

	def _on_resize(self, window, w, h):
		self.width = w
		self.height = h

		self.program.set_uniform(b'uResolution', ivec2(w, h))
		glViewport(0, 0, w, h)

	def _on_mouse_move(self, window, x, y):
		self.program.set_uniform(b'uMousePos', vec2(x, self.height - y))

	def __init__(self, width, height):
		if not glfw.init():
			raise Exception("glfw can not be initialized!")
		self.window = glfw.create_window(width, height, "My OpenGL window", None, None)

		if not self.window:
			glfw.terminate()
			raise Exception("glfw window can not be created!")

		glfw.set_window_pos(self.window, 50, 50)
		glfw.make_context_current(self.window)
		glfw.set_window_size_callback(self.window, self._on_resize)
		glfw.set_cursor_pos_callback(self.window, self._on_mouse_move)

		self.program = init_program()
		self._on_resize(self.window, width, height)


	def __del__(self):
		del self.program
		glfw.terminate()

	def start(self):
		glClearColor(0, 1, 0, 0)

		while not glfw.window_should_close(self.window):
			glfw.poll_events()

			glClear(GL_COLOR_BUFFER_BIT)
			self._draw()

			glfw.swap_buffers(self.window)


def include_str(path):
	with open(path, 'r') as file:
		return file.read()

if __name__ == '__main__':
	app = Application(900, 900)
	app.start()


