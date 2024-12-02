from pathlib import Path
import numpy as np


def load(f: Path) -> list[str]:
    return [[int(x) for x in line.split(" ")] for line in f.read_text().splitlines()]


def count_safe(rs):
    return sum([all([1 <= d <= 3 for d in np.diff(r)]) or all([-3 <= d <= -1 for d in np.diff(r)]) for r in rs])


def part1(file: Path):
    return count_safe(load(file))


def part2(file: Path):
    return sum([count_safe([[*r[:i], *r[i + 1:]] for i in range(len(r) + 1)]) >= 1 for r in load(file)])


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 2

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 421

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 4

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 476
