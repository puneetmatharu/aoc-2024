import numpy as np
from math import prod
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Robot:
    p: tuple[int, int]
    v: tuple[int, int]
    room_size: tuple[int, int]

    def move(self, n: int):
        self.p = ((self.p[0] + (n * self.v[0])) % self.room_size[0], (self.p[1] + (n * self.v[1])) % self.room_size[1])
        return self


def load(f: Path, room_size: tuple[int, int]) -> list[str]:
    return [Robot(*[[int(x) for x in reversed(v[2:].split(","))] for v in line.split(" ")], room_size) for line in f.read_text().splitlines()]


def part1(file: Path, size: tuple[int, int]):
    def quadrant(r):
        (h2, w2) = (size[0] // 2, size[1] // 2)
        if r.p[0] == size[0] // 2 or r.p[1] == size[1] // 2:
            return None
        return (2 * (r.p[0] // (h2 + 1))) + (r.p[1] // (w2 + 1))
    quadrant_count = [0, 0, 0, 0]
    robots = load(file, size)
    for r in robots:
        r.move(n=100)
        if (q := quadrant(r)) is not None:
            quadrant_count[q] += 1
    return prod(quadrant_count)


def part2(file: Path, size: tuple[int, int]):
    def print_grid(robots):
        grid = np.full(size, " ", dtype=str)
        for r in robots:
            grid[*r.p] = '*'
        print("\n".join(["".join(row) for row in grid]))
    robots = load(file, size)
    num_robots = len(robots)
    for i in range(50000):
        for r in robots:
            r.move(n=1)
        if len(set([tuple(r.p) for r in robots])) == num_robots:
            print(f"ROUND #{i}")
            print_grid(robots)
            return i + 1


if __name__ == "__main__":
    output = part1(Path("example_data.txt"), (7, 11))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 12

    output = part1(Path("test_data.txt"), (103, 101))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 229868730

    output = part2(Path("test_data.txt"), (103, 101))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 7861
