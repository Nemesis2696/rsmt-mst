"""读 examples/*.txt，用简单平推求超图最小生成树。本文件由 AI 编写。"""

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from graph import HyperGraph

DEFAULTS = (
    ROOT / "examples" / "10-0.txt",
    ROOT / "examples" / "10-1.txt",
)
EXPECTED_MARK = "最短总长："


def parse_example(path):
    expected = None
    section = None
    pos = []
    wedges = []
    text = path.read_text(encoding="utf-8")
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            if EXPECTED_MARK in line:
                tail = line.split(EXPECTED_MARK, 1)[1].strip()
                expected = int(tail)
            continue
        if line == "nodes":
            section = "nodes"
            continue
        if line == "edges":
            section = "edges"
            continue
        if section == "nodes":
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"{path.name}:{lineno}: 坐标需要两个整数")
            pos.append((int(parts[0]), int(parts[1])))
            continue
        if section == "edges":
            if "|" not in line:
                raise ValueError(f"{path.name}:{lineno}: 超边需要用 | 分开端点和权重")
            left, right = line.split("|", 1)
            ends = [int(piece) for piece in left.split()]
            if len(ends) < 2:
                raise ValueError(f"{path.name}:{lineno}: 超边至少两个端点")
            wedges.append((ends, int(right.strip())))
            continue
        raise ValueError(f"{path.name}:{lineno}: nodes 之前出现了内容")
    if expected is None:
        raise ValueError(f"{path.name}: 缺少「{EXPECTED_MARK}」")
    if not pos or not wedges:
        raise ValueError(f"{path.name}: 缺少点或超边")
    count = len(pos)
    for ends, _weight in wedges:
        for node in ends:
            if node < 0 or node >= count:
                raise ValueError(f"{path.name}: 端点编号 {node} 超出 0..{count - 1}")
    return pos, wedges, expected


def solve(path):
    pos, wedges, expected = parse_example(path)
    hg = HyperGraph.from_wedges(wedges, pos=pos)
    mst = hg.cacu_mst2(debug=0, verbose_pic=0, verbose_text=0)
    return mst.len(), expected


def main(argv):
    if len(argv) > 1:
        paths = [Path(arg) for arg in argv[1:]]
    else:
        paths = list(DEFAULTS)
    failed = False
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
        got, expected = solve(path)
        print(f"{path.name}  length {got}  expected {expected}")
        if got != expected:
            failed = True
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main(sys.argv)
