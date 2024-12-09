from dataclasses import dataclass
from pathlib import Path


@dataclass
class Block:
    value: str
    size: int
    moved: bool = False


@dataclass
class Disk:
    blocks: list[Block]

    def find_free(self, sz: int, stop: int | None = None):
        for i in range(stop or len(self.blocks)):
            if (self.blocks[i].value == ".") and (self.blocks[i].size >= sz):
                return i
        return None

    def find_last_unmoved_block(self):
        for i in range(len(self.blocks) - 1, -1, -1):
            if (self.blocks[i].value != ".") and (not self.blocks[i].moved):
                return i
        return None

    def move(self, i_file: int, j_space: int):
        s = self.blocks[j_space]
        f = self.blocks[i_file]
        sz_diff = s.size - f.size
        s.value = f.value
        f.value = "."
        s.moved = True
        if sz_diff == 0:
            return self
        s.size = f.size
        self.blocks.insert(j_space + 1, Block(".", sz_diff))
        return self

    def defragment(self):
        while True:
            i_file = self.find_last_unmoved_block()
            if i_file is None:
                break
            j_free = self.find_free(sz=self.blocks[i_file].size, stop=i_file)
            if (j_free is None) or (j_free > i_file):
                self.blocks[i_file].moved = True
                continue
            self.move(i_file, j_free)
        return self

    def checksum(self):
        (csum, idx) = (0, 0)
        for b in self.blocks:
            if b.value != ".":
                csum += b.value * sum(range(idx, idx + b.size))
            idx += b.size
        return csum


def load(f: Path) -> list[str]:
    return f.read_text()


def part1(file: Path):
    disk = Disk([Block(value=((i // 2) if (i % 2 == 0) else "."), size=1, moved=False) for (i, s) in enumerate(list(load(file))) if int(s) != 0 for _ in range(int(s))])
    return disk.defragment().checksum()


def part2(file: Path):
    disk = Disk([Block(value=((i // 2) if (i % 2 == 0) else "."), size=int(s), moved=False) for (i, s) in enumerate(list(load(file))) if int(s) != 0])
    return disk.defragment().checksum()


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 1928

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 6283404590840

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 2858

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 6304576012713
