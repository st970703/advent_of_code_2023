import re
from dataclasses import dataclass
from operator import attrgetter


def get_seeds(line: str):
    return {int(num_str) for num_str in re.split("\\s+", line) if num_str and num_str.isdigit()}


@dataclass
class RangeData:
    dest_range_start: int
    src_range_start: int
    range_length: int

    def dest_range_end(self) -> int:
        return self.dest_range_start + self.range_length - 1

    def src_range_end(self) -> int:
        return self.src_range_start + self.range_length - 1

    def is_num_within_src_range(self, num: int) -> bool:
        return True if (
            self.src_range_start <= num <= self.src_range_end()
        ) else False

    def get_diff(self) -> int:
        return self.dest_range_start - self.src_range_start

    def get_dest_from_src(self, num: int) -> int | None:
        if self.is_num_within_src_range(num=num):
            return num + self.get_diff()

def get_location_for_seed(
    seed: int,
    seed_to_soil_map_list: list,
    soil_to_fertilizer_map_list: list,
    fertilizer_to_water_map_list: list,
    water_to_light_map_list: list,
    light_to_temperature_map_list: list,
    temperature_to_humidity_map_list: list,
    humidity_to_location_map_list: list,
) -> int | None:
    soil = None
    for seed_to_soil in seed_to_soil_map_list:
        if seed_to_soil.get_dest_from_src(num=seed):
            soil = seed_to_soil.get_dest_from_src(num=seed)
            break
    if not soil:
        soil = seed

    fertilizer = None
    for soil_to_fertilizer in soil_to_fertilizer_map_list:
        if soil_to_fertilizer.get_dest_from_src(num=soil):
            fertilizer = soil_to_fertilizer.get_dest_from_src(num=soil)
            break
    if not fertilizer:
        fertilizer = soil

    water = None
    for fertilizer_to_water in fertilizer_to_water_map_list:
        if fertilizer_to_water.get_dest_from_src(num=fertilizer):
            water = fertilizer_to_water.get_dest_from_src(num=fertilizer)
            break
    if not water:
        water = fertilizer

    light = None
    for water_to_light in water_to_light_map_list:
        if water_to_light.get_dest_from_src(num=water):
            light = water_to_light.get_dest_from_src(num=water)
            break
    if not light:
        light = water

    temperature = None
    for light_to_temperature in light_to_temperature_map_list:
        if light_to_temperature.get_dest_from_src(num=light):
            temperature = light_to_temperature.get_dest_from_src(num=light)
            break
    if not temperature:
        temperature = light

    humidity = None
    for temperature_to_humidity in temperature_to_humidity_map_list:
        if temperature_to_humidity.get_dest_from_src(num=temperature):
            humidity = temperature_to_humidity.get_dest_from_src(num=temperature)
            break
    if not humidity:
        humidity = temperature

    location = None
    for humidity_to_location in humidity_to_location_map_list:
        if humidity_to_location.get_dest_from_src(num=humidity):
            location = humidity_to_location.get_dest_from_src(num=humidity)
            break
    if not location:
        location = humidity

    return location

if __name__ == '__main__':
    file_path = "part_1_input.txt"
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

        seed_to_soil_map_list = []
        soil_to_fertilizer_map_list = []
        fertilizer_to_water_map_list = []
        water_to_light_map_list = []
        light_to_temperature_map_list = []
        temperature_to_humidity_map_list = []
        humidity_to_location_map_list = []

        i: int
        line: str
        for i, line in enumerate(lines):
            if "seeds: " in line:
                seeds = get_seeds(line=line)
            if "-to-" and " map:" in line:
                map_name = line
                for x in range(i + 1, len(lines) + 1):
                    if x >= len(lines):
                        break
                    if lines[x] == "":
                        break
                    if "-to-" and " map:" in lines[x]:
                        break
                    dest_range_start_str, src_range_start_str, range_length_str = re.split("\\s+", lines[x])
                    dest_range_start = int(dest_range_start_str)
                    src_range_start = int(src_range_start_str)
                    range_length = int(range_length_str)
                    range_data = RangeData(
                        dest_range_start=dest_range_start,
                        src_range_start=src_range_start,
                        range_length=range_length,
                    )
                    if map_name == "seed-to-soil map:":
                        seed_to_soil_map_list.append(range_data)
                    elif map_name == "soil-to-fertilizer map:":
                        soil_to_fertilizer_map_list.append(range_data)
                    elif map_name == "fertilizer-to-water map:":
                        fertilizer_to_water_map_list.append(range_data)
                    elif map_name == "water-to-light map:":
                        water_to_light_map_list.append(range_data)
                    elif map_name == "light-to-temperature map:":
                        light_to_temperature_map_list.append(range_data)
                    elif map_name == "temperature-to-humidity map:":
                        temperature_to_humidity_map_list.append(range_data)
                    elif map_name == "humidity-to-location map:":
                        humidity_to_location_map_list.append(range_data)

    sorted(seed_to_soil_map_list, key=attrgetter('src_range_start'))
    sorted(soil_to_fertilizer_map_list, key=attrgetter('src_range_start'))
    sorted(fertilizer_to_water_map_list, key=attrgetter('src_range_start'))
    sorted(water_to_light_map_list, key=attrgetter('src_range_start'))
    sorted(light_to_temperature_map_list, key=attrgetter('src_range_start'))
    sorted(temperature_to_humidity_map_list, key=attrgetter('src_range_start'))
    sorted(humidity_to_location_map_list, key=attrgetter('src_range_start'))

    locations = [
        get_location_for_seed(
            seed=seed,
            seed_to_soil_map_list=seed_to_soil_map_list,
            soil_to_fertilizer_map_list=soil_to_fertilizer_map_list,
            fertilizer_to_water_map_list=fertilizer_to_water_map_list,
            water_to_light_map_list=water_to_light_map_list,
            light_to_temperature_map_list=light_to_temperature_map_list,
            temperature_to_humidity_map_list=temperature_to_humidity_map_list,
            humidity_to_location_map_list=humidity_to_location_map_list,
        )
        for seed in seeds
    ]

    if file_path == "part_1_sample_input.txt":
        assert min(locations) == 35
    print(min(locations))
