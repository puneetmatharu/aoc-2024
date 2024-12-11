import numpy as np
from pathlib import Path


def load(f: Path) -> list[str]:
    return [int(x) for x in f.read_text().split(" ")]


def apply_rules(x):
    return [1] if (x == 0) else ([int(s[:len(s) // 2]), int(s[len(s) // 2:])] if ((len(s := f"{x}")) % 2 == 0) else [2024 * x])


def run(stones: list[int], num_blinks: int):
    history = {}
    stones = {int(v): int(c) for (v, c) in zip(*np.unique(stones, return_counts=True))}
    for _ in range(num_blinks):
        new_stones = {}
        [new_stones.update({ns: new_stones.get(ns, 0) + count}) for (stone, count) in stones.items() for ns in (history[stone] if stone in history else apply_rules(stone))]
        stones = new_stones
    return sum(stones.values())


def part1(file: Path):
    return run(load(file), 25)


def part2(file: Path):
    return run(load(file), 75)


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 55312

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 189167

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 225253278506288
