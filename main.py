from argparse import ArgumentParser
from inspect import cleandoc
from pathlib import Path
from typing import Callable

from csv_tools import find_last_csv_entry
from csv_tools import read_csv_and_convert
from songdata_file_creator import create_entry_counter_list
from songdata_file_creator import creator_directory
from songdata_file_creator import creator_normal
from songdata_file_creator import write_songdata_file


def _create_argument_parser() -> ArgumentParser:
	parser = ArgumentParser()

	parser.add_argument("input", help="Input library, as csv")
	parser.add_argument("output", help="Output file, in 'SONGDATA.DIR' format")

	parser.add_argument("-f", "--file-name",
						help="Specify the name of the file stored. Default: 'SONGDATA.DIR'",
						default="SONGDATA.DIR")
	parser.add_argument("-d", "--directory-file",
						help="Specify if the file to be created should be of the directory style. Default: No",
						action="store_true", default=False)

	return parser


def main(arg_parser: ArgumentParser) -> None:
	ENTRY_COUNTER_PATH = 'data-files/standard-counted-entries.csv'

	args = arg_parser.parse_args()

	library_name_path = Path(args.input)
	output_file_path = Path(args.output) / args.file_name

	output_file_path.parent.mkdir(parents=True, exist_ok=True)

	short_name_to_long_name_map: dict = read_csv_and_convert(library_name_path, dict)
	entry_counts: list = read_csv_and_convert(ENTRY_COUNTER_PATH, list)

	last_entry = find_last_csv_entry(library_name_path)
	hex_counter: list[bytearray] = create_entry_counter_list(entry_counts)

	file_name_behavior: Callable[[str], bytes] = creator_directory if args.directory_file else creator_normal

	write_songdata_file(hex_counter, last_entry, short_name_to_long_name_map, output_file_path, file_name_behavior)


if __name__ == '__main__':
	arg_parser = _create_argument_parser()

	try:
		main(arg_parser)
	except FileNotFoundError:
		print()
		arg_parser.exit(status=3, message=
		cleandoc("""
			The file you specified for input does not exist.
			Please check the path, and try again.
		""") + "\n\n")
	except FileExistsError:
		print()
		arg_parser.exit(status=4, message=
		cleandoc("""
			The file you specified for output already exists. 
			For safety, you may not overwrite existing files with this tool.
			Change the output file path or rename the output file name, or rename or delete the existing file.
		""") + "\n\n")
	except PermissionError:
		print()
		arg_parser.exit(status=5, message=
		cleandoc("""
			You do not have the proper permissions to access a location.
			You might have entered a directory instead of a file as the input library path. 
			Have you entered the input library path properly?
		""") + "\n\n")
