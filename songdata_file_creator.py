from pathlib import Path
from typing import Callable
from typing import Iterable

from string_utilities import make_char_added_space
from string_utilities import make_limited_char_string

LONG_NAME_LIMIT: int = 20
LONG_NAME_SPACE: int = 48


def create_entry_counter_list(entry_count_list: Iterable) -> list[bytearray]:
	"""
	This function takes an iterable (usually, a list) that contains a number of lists,
	which contain a number of strings, which must be hexadecimal numbers with two digits.

	It returns a list of bytearrays of each hexadecimal digit.

	This is necessary because the counter entries that this function makes will be written to a file as bytes.
	Writing the name counter is part of the SONGDATA file structure.
	We write in bytes to ensure that there is less of a chance of "misunderstandings" like file encoding issues.

	:param entry_count_list: A list of lists of strings containing two digit hex numbers.
	:return: A list of bytearrays of hexadecimal values.
	"""

	_validate_input_create_entry_counter_list(entry_count_list)

	list_of_entry_counts = []

	for single_entry_count in entry_count_list:
		hex_count = [int(hex_pair, 16) for hex_pair in single_entry_count]
		list_of_entry_counts.append(bytearray(hex_count))

	return list_of_entry_counts


def write_songdata_file(all_counts: list[bytearray],
						last_entry: any,
						short_name_to_long_name_map: dict[str, str],
						output_file_path: str | Path,
						file_name_behavior: Callable[[str], bytes]) -> None:
	with open(output_file_path, 'xb') as f:
		complete_file_info = zip(short_name_to_long_name_map, all_counts)

		for short_file_name, current_count in complete_file_info:
			f.write(_create_long_file_name_from_short_file_name(short_file_name=short_file_name,
																short_name_to_long_name_map=short_name_to_long_name_map))

			if short_file_name != '':
				f.write(file_name_behavior(short_file_name))
			else:
				f.write(_create_null_spacing_bytes())

			if short_file_name == last_entry[0]:
				f.write(_create_current_count_last_entry(current_count))
			else:
				f.write(_create_current_count_normal(current_count))


def _create_long_file_name_from_short_file_name(short_file_name: str,
												short_name_to_long_name_map: dict[str, str]) -> bytes:
	"""
	This function writes a long file name properly into a SONGDATA.DIR file.
	It looks up a long name from the short name to find the correct long name to write.

	:param short_file_name: A short file name that can be found in short_name_to_long_name_map. It must be there, or this function will raise KeyError.
	:param short_name_to_long_name_map: A dictionary with which to look up the long name from the short name.
	"""
	return bytes(make_limited_char_string(short_name_to_long_name_map[short_file_name],
										  LONG_NAME_LIMIT,
										  LONG_NAME_SPACE).encode('utf-8'))


def _create_directory_name(name: str) -> bytes:
	return bytes(name.encode("utf-8"))


def _create_short_file_name(short_file_name: str) -> bytes:
	return bytes(
		(make_char_added_space(short_file_name, spaces_to_fill=8, space_char='\x20') + 'MID').encode('utf-8')
	)


creator_directory = _create_directory_name
creator_normal = _create_short_file_name


def _create_null_spacing_bytes() -> bytes:
	return bytes(
		('\x00' * 8 + '\x00' * 3).encode('utf-8')
	)


def _create_current_count_last_entry(current_count: bytearray) -> bytes:
	return bytes(
		b'\x00' * 3 + current_count[3:]
	)


def _create_current_count_normal(current_count) -> bytes:
	return bytes(current_count)


def _validate_input_create_entry_counter_list(entry_count_list: Iterable) -> None:
	"""
	This function validates that an iterable passed to it will work properly with
	the create_entry_counter_list function. If it is found that it will work, nothing happens.
	If something is not right with the input, it raises an exception, depending on what went wrong.

	:param entry_count_list: What should be the list of lists of strings containing two digit hex numbers.
	"""
	for counting_entry in entry_count_list:
		for hex_pair in counting_entry:
			if len(hex_pair) != 2:
				raise ValueError("Each entry in each hex pair in entry_count_list must be only two digits long.")

			try:
				_ = int(hex_pair, 16)
			except ValueError:
				raise ValueError("Each entry in each hex pair in entry_count_list must be a valid hexadecimal literal.")
