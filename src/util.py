__all__ = ["read_file_to_str"]


def read_file_to_str(path):
	with open(path, 'r') as file:
		return file.read()