# fromedi (From EDI)

Just jotted down some idea for a EDI-to-human-language translator.

#### Goal

Produce information of EDI in understandable json format
Example, from
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

#### Project layout

- `defs.py` defines EDI structure and necessary information for parsing

- `parser.py` defines parsing logic

#### Refs
- [What is EDI?](https://www.ibm.com/topics/edi-electronic-data-interchange)
