def print_error(message):
	print("*** ERROR ***: {}".format(message))

def flatten(List):
	while any([isinstance(i, list) or isinstance(i, tuple) for i in List]):
		new_list = []
		for i in List:
			if isinstance(i, list) or isinstance(i, tuple):
				new_list += i
			else:
				new_list += [i]
		List = new_list
	return List