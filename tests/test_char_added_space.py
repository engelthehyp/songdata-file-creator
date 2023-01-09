import unittest

from string_utilities import make_char_added_space as char_add_space


class TestMakeCharAddedSpace(unittest.TestCase):
	ALLOWED_SPACE = 48
	PADDING_CHARACTER = '\x00'

	PARAMS = ALLOWED_SPACE, PADDING_CHARACTER

	def test_zero_length_string_is_pad_char_to_space(self):
		func_input = ''

		space, pad_char = self.PARAMS

		expected = pad_char * space
		actual = char_add_space(func_input, *self.PARAMS)

		self.assertEqual(expected, actual)

	def test_string_shorter_than_space_is_padded_to_space(self):
		func_input = 'Below 48 chars'

		space, pad_char = self.PARAMS

		expected = func_input + (pad_char * (space - len(func_input)))
		actual = char_add_space(func_input, *self.PARAMS)

		self.assertEqual(expected, actual)

	def test_string_equal_to_length_of_space_is_unchanged(self):
		func_input = 'A string that is exactly 48 characters long here'

		space, pad_char = self.PARAMS

		expected = func_input + (pad_char * (space - len(func_input)))
		actual = char_add_space(func_input, *self.PARAMS)

		self.assertEqual(expected, actual)

	def test_string_longer_than_space_is_cut_at_space(self):
		func_input = 'A string that is definitely longer 48 characters long here.'

		space, pad_char = self.PARAMS

		expected = func_input[:space]
		actual = char_add_space(func_input, *self.PARAMS)

		self.assertEqual(expected, actual)


if __name__ == '__main__':
	unittest.main()
