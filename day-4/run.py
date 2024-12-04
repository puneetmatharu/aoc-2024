from pathlib import Path
import numpy as np


def load(f: Path) -> list[str]:
    return np.array([list(line) for line in f.read_text().splitlines()], dtype=str)


def part1(file: Path):
    x = np.pad(load(file), offset := 3, constant_values=".")
    return sum([sm in ("XMAS", "SAMX") for i in range(offset, x.shape[0] - offset) for j in range(offset, x.shape[1] - offset) for sm in ("".join(x[i:i + 4, j]), "".join(x[i, j:j + 4]), "".join(x[range(i, i + 4), range(j, j + 4)]), "".join(x[range(i, i - 4, -1), range(j, j + 4)]))])


def part2(file: Path):
    x = np.pad(load(file), offset := 3, constant_values=".")
    return sum([1 if ("".join(x[range(i - 1, i + 2), range(j - 1, j + 2)]) in ("MAS", "SAM")) and ("".join(x[range(i + 1, i - 2, -1), range(j - 1, j + 2)]) in ("MAS", "SAM")) else 0 for i in range(offset, x.shape[0] - offset) for j in range(offset, x.shape[1] - offset)])


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 18

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 2496

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 9

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 1967
