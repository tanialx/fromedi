# fromedi (From EDI)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache&#8208;2.0-green.svg?style=flat-square)](LICENSE.md)
![Stability-wip](https://img.shields.io/badge/Stability-WIP-yellow.svg?style=flat-square)

Just jotted down some idea for a EDI-to-human-language translator.

### Goal

Produce information of EDI in understandable json format; 
for example, from
```
BIG*20101204*217224*20101204*P792940
```
to
```json
{
  "Invoice date": "12-04-2010",
  "Invoice #": "217224",
  "Order date": "12-04-2010",
  "Order #": "P792940"
}
```

### Project layout

#### fromedi
- `defs.py` defines EDI structure and necessary information for parsing
- `parser.py` defines parsing logic
- `literal/*.json` mapping EDI keycode to human-language text
- `struct/*.json` structure of EDI segments/sub-segments (similar to `rule` object in `defs.py`). Path: `struct/<segment_name>/<mapping_key>.json`

#### tests

- `data/*.edi` EDI files used for testing
- `test_parser.py` test cases

### Refs
- [What is EDI?](https://www.ibm.com/topics/edi-electronic-data-interchange)
