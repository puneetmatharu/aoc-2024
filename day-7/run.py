from pathlib import Path
from operator import add, mul


def load(f: Path) -> list[str]:
    vals = [line.split(": ") for line in f.read_text().splitlines()]
    vals = [(int(v[0]), [int(x) for x in v[1].split(" ")]) for v in vals]
    return vals


def apply(nums: list[int], ops: list[callable]) -> int:
    return [op(nums[0], nums[1]) for op in ops] if (len(nums) == 2) else [x for v in apply(nums[:2], ops) for x in apply([v, *nums[2:]], ops)]


def part1(file: Path):
    return sum([target for (target, nums) in load(file) if target in apply(nums, [add, mul])])


def part2(file: Path):
    concat = lambda x, y: int(f"{x}{y}")
    return sum([target for (target, nums) in load(file) if target in apply(nums, [add, mul, concat])])


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 3749

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 1430271835320

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 11387

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 456565678667482
