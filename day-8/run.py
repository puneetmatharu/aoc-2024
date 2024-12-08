import numpy as np
from pathlib import Path
from itertools import combinations


def load(f: Path) -> list[str]:
    return np.array([list(line) for line in f.read_text().splitlines()], dtype=str)


def group_antennae(grid, posns):
    ga = dict()
    for p in posns:
        a = str(grid[*p])
        ga[a] = [*ga.get(a, []), p]
    return ga


def construct_antinodes_pt1(ij1, ij2):
    (nij1, nij2) = (np.array(ij1), np.array(ij2))
    d = nij2 - nij1
    return ((nij1 - d).tolist(), (nij2 + d).tolist())


def construct_antinodes_pt2(g, ij1, ij2):
    (nij1, nij2) = (np.array(ij1), np.array(ij2))
    d = nij2 - nij1
    mult = min((g.shape[0] // abs(d[0])), (g.shape[1] // abs(d[1])))
    return [an.tolist() for i in range(mult) for an in ((nij1 - (i * d)), (nij2 + (i * d)))]


def out_of_bounds(g, i, j):
    return not ((0 <= i < g.shape[0]) and ((0 <= j < g.shape[1])))


def find_all_antinodes(grid, an_fn):
    ps = set([tuple(an) for an in np.argwhere(grid != ".")])
    ga = group_antennae(grid, ps)
    ans = set()
    for v in ga.values():
        if len(v) == 1:
            continue
        combs = list(combinations(v, 2))
        for (a1, a2) in combs:
            for an in an_fn(a1, a2):
                if ((0 <= an[0] < grid.shape[0]) and ((0 <= an[1] < grid.shape[1]))):
                    ans |= set([tuple(an)])
    return len(ans)


def part1(file: Path):
    return find_all_antinodes(load(file), construct_antinodes_pt1)


def part2(file: Path):
    return find_all_antinodes((g := load(file)), lambda i, j : construct_antinodes_pt2(g, i, j))


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 14

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 332

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 34

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 1174
