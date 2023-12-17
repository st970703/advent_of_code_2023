from dataclasses import dataclass, field


def is_a_symbol(char: str):
    if char != "." and not char.isdigit():
        return True
    else:
        return False

@dataclass
class NumAsStrAndInfo:
    starting_col_index: int | None = field(default=None)
    ending_col_index: int | None = field(default=None)
    row_index: int | None = field(default=None)
    num_as_str: str = field(default='')
    source_line: str = field(default='')

    def append_num_str(self, num_as_char: str):
        self.num_as_str += num_as_char

def get_list_of_ints_from_each_line(line: str, lines: list[str], row_index: int) -> list[int]:
    num_as_str_and_info = NumAsStrAndInfo(row_index=row_index, source_line=line)
    list_of_ints: list[int] = []
    for x in range(0, len(line)):
        if line[x].isdigit():
            if num_as_str_and_info.starting_col_index is None:
                num_as_str_and_info.starting_col_index = x
            num_as_str_and_info.append_num_str(line[x])

            if x == len(line) - 1:
                num_as_str_and_info.ending_col_index = x
                if check_extended_rectangle_for_symbol(num_as_str_and_info=num_as_str_and_info, lines=lines):
                    list_of_ints.append(int(num_as_str_and_info.num_as_str))
        else:
            if num_as_str_and_info.starting_col_index is not None and num_as_str_and_info.num_as_str != '':
                # end of a valid number as str
                num_as_str_and_info.ending_col_index = x - 1
                if check_extended_rectangle_for_symbol(num_as_str_and_info=num_as_str_and_info, lines=lines):
                    list_of_ints.append(int(num_as_str_and_info.num_as_str))
            num_as_str_and_info = NumAsStrAndInfo(row_index=row_index, source_line=line)
    return list_of_ints


def check_extended_rectangle_for_symbol(num_as_str_and_info: NumAsStrAndInfo, lines: list[str]) -> bool:
    matrix_size = len(lines)
    row_lower_bound = num_as_str_and_info.row_index - 1 if not num_as_str_and_info.row_index == 0 else 0
    row_upper_bound = num_as_str_and_info.row_index + 1 if not num_as_str_and_info.row_index == matrix_size - 1 else matrix_size - 1
    col_lower_bound = num_as_str_and_info.starting_col_index - 1 if not num_as_str_and_info.starting_col_index == 0 else 0
    col_upper_bound = num_as_str_and_info.ending_col_index + 1 if not num_as_str_and_info.ending_col_index == matrix_size - 1 else matrix_size - 1
    for x in range(row_lower_bound, row_upper_bound + 1):
        for y in range(col_lower_bound, col_upper_bound + 1):
            if is_a_symbol(lines[x][y]):
                return True
    return False



if __name__ == '__main__':
    file_path = "day_3_part_1_input.txt"
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
        part_number_sum: int = 0

        all_nums = []

        i: int
        line: str
        for i, line in enumerate(lines):
            list_of_ints = get_list_of_ints_from_each_line(line=line, row_index=i, lines=lines)
            part_number_sum += sum(list_of_ints)
            all_nums = [*all_nums, *list_of_ints]
    assert part_number_sum == 507214
