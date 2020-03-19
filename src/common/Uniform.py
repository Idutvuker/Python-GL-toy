from OpenGL.GL import *
from glm import *

class TypeInfo:
	def __init__(self, type_str, gl_type, py_type):
		self.type_str = type_str
		self.gl_type = gl_type
		self.py_type = py_type


MY_TYPES = [
	TypeInfo("float", GL_FLOAT, float),
	TypeInfo("int", GL_INT, int),

	TypeInfo("vec2", GL_FLOAT_VEC2, vec2),
	TypeInfo("vec3", GL_FLOAT_VEC3, vec2),
	TypeInfo("vec4", GL_FLOAT_VEC4, vec2),

	TypeInfo("ivec2", GL_INT_VEC2, ivec2),
	TypeInfo("ivec3", GL_INT_VEC3, ivec3),
	TypeInfo("ivec4", GL_INT_VEC4, ivec4),

	TypeInfo("mat2", GL_FLOAT_MAT2, mat2),
	TypeInfo("mat3", GL_FLOAT_MAT3, mat3),
	TypeInfo("mat4", GL_FLOAT_MAT4, mat4)
]


def ti_type_str(type_str: str):
	for tp in MY_TYPES:
		if tp.type_str == type_str:
			return tp

	return None


def ti_gl_type(gl_type):
	for tp in MY_TYPES:
		if tp.gl_type == gl_type:
			return tp

	return None


class Uniform:
	def __init__(self, program, type_str, uname, value=None):
		self.utype = ti_type_str(type_str)
		self.uname = uname
		self.program = program
		self.loc = glGetUniformLocation(program, uname)

		self.value = value
		if self.value is None:
			self.value = self.utype.py_type()

		update_func_dict = {
			GL_INT: lambda: glProgramUniform1i(self.program, self.loc, self.value),
			GL_FLOAT: lambda: glProgramUniform1f(self.program, self.loc, self.value),

			GL_INT_VEC2: lambda: glProgramUniform2iv(self.program, self.loc, 1, value_ptr(self.value)),
			GL_INT_VEC3: lambda: glProgramUniform3iv(self.program, self.loc, 1, value_ptr(self.value)),
			GL_INT_VEC4: lambda: glProgramUniform4iv(self.program, self.loc, 1, value_ptr(self.value)),

			GL_FLOAT_VEC2: lambda: glProgramUniform2fv(self.program, self.loc, 1, value_ptr(self.value)),
			GL_FLOAT_VEC3: lambda: glProgramUniform3fv(self.program, self.loc, 1, value_ptr(self.value)),
			GL_FLOAT_VEC4: lambda: glProgramUniform4fv(self.program, self.loc, 1, value_ptr(self.value)),

			GL_FLOAT_MAT2: lambda: glProgramUniformMatrix2fv(self.program, self.loc, 1, False, value_ptr(self.value)),
			GL_FLOAT_MAT3: lambda: glProgramUniformMatrix3fv(self.program, self.loc, 1, False, value_ptr(self.value)),
			GL_FLOAT_MAT4: lambda: glProgramUniformMatrix4fv(self.program, self.loc, 1, False, value_ptr(self.value)),
		}

		self._update_func = update_func_dict[self.utype.gl_type]

	def update(self):
		self._update_func()

	def set_update(self, value):
		self.value = value
		self._update_func()
