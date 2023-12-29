from collections import defaultdict
import re

def find_common_numbers_from_line(line) -> set[int]:
    left_numbers, right_numbers = line.split(": ")[1].split(" | ")
    left_numbers = {int(num_str) for num_str in re.split("\\s+", left_numbers) if num_str}
    right_numbers = {int(num_str) for num_str in re.split("\\s+", right_numbers) if num_str}
    return left_numbers & right_numbers


if __name__ == '__main__':
    file_path = "day_4_part_2_input.txt"
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

        card_number_to_copies_mapping = defaultdict(int)

        i: int
        line: str
        for i, line in enumerate(lines):
            card_num_str = line.split(": ")[0]
            card_num = [int(card_num) for card_num in re.split("\\s+", card_num_str) if card_num.isdigit()][0]
            card_number_to_copies_mapping[card_num] += 1
            common_numbers = find_common_numbers_from_line(line)
            if not common_numbers:
                continue
            for _ in range(1,  card_number_to_copies_mapping[card_num] + 1, 1):
                for j in range(1, len(common_numbers) + 1, 1):
                    card_number_to_copies_mapping[card_num + j] += 1

    total_scores = sum(list(card_number_to_copies_mapping.values()))

    if file_path == "day_4_part_2_sample_input.txt":
        assert total_scores == 30

    print(total_scores)
