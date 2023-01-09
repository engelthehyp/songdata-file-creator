def make_char_added_space(s: str, spaces_to_fill: int, space_char: str = '\x00') -> str:
	"""
	This function returns a string, padded to a certain length specified, with the character specified.

	This function was written because there must be a certain amount of space for each song or library name on the hard disk. The name has to occupy a block of 48 characters, no matter how long it is.

	If the string is shorter than the length to pad to, the padding character will be added to the end of it until it reaches the specified length.
	If the string is the same size as the length to pad to, the same sting will be returned.
	If the string is longer than the spaces to fill, it will be cut at that limit without padding.

	:param s: The sting to be padded.
	:param spaces_to_fill: The number of spaces to fill out the string to.
	:param space_char: The character with which to pad out the string.
	:return: A new string, cut or padded to the desired length.
	"""

	if len(s) == spaces_to_fill:
		return s

	if len(s) < spaces_to_fill:
		diff = spaces_to_fill - len(s)
		return s + (space_char * diff)

	if len(s) > spaces_to_fill:
		return s[:spaces_to_fill]


def make_limited_char_string(s: str, content_size_limit: int, total_length: int, space_char: str = '\x00') -> str:
	"""
	This function cuts a string down to a limited length, and pads that string to another length with the character specified.

	This function was written because although the player piano system reserves a block size of 48 characters, all names must be 20 characters long or less. With this function, the names can follow that rule.
	It's important for this function to exist because it can handle cutting a string to a length that is different from its final length.
	This is needed because a long name can have a length up to 20 characters but needs a space of 48.

	:param s: The string to cut and pad. Suitable to use with a 20 character song name or library name.
	:param content_size_limit: The maximum length of the part of the string that holds content, as opposed to the part that holds padding. For use with long song names and library names, it should be 20.
	:param total_length: The number of characters that will be in the final string. In other words, the length of it.
	:param space_char: The character with which to pad out the string.
	:return: A new string, cut to the content size limit, and padded to the total length.
	"""

	if len(s) > content_size_limit:
		result = s[:content_size_limit]
	else:
		result = s

	result = make_char_added_space(result, total_length, space_char)

	return result
