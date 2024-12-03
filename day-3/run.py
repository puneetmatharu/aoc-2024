import re
from pathlib import Path


def load(f: Path) -> list[str]:
    return f.read_text()


def count(s):
    return sum([int(x) * int(y) for (x, y) in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", s)])


def part1(file: Path):
    return count(load(file))


def part2(file: Path):
    (total, enabled) = (0, True)
    for m in re.findall(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))", load(file)):
        enabled = ((m == "do()") if (m in ("do()", "don't()")) else enabled)
        total += count(m) * enabled
    return total


if __name__ == "__main__":
    output = part1(Path("example_data1.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 161

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 166630675

    output = part2(Path("example_data2.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 48

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 93465710
