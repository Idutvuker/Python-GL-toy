import io
import re
import sys
from OpenGL.GL import *

__all__ = ["parse_header"]

type_dict = {
	"bool": GL_BOOL,
	"int": GL_INT,
	"float": GL_FLOAT,
}

def parse_header_uniform(line: str):
	delimiters = r'\s+'
	spl = re.split(delimiters, line)

	assert len(spl) >= 6
	utype, in_name, min_val, max_val, def_val = spl[1:6]

	out_name = in_name
	if len(spl) >= 7:
		out_name = spl[6][1:-1]


	utype = type_dict.get(utype)

	if utype == GL_FLOAT:
		min_val = float(min_val)
		max_val = float(max_val)
		def_val = float(def_val)

		return "uniform float {} = {};".format(in_name, def_val)


def parse_header(src: str):
	buf = io.StringIO(src.lstrip())
	if not buf.readline().startswith("#HEADER"):
		return src, []

	extern_list = []
	ret = ["#version 330 core"]

	for line in buf:
		line = line.strip()

		if not line:
			continue

		if line[0] != "#":
			print("Wrong header format. Line:\n", line, file=sys.stderr)
			return src, []

		if line.startswith("#ENDHEADER"):
			ret.append(buf.read())
			return "\n".join(ret), extern_list

		if line.startswith("#uniform"):
			ret.append(parse_header_uniform(line))

	print("Header is not closed.", file=sys.stderr)
	return src, []