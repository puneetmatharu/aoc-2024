from __future__ import annotations

import numpy as np
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Plot:
    x: tuple[int, int]
    U: Plot
    R: Plot
    D: Plot
    L: Plot

    def is_neighbour(self)


@dataclass
class Region:
    plots: list[Plot]

    def in_region(self, p: Plot):

        self.plots += [p]

    def add(self, p: Plot):
        self.plots += [p]


class Farm:
    def __init__(self, grid: np.ndarray):
        self.parse(grid)

    def in_region(self, grid) -> int:
        pass

    def parse(self, grid) -> None:
        pass




def load(f: Path) -> list[str]:
    return np.array([list(line) for line in f.read_text().splitlines()], dtype=str)


def part1(file: Path):
    raise NotImplementedError()


def part2(file: Path):
    raise NotImplementedError()


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == None

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == None

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == None

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == None
