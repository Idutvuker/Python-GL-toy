from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from glm import *
import sys
import json

from src.common.Uniform import Uniform

from src.util import read_file_to_str


class Program:
	def use(self):
		glUseProgram(self.program)

	def get_uniform(self, uname):
		return self.uniforms[uname]

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
		b = [0, 0]
		for i in range(count):
			a = glGetActiveUniform(self.program, i, 32, None, None, None, uname)
			#print(b)
			self._uniforms[uname.value] = glGetUniformLocation(self.program, uname.value)
			#a = Uniform(self.program, utype, uname.value, 0)




	@staticmethod
	def from_files(vs_path, fs_path):
		vs_str = read_file_to_str(vs_path)
		fs_str = read_file_to_str(fs_path)
		return Program.from_strings(vs_str, fs_str)

	@staticmethod
	def parse_header(s: str):
		s = s.lstrip()
		if not s.startswith("#header"):
			return s, None

		res = ["#version 330 core"]

		spl = s.split("\n", 1)

		x = len("#header")
		path = spl[0][x:].strip()[1:-1]

		uni_defs = []

		with open(path) as file:
			fld = json.load(file)
			unis = fld.get("uniforms", None)

			if unis:
				for uni in unis.items():
					uname = uni[0]
					utype = uni[1]["type"]
					value = uni[1].get("value", None)
					if value is None:
						res.append("uniform {type} {name};".format(type=utype, name=uname))
					else:
						res.append("uniform {type} {name} = {val};".format(type=utype, name=uname, val=value))

					uni_defs.append((utype, uname, value))
					#uniforms[uni[0]] = Uniform(-1, utype, uname, value)


			res.append(spl[1])
			return "\n".join(res), uni_defs


	@staticmethod
	def from_strings(vs_str: str, fs_str: str):
		fs_str, uni_defs = Program.parse_header(fs_str)
		#print(fs_str)

		vs = compileShader(vs_str, GL_VERTEX_SHADER)
		fs = compileShader(fs_str, GL_FRAGMENT_SHADER)
		return Program(vs, fs, uni_defs)

	def __init__(self, vertex_shader, fragment_shader, uni_defs=None):
		self.program = compileProgram(vertex_shader, fragment_shader)
		glUseProgram(self.program)

		self.uniforms = {}

		if uni_defs:
			for udef in uni_defs:
				self.uniforms[udef[1]] = Uniform(self.program, *udef)
		#self._create_uniform_map()

	def delete(self):
		glDeleteProgram(self.program)
