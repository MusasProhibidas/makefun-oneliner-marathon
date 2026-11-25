"""make.fun entry: One-Liner Marathon.

Reads the one-line joke from line.txt (next to this file), validates it
(single line, at most 280 characters) and writes it to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

No network access. Deterministic: every run writes the same bytes.
After writing, the output is verified byte-for-byte against the source
(SHA-256) so a partial or corrupted write fails loudly.
"""

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "line.txt"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT = OUT_DIR / "entry.txt"
MAX_CHARS = 280


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    line = SRC.read_text(encoding="utf-8").strip("\n")
    if "\n" in line or "\r" in line:
        raise SystemExit("line.txt must contain exactly one line")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"line is {len(line)} characters, over the 280-character cap"
        )
    if not line:
        raise SystemExit("line.txt is empty")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(line + "\n", encoding="utf-8")
    if _sha256(SRC) != _sha256(OUT):
        raise SystemExit("entry.txt mismatch: output bytes differ from source")
    print(line)
    print(f"sha256: {_sha256(OUT)}")
    print(f"characters: {len(line)}")


if __name__ == "__main__":
    main()
