from functools import cmp_to_key
from pathlib import Path


def load(f: Path) -> list[str]:
    text = f.read_text().splitlines()
    i = text.index("")
    rules = [[int(x) for x in rule.split("|")] for rule in text[:i]]
    deps = {k: set() for pair in rules for k in pair}
    for (x, y) in rules:
        deps[x] |= set([y])
    updates = [[int(x) for x in update.split(",")] for update in text[i + 1:]]
    return (deps, updates)


def is_correctly_ordered(update, deps) -> bool:
    return all([len(set(update[:i]) & deps[update[i]]) == 0 for i in range(len(update))])


def part1(file: Path):
    (deps, updates) = load(file)
    return sum([u[len(u) // 2] for u in updates if is_correctly_ordered(u, deps)])


def part2(file: Path):
    (deps, updates) = load(file)
    return sum([(su := sorted(u, key=cmp_to_key(lambda x, y: -1 if y in deps[x] else 1)))[len(su) // 2] for u in updates if not is_correctly_ordered(u, deps)])


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 143

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 5391

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 123

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 6142
