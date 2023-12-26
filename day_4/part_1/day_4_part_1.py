from dataclasses import dataclass, field

def find_common_numbers_from_line(line) -> set[int]:
    left_numbers, right_numbers = line.split(": ")[1].split(" | ")
    left_numbers = {int(num_str) for num_str in left_numbers.split(" ") if num_str}
    right_numbers = {int(num_str) for num_str in right_numbers.split(" ") if num_str}
    return left_numbers & right_numbers

if __name__ == '__main__':
    file_path = "day_4_part_1_input.txt"
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

        total_score = 0

        i: int
        line: str
        for i, line in enumerate(lines):
            common_numbers = find_common_numbers_from_line(line)
            if len(common_numbers) > 0:
                score = 2**(len(common_numbers) - 1)
                total_score += score
    print(total_score)
