from __future__ import annotations

import numpy as np
from pathlib import Path


class Plot:
    def __init__(self, x, plant):
        self.plant = str(plant)
        self.x = tuple(x)
        self.U = None
        self.R = None
        self.D = None
        self.L = None
        self.region_id = None

    def __str__(self):
        return f"Plot(x={self.x}, plant={self.plant}, region_id={self.region_id})"

    def __repr__(self):
        return str(self)

    def __eq__(self, p: Plot):
        return (list(self.x) == list(p.x)) and (str(self.plant) == str(p.plant))

    def is_surrounded(self):
        return all([self.U, self.R, self.D, self.L])

    def is_neighbour(self, p: Plot):
        result = (np.sum(np.abs(np.array(p.x) - self.x)) == 1) and (self.plant == p.plant)
        return result

    def add_neighbour(self, p: Plot):
        if not self.is_neighbour(p):
            raise ValueError(f"{p} not neighbour of {self}")
        offset = (np.array(p.x) - self.x).tolist()
        if offset == [-1, 0]:
            self.U = p
            p.D = self
        elif offset == [1, 0]:
            self.D = p
            p.U = self
        elif offset == [0, -1]:
            self.L = p
            p.R = self
        elif offset == [0, 1]:
            self.R = p
            p.L = self
        else:
            raise ValueError("Something went wrong")

    def neighbours(self):
        return [p for p in (self.U, self.R, self.D, self.L) if p is not None]

    def free_directions(self):
        return [d for d in ("U", "D", "L", "R") if getattr(self, d) is None]

    def free_boundaries(self):
        return sum([p is None for p in (self.U, self.R, self.D, self.L)])

    def free_neighbours(self):
        free = []
        if self.U is None:
            free += [(self.x[0] - 1, self.x[1])]
        if self.D is None:
            free += [(self.x[0] + 1, self.x[1])]
        if self.L is None:
            free += [(self.x[0], self.x[1] - 1)]
        if self.R is None:
            free += [(self.x[0], self.x[1] + 1)]
        return free


class Region:
    def __init__(self, ID: int, plots: list[Plot]):
        self.ID = ID
        self.plots = plots

    @property
    def plant(self):
        if len(self.plots) == 0:
            return None
        return self.plots[0].plant

    def print(self, size):
        print(f"Region #{self.ID} [type {self.plant}]:")
        rg = np.full(size, ".", dtype=str)
        for p in self.plots:
            rg[*p.x] = p.plant
            # print(f"{p.x} = {p.plant} | {p.free_boundaries()}")
        print("\n".join(["".join(row) for row in rg]))

    def area(self):
        return len(self.plots)

    def perimeter(self):
        return sum([p.free_boundaries() for p in self.plots])

    def sides(self):
        return []


class Farm:
    def __init__(self, grid: np.ndarray):
        self.shape = grid.shape
        self.regions = self.parse(grid)

    def in_bounds(self, x):
        return (0 <= x[0] < self.shape[0]) and (0 <= x[1] < self.shape[1])

    def parse(self, grid) -> None:
        plots = [Plot((i, j), grid[i, j]) for i in range(grid.shape[0]) for j in range(grid.shape[1])]
        ij_to_p_idx = {p.x:k for (k, p) in enumerate(plots)}

        # Generate region IDs
        region_id_to_plots = {}
        for (i, p) in enumerate(plots):
            p.region_id = i
            region_id_to_plots[i] = [*region_id_to_plots.get(i, []), i]

        # Merge plots via region ID
        for p1 in plots:
            for x_n in p1.free_neighbours():
                if not self.in_bounds(x_n):
                    continue
                p2 = plots[ij_to_p_idx[x_n]]
                if p1.is_neighbour(p2):
                    p1.add_neighbour(p2)
                    if (r1 := p1.region_id) == (r2 := p2.region_id):
                        continue
                    (r_new, r_old) = (min(r1, r2), max(r1, r2))
                    plots_to_merge = region_id_to_plots.pop(r_old)
                    for p_idx in plots_to_merge:
                        plots[p_idx].region_id = r_new
                    region_id_to_plots[r_new] += plots_to_merge

        regions = [Region(region_id, [plots[i] for i in plot_ids]) for (region_id, plot_ids) in region_id_to_plots.items()]
        return regions

    def perimeter_price(self):
        return sum([r.price() for r in self.regions])

    def print(self):
        print("\n"*5)
        for r in self.regions:
            r.print(self.shape)
        print("\n"*5)


def load(f: Path) -> list[str]:
    return np.array([list(line) for line in f.read_text().splitlines()], dtype=str)


def part1(file: Path):
    # Farm(load(file)).print()
    return sum([r.area() * r.perimeter() for r in Farm(load(file)).regions])


def part2(file: Path):
    return sum([r.area() * r.sides() for r in Farm(load(file)).regions])


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 1930

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 1473620

    # output = part2(Path("example_data.txt"))
    # print(f"[EXAMPLE] Part 2 output: {output}")
    # assert output == 1206

    # output = part2(Path("test_data.txt"))
    # print(f"[TEST] Part 2 output: {output}")
    # assert output == None
