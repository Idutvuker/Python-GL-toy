import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader
from glm import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

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

		if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS and not imgui.get_io().want_capture_mouse:
			self.mvel += 3.0 * diff


	def _init_window(self, width, height):
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

		imgui.create_context()
		self.impl = GlfwRenderer(self.window, False)



	def __init__(self, width, height):
		self._init_window(width, height)

		self.program = init_program()
		self._on_resize(self.window, width, height)

		self.prev_mpos = vec2(0, 0)
		self.u_mpos = vec2(0, 0)

		self.prev_time = glfw.get_time()
		self.mvel = vec2(0, 0)

		self.u_zoom = 1.0
		self.u_alpha = 700.0
		self.u_beta = 2.0
		self.u_iters = 11


	def __del__(self):
		del self.program
		self.impl.shutdown()
		glfw.terminate()


	def start(self):
		glClearColor(0, 1, 0, 0)

		while not glfw.window_should_close(self.window):
			cur_time = glfw.get_time()
			elapsed = cur_time - self.prev_time
			self.prev_time = cur_time

			glfw.poll_events()
			self.impl.process_inputs()

			self._process(elapsed)

			imgui.new_frame()

			# if imgui.begin_main_menu_bar():
			# 	if imgui.begin_menu("File", True):
			#
			# 		clicked_quit, selected_quit = imgui.menu_item(
			# 			"Quit", 'Cmd+Q', False, True
			# 		)
			#
			# 		if clicked_quit:
			# 			exit(1)
			#
			# 		imgui.end_menu()
			# 	imgui.end_main_menu_bar()

			# imgui.show_test_window()

			imgui.set_next_window_position(0, 0)
			imgui.set_next_window_size(200, 120)

			imgui.begin("Custom window", False, imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE)

			changed, self.u_zoom = imgui.slider_float("Zoom", self.u_zoom, 1.0, 20.0)
			if changed:
				self.program.set_uniform(b'uZoom', self.u_zoom)

			changed, self.u_alpha = imgui.slider_float("Alpha", self.u_alpha, -3.14, 3.14)
			if changed:
				self.program.set_uniform(b'uAlpha', self.u_alpha)

			changed, self.u_beta = imgui.slider_float("Beta", self.u_beta, -3.14, 3.14)
			if changed:
				self.program.set_uniform(b'uBeta', self.u_beta)

			changed, self.u_iters = imgui.slider_int("Iterations", self.u_iters, 1, 16)
			if changed:
				self.program.set_uniform(b'uIters', self.u_iters)

			imgui.end()


			glClear(GL_COLOR_BUFFER_BIT)
			self._draw()

			imgui.render()
			self.impl.render(imgui.get_draw_data())

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
	app = Application(500, 500)
	app.start()
