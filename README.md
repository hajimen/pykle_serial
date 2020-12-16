# pykle_serial

pykle_serial is a Python library for parsing the serialized format used on [keyboard-layout-editor.com (KLE)](http://www.keyboard-layout-editor.com/).
pykle_serial is a Python port of [kle-serial](https://github.com/ijprest/kle-serial), 
based on [commit #4080386 on Dec 31, 2019](https://github.com/ijprest/kle-serial/commit/4080386fcdcb66a391e1b4857532512f9ca4121e).

## Usage

```
from pykle_serial import serial

keyboard = serial.deserialize([
    {'name': "Sample", 'author': "Your Name"},
    ["Q", "W", "E", "R", "T", "Y"]
])

# or

keyboard = serial.parse('''[
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

- KLE's "Raw data" text requies additional outer `[]` as JSON5.

- `labels` is HTML fragment.
