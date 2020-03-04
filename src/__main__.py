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
		mpos = vec2(x, self.height - y)
		diff = mpos - self.prev_mpos
		self.prev_mpos = mpos

		if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
			self.mvel += 3.0 * diff


	def __init__(self, width, height):
		if not glfw.init():
			raise Exception("glfw can not be initialized!")
		self.window = glfw.create_window(width, height, "My OpenGL window", None, None)

		if not self.window:
			raise Exception("glfw window can not be created!")

		glfw.set_window_pos(self.window, 50, 50)
		glfw.make_context_current(self.window)
		glfw.swap_interval(0)

		glfw.set_window_size_callback(self.window, self._on_resize)
		glfw.set_cursor_pos_callback(self.window, self._on_mouse_move)

		self.program = init_program()
		self._on_resize(self.window, width, height)

		self.prev_mpos = vec2(0, 0)
		self.u_mpos = vec2(0, 0)

		self.prev_time = glfw.get_time()
		self.mvel = vec2(0, 0)


	def __del__(self):
		del self.program
		glfw.terminate()

	def start(self):
		glClearColor(0, 1, 0, 0)

		while not glfw.window_should_close(self.window):
			cur_time = glfw.get_time()
			elapsed = cur_time - self.prev_time
			self.prev_time = cur_time

			glfw.poll_events()
			self._process(elapsed)

			glClear(GL_COLOR_BUFFER_BIT)
			self._draw()

			glfw.swap_buffers(self.window)

	def _process(self, delta):
		self.u_mpos += self.mvel * delta
		self.program.set_uniform(b'uMousePos', self.u_mpos)

		x = pow(0.03, delta)
		self.mvel *= x

def include_str(path):
	with open(path, 'r') as file:
		return file.read()

if __name__ == '__main__':
	app = Application(900, 900)
	app.start()


