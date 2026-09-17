#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROM_SIZE = 16 * 1024 * 1024
REGIONS = {
    "BPEJ": "Japan / Japanese",
    "BPEE": "USA/Europe / English",
    "BPED": "Germany / German",
    "BPEF": "France / French",
    "BPEI": "Italy / Italian",
    "BPES": "Spain / Spanish",
}


def digest(data: bytes, name: str) -> str:
    h = hashlib.new(name)
    h.update(data)
    return h.hexdigest()


def inspect(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < 0xBE:
        raise ValueError(f"{path}: too small to contain a GBA header")

    title = data[0xA0:0xAC].decode("ascii", "replace").rstrip("\0 ")
    game_code = data[0xAC:0xB0].decode("ascii", "replace")
    maker_code = data[0xB0:0xB2].decode("ascii", "replace")
    fixed_value = data[0xB2]
    software_version = data[0xBC]
    stored_checksum = data[0xBD]
    calculated_checksum = (-sum(data[0xA0:0xBD]) - 0x19) & 0xFF

    return {
        "path": str(path),
        "name": path.name,
        "size_bytes": len(data),
        "expected_emerald_size": len(data) == ROM_SIZE,
        "sha256": digest(data, "sha256"),
        "sha1": digest(data, "sha1"),
        "md5": digest(data, "md5"),
        "header": {
            "title": title,
            "game_code": game_code,
            "language_region": REGIONS.get(game_code, "unknown"),
            "maker_code": maker_code,
            "fixed_value": f"0x{fixed_value:02X}",
            "fixed_value_valid": fixed_value == 0x96,
            "software_version": software_version,
            "stored_complement_checksum": f"0x{stored_checksum:02X}",
            "calculated_complement_checksum": f"0x{calculated_checksum:02X}",
            "complement_checksum_valid": stored_checksum == calculated_checksum,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fingerprint local Pokemon Emerald GBA ROM inputs without modifying them."
    )
    parser.add_argument("roms", nargs="+", type=Path)
    parser.add_argument("--output", "-o", type=Path, help="Write JSON report to this path")
    args = parser.parse_args()

    rows = [inspect(path) for path in args.roms]
    groups: dict[str, list[str]] = {}
    for row in rows:
        groups.setdefault(row["sha256"], []).append(row["name"])

    report = {
        "format": "emerald-rom-fingerprint-v1",
        "input_count": len(rows),
        "unique_sha256_count": len(groups),
        "roms": rows,
        "duplicate_groups": [
            {"sha256": sha256, "names": names}
            for sha256, names in sorted(groups.items())
            if len(names) > 1
        ],
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
