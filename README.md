# pykle-serial

**pykle-serial** is a Python library for parsing the serialized format used on [keyboard-layout-editor.com (KLE)](http://www.keyboard-layout-editor.com/).

pykle-serial is a Python port of [kle-serial](https://github.com/ijprest/kle-serial), 
based on [commit #4080386 on Dec 31, 2019](https://github.com/ijprest/kle-serial/commit/4080386fcdcb66a391e1b4857532512f9ca4121e)
and includes [Fix issue with incorrect x and y for rotated key](https://github.com/ijprest/kle-serial/pull/1/commits/913a6f42f3ee03586d1cb0665f5d24ffe5bf5b68).

## Usage

```python
import pykle_serial as kle_serial

keyboard = kle_serial.deserialize([
    {'name': "Sample", 'author': "Your Name"},
    ["Q", "W", "E", "R", "T", "Y"]
])

# or

keyboard = kle_serial.parse('''[
    { name: "Sample", author: "Your Name" },
    ["Q", "W", "E", "R", "T", "Y"]
]''')
```

About the details of `keyboard`, see original [kle-serial](https://github.com/ijprest/kle-serial).

## Noticeable differences from original kle-serial

- `labels` / `textColor` / `textSize` of `Key` class always have 12 elements.

JavaScript's array esoterically supports out-of-index access. Python's list doesn't.

- (implicit) `textSize` is int.

JavaScript doesn't distinguish between float and int. Python does.

## Caveats

- KLE's "Raw data" text requires additional outer `[]` as JSON5.

- `labels` is HTML fragment.

## License

MIT license.
