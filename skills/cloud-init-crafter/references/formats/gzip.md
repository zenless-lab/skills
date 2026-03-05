# Gzip Compressed Content

**Format:** Binary `.gz` file

Content found to be gzip compressed will be automatically uncompressed by cloud-init. The uncompressed data is then processed as if it were not compressed.

## Common Use Cases

- Bypassing user-data size limitations imposed by specific cloud platforms.

## Important Notes

- **Warning:** Some cloud platforms are known to corrupt binary content during metadata injection, which may prevent the use of this format.
