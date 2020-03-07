from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from glm import *
import sys

from src.util import read_file_to_str

class Program:
	def use(self):
		glUseProgram(self.program)

	def set_uniform(self, uname, value):
		loc = self._uniforms.get(uname, -1)
		if loc != -1:
			glUseProgram(self.program)
			utype = type(value)

			if utype is float: return glUniform1f(loc, value)
			if utype is int: return glUniform1i(loc, value)

			if utype is vec2: return glUniform2fv(loc, 1, value_ptr(value))
			if utype is vec3: return glUniform3fv(loc, 1, value_ptr(value))
			if utype is vec4: return glUniform4fv(loc, 1, value_ptr(value))

			if utype is ivec2: return glUniform2iv(loc, 1, value_ptr(value))
			if utype is ivec3: return glUniform3iv(loc, 1, value_ptr(value))
			if utype is ivec4: return glUniform4iv(loc, 1, value_ptr(value))

			if utype is mat2: return glUniformMatrix2fv(loc, 1, False, value_ptr(value))
			if utype is mat3: return glUniformMatrix3fv(loc, 1, False, value_ptr(value))
			if utype is mat4: return glUniformMatrix4fv(loc, 1, False, value_ptr(value))

			print("Type %s is not supported!" % utype, file=sys.stderr)


	def _get_uniform_map(self):
		self._uniforms = {}

		count = glGetProgramiv(self.program, GL_ACTIVE_UNIFORMS)
		uname = ctypes.create_string_buffer(32)
		for i in range(count):
			glGetActiveUniform(self.program, i, 32, None, None, None, uname)

			self._uniforms[uname.value] = glGetUniformLocation(self.program, uname.value)


	@staticmethod
	def from_files(vs_path, fs_path):
		vs_str = read_file_to_str(vs_path)
		fs_str = read_file_to_str(fs_path)
		return Program.from_strings(vs_str, fs_str)

	@staticmethod
	def from_strings(vs_str: str, fs_str: str):
		vs = compileShader(vs_str, GL_VERTEX_SHADER)
		fs = compileShader(fs_str, GL_FRAGMENT_SHADER)
		return Program(vs, fs)

	def __init__(self, vertex_shader, fragment_shader):
		self.program = compileProgram(vertex_shader, fragment_shader)
		glUseProgram(self.program)

		self._get_uniform_map()

	def delete(self):
		glDeleteProgram(self.program)

