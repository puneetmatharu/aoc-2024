import numpy as np
from pathlib import Path
from numpy.linalg import solve as lasolve


def solve(ax, ay, bx, by, px, py, offset: int = 0):
    (a, b) = np.rint(lasolve([[ax, bx], [ay, by]], [px + offset, py + offset])).astype(np.int64).tolist()
    return (3 * a) + b if ((a >= 0) and (b >= 0)) and (((a * ax) + (b * bx) == (px + offset)) and (((a * ay) + (b * by) == (py + offset)))) else None


def load(f: Path) -> list[str]:
    return [[v for line in game.splitlines() for v in [int(s[2:]) for s in line.split(": ")[1].split(", ")]] for game in f.read_text().split("\n\n")]


def part1(file: Path):
    return sum([soln for g in load(file) if (soln := solve(*g)) is not None])


def part2(file: Path):
    return sum([soln for g in load(file) if (soln := solve(*g, offset=10**13)) is not None])


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 480

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 29522

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 875318608908

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 101214869433312
