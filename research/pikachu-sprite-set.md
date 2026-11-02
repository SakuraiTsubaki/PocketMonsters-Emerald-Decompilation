# Emerald Pikachu sprite reconstruction

`bpe-j-rev0-retail` is the Japanese origin reference. All 6 cataloged builds (Japanese, English, German, French, Italian, Spanish) independently locate the species front, back, and normal-palette tables by their structural deltas. Each GBA LZ77 stream is decoded, rendered to a 128x128 PNG with the verified BGR555 palette, and recorded with compressed, decoded, palette, and output hashes. No ROM bytes are published.
