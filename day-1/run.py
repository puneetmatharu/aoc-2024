import re
import numpy as np
from pathlib import Path


def load(f: Path) -> list[str]:
    return [np.sort(sa.squeeze()) for sa in np.split(np.array([[int(x) for x in re.sub(r'\s+', ' ', line).split(" ")] for line in Path(f).read_text().splitlines()]), 2, axis=-1)]


def part1(file: Path):
    return sum([abs(x - y) for (x, y) in zip(*load(file))])


def part2(file: Path):
    (arr1, arr2) = load(file)
    return sum([x * {int(v): c for (v, c) in zip(*np.unique(arr2, return_counts=True))}.get(int(x), 0) for x in arr1])


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 11

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 1341714

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 31

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 27384707
