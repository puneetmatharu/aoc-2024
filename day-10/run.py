import numpy as np
from pathlib import Path


def find_starts(data):
    return np.argwhere(data == 0)


def in_bounds(data, ij):
    return (0 <= ij[0] < data.shape[0]) and (0 <= ij[1] < data.shape[1])


def get_valid_directions(data, ij):
    return [new_pos for d in ((-1, 0), (1, 0), (0, -1), (0, 1)) if in_bounds(data, new_pos := ij + d) if ((data[*new_pos] - data[*ij]) == 1)]


def follow(data, s):
    return [tuple(s)] if data[*s] == 9 else [p for vd in get_valid_directions(data, s) for p in follow(data, vd)]


def count_trailheads(data):
    return sum([len(set(follow(data, s))) for s in find_starts(data)])


def trailhead_rating(data):
    return sum([len(follow(data, s)) for s in find_starts(data)])


def load(f: Path) -> list[str]:
    return np.array([[int(x) for x in list(line)] for line in f.read_text().splitlines()])


def part1(file: Path):
    return count_trailheads(load(file))


def part2(file: Path):
    return trailhead_rating(load(file))


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 36

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 496

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 81

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 1120
