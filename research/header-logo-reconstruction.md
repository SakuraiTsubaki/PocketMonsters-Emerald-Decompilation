# Emerald GBA header Nintendo logo reconstruction

`bpe-j-rev0-retail` is the Japanese origin reference. Every one of the 6 cataloged builds (Japanese, English, German, French, Italian, Spanish) has the same 156-byte payload at header offset `0x04`. BIOS Huffman and cumulative-delta decoding independently reproduces the shared 104x16 logical logo and deterministic 416x64 PNG. Per-build reports retain ROM identity, source, decoded 1bpp, and PNG hashes without publishing ROM bytes.
