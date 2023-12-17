from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class NumAsStrAndInfo:
    starting_col_index: int | None = field(default=None)
    ending_col_index: int | None = field(default=None)
    row_index: int | None = field(default=None)
    num_as_str: str = field(default='')
    source_line: str = field(default='')

    def append_num_str(self, num_as_char: str):
        self.num_as_str += num_as_char


@dataclass
class Coordinate:
    row_index: int | None = field(default=None)
    col_index: int | None = field(default=None)


def get_gear_coordinate_in_extended_rectangle(num_as_str_and_info: NumAsStrAndInfo, lines: list[str]) -> Coordinate | None:
    matrix_size = len(lines)
    row_lower_bound = num_as_str_and_info.row_index - 1 if not num_as_str_and_info.row_index == 0 else 0
    row_upper_bound = num_as_str_and_info.row_index + 1 if not num_as_str_and_info.row_index == matrix_size - 1 else matrix_size - 1
    col_lower_bound = num_as_str_and_info.starting_col_index - 1 if not num_as_str_and_info.starting_col_index == 0 else 0
    col_upper_bound = num_as_str_and_info.ending_col_index + 1 if not num_as_str_and_info.ending_col_index == matrix_size - 1 else matrix_size - 1
    for x in range(row_lower_bound, row_upper_bound + 1):
        for y in range(col_lower_bound, col_upper_bound + 1):
            if lines[x][y] == '*':
                return Coordinate(row_index=x, col_index=y)


def calculate_gear_ratio(part_numbers: list[NumAsStrAndInfo]) -> int | None:
    if len(part_numbers) == 2:
        return int(part_numbers[0].num_as_str) * int(part_numbers[1].num_as_str)


if __name__ == '__main__':
    file_path = "day_3_part_2_input.txt"
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

        # note: 'row_index_col_index' of the gear
        # is the dict key
        gear_coordinates_to_part_numbers_mapping: dict[str, list[NumAsStrAndInfo]] = defaultdict(list[NumAsStrAndInfo])

        sum_of_gear_ratios = 0

        row_num: int
        line: str
        for row_num, line in enumerate(lines):
            num_as_str_and_info = NumAsStrAndInfo(row_index=row_num, source_line=line)
            for col_index in range(0, len(line)):
                if line[col_index].isdigit():
                    if num_as_str_and_info.starting_col_index is None:
                        num_as_str_and_info.starting_col_index = col_index
                    num_as_str_and_info.append_num_str(line[col_index])

                    # This is a number that ends on the right end of the line
                    if col_index == len(line) - 1:
                        num_as_str_and_info.ending_col_index = col_index
                        gear_coordinate = get_gear_coordinate_in_extended_rectangle(
                            num_as_str_and_info=num_as_str_and_info, lines=lines)
                        if gear_coordinate:
                            computed_key = f'{gear_coordinate.row_index}_{gear_coordinate.col_index}'
                            gear_coordinates_to_part_numbers_mapping[computed_key].append(num_as_str_and_info)

                else:
                    if num_as_str_and_info.starting_col_index is not None and num_as_str_and_info.num_as_str != '':
                        # end of a valid number as str
                        num_as_str_and_info.ending_col_index = col_index - 1
                        gear_coordinate = get_gear_coordinate_in_extended_rectangle(
                            num_as_str_and_info=num_as_str_and_info, lines=lines)
                        if gear_coordinate:
                            computed_key = f'{gear_coordinate.row_index}_{gear_coordinate.col_index}'
                            gear_coordinates_to_part_numbers_mapping[computed_key].append(num_as_str_and_info)
                    num_as_str_and_info = NumAsStrAndInfo(row_index=row_num, source_line=line)

        for part_numbers in gear_coordinates_to_part_numbers_mapping.values():
            gear_ratio = calculate_gear_ratio(part_numbers=part_numbers)
            if gear_ratio:
                sum_of_gear_ratios += gear_ratio

    print(sum_of_gear_ratios)