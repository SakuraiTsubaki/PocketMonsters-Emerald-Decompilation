#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

BLOCK_SIZE = 64 * 1024


def game_code(data: bytes) -> str:
    if len(data) < 0xB0:
        raise ValueError("input is too small to contain a GBA header")
    return data[0xAC:0xB0].decode("ascii", "replace")


def compare(a: bytes, b: bytes) -> dict:
    if len(a) != len(b):
        raise ValueError("ROM sizes differ")

    differing = 0
    first = None
    last = None
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            differing += 1
            if first is None:
                first = i
            last = i

    identical_blocks = sum(
        a[offset:offset + BLOCK_SIZE] == b[offset:offset + BLOCK_SIZE]
        for offset in range(0, len(a), BLOCK_SIZE)
    )

    return {
        "size_bytes": len(a),
        "differing_bytes": differing,
        "differing_fraction": differing / len(a) if a else 0.0,
        "differing_percent": (100.0 * differing / len(a)) if a else 0.0,
        "block_size": BLOCK_SIZE,
        "block_count": (len(a) + BLOCK_SIZE - 1) // BLOCK_SIZE,
        "identical_blocks": identical_blocks,
        "first_difference_offset": first,
        "last_difference_offset": last,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare local Emerald ROM variants without modifying or redistributing them."
    )
    parser.add_argument("roms", nargs="+", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args()

    inputs = {}
    for path in args.roms:
        data = path.read_bytes()
        code = game_code(data)
        if code in inputs:
            if inputs[code]["data"] != data:
                raise ValueError(f"multiple non-identical inputs use game code {code}")
            inputs[code]["names"].append(path.name)
            continue
        inputs[code] = {"data": data, "names": [path.name]}

    pairs = []
    for left, right in itertools.combinations(sorted(inputs), 2):
        row = compare(inputs[left]["data"], inputs[right]["data"])
        row.update({"left": left, "right": right})
        pairs.append(row)

    report = {
        "format": "emerald-cross-variant-byte-comparison-v1",
        "unique_game_codes": sorted(inputs),
        "block_size": BLOCK_SIZE,
        "pairs": pairs,
    }

    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
