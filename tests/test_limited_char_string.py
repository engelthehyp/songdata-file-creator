import unittest
from string_utilities import make_limited_char_string as lim_char_str


class TestMakeLimitedCharString(unittest.TestCase):
	LONG_NAME_LIMIT = 20
	LONG_NAME_SPACE = 48
	PADDING_CHARACTER = '\x00'

	PARAMS = LONG_NAME_LIMIT, LONG_NAME_SPACE, PADDING_CHARACTER

	def test_zero_length_name_is_pad_char_to_limit(self):
		func_input = ''

		lim, name_space, pad_char = self.PARAMS

		expected = pad_char * name_space
		actual = lim_char_str(func_input, *self.PARAMS)

		self.assertEqual(expected, actual)

	def test_below_length_limit_name_is_padded_to_limit_and_space(self):
		func_input = 'Below 20'
		lim, name_space, pad_char = self.PARAMS

		expected = func_input + (pad_char * (name_space - len(func_input)))
		actual = lim_char_str(func_input, *self.PARAMS)

		self.assertEqual(expected, actual)

	def test_exact_length_name_is_padded_to_space_but_otherwise_unchanged(self):
		func_input = 'Exactly 20 chars End'
		lim, name_space, pad_char = self.PARAMS

		expected = func_input + (pad_char * (name_space - len(func_input)))
		actual = lim_char_str(func_input, *self.PARAMS)

		self.assertEqual(expected, actual)

	def test_above_length_limit_name_is_cut_at_limit_and_padded_to_space(self):
		func_input = 'This name is above 20 characters!'
		lim, name_space, pad_char = self.PARAMS

		cut_off_name = func_input[:lim]

		expected = cut_off_name + (pad_char * (name_space - len(cut_off_name)))
		actual = lim_char_str(func_input, *self.PARAMS)

		self.assertEqual(expected, actual)


if __name__ == '__main__':
	unittest.main()
