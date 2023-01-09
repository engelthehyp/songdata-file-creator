import csv
from pathlib import Path
from typing import Callable


def read_csv_and_convert(path: str | Path, transformer: Callable[[csv.reader], any]) -> any:
	with open(path, newline='') as table:
		reader = csv.reader(table)
		return transformer(reader)


def find_last_csv_entry(path: str | Path) -> any:
	csv_file = read_csv_and_convert(path, list)
	return csv_file[-1]
