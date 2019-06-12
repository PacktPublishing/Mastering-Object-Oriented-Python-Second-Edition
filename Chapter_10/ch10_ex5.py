#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 10. Example 5. EBCDIC encode/decode
"""

# Persistence Classes
# ========================================

# A detail class for micro-blog posts
import datetime
from typing import List, Optional, Dict, Any, Tuple, Callable, Union
from dataclasses import dataclass
from pathlib import Path

from Chapter_10.ch10_ex1 import Post, Blog, travel, rst_render
from Chapter_10.ch10_ex2 import FaceCard, AceCard, Card
from Chapter_10.ch10_ex4 import Player_Strategy, Martingale_Bet, gamestat_iter, GameStat
import io

# Legacy Files
# ===================

# We'll look at pure text and mixed text w/ packed decimal.

# Example 1 dumping all text
# ###########################

# Metadata for Gamestat objects.
# attribute name, start, size, and an output format specification.

from typing import NamedTuple, BinaryIO, TextIO, Iterable, Iterator, cast
from pathlib import Path

class FixedField(NamedTuple):
    name: str
    offset: int
    length: int
    format_spec: str

class Metadata(NamedTuple):
    fields: List[FixedField]
    reclen: int

metadata_txt = Metadata(
    fields=[
        FixedField("player", 0, 20, "{:<{size}s}"),
        FixedField("bet", 20, 20, "{:<{size}s}"),
        FixedField("rounds", 40, 5, "{:>{size}d}"),
        FixedField("final", 45, 8, "{:>{size}d}"),
    ],
    reclen=53,
)

# A function to transform a namedtuple into a fixed-layout record.
def gamestat_record(gamestat:GameStat, metadata: Metadata) -> str:
    record_fields = [
        format_spec.format(getattr(gamestat, name), size=size)
        for name, start, size, format_spec in metadata.fields
    ]
    record_text = "".join(record_fields)
    assert len(record_text) == metadata.reclen, f"Got {len(record_text)} Should Be {metadata.reclen}"
    return record_text


# An application of the game statistics definitions.
with (Path.cwd()/"data"/"ch10_blackjack.file").open("w", encoding="cp037", newline="") as target:
    for gamestat in gamestat_iter(Player_Strategy, Martingale_Bet):
        record = gamestat_record(gamestat, metadata_txt)
        target.write(record)

# Example 2 loading all text
# ##########################

# Loading data from the simulator. Part 1 -- Physical decomposition into rows.
def line_iter(aFile: TextIO, metadata: Union[Metadata, 'XMetadata']) -> Iterator[str]:
    recBytes = aFile.read(metadata.reclen)
    while recBytes:
        yield recBytes
        recBytes = aFile.read(metadata.reclen)


# Part 2 -- decomposition into named fields.
def record_iter(aFile: TextIO, metadata: Metadata) -> Iterator[Dict[str, str]]:
    for line in line_iter(aFile, metadata):
        record = {
            name: line[start:start + size].strip()
            for name, start, size, format_spec in metadata.fields
        }
        yield record


# Part 3 -- using the field to dictionary parser.
test_reader_1 = """
    >>> with (Path.cwd()/"data"/"ch10_blackjack.file").open("r", encoding="cp037", newline="") as source:
    ...     for record_in in record_iter(cast(TextIO, source), metadata_txt):
    ...         print(record_in)
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '100', 'final': '142'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '27', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '25', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '100', 'final': '157'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '100', 'final': '87'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '18', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '100', 'final': '161'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '10', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '22', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '53', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '37', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '27', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '100', 'final': '188'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '58', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '100', 'final': '103'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '28', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '60', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '100', 'final': '150'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '9', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '13', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '97', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '100', 'final': '93'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '72', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '12', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '36', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '35', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '78', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '68', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '39', 'final': '0'}
    {'player': 'Player_Strategy', 'bet': 'Martingale_Bet', 'rounds': '47', 'final': '0'}
"""

# Example 3 -- USAGE DISPLAY and USAGE COMP3
# ###########################################

# Using COMP-3 expands the problem into three kinds of data
#
# - Alpha and Alphanumeric encoded in EBCDIC or ASCII
#
# - Numeric, USAGE DISPLAY, as a string of digits encoded in EBCDIC or ASCII
#
# - Numeric, USAGE COMP-3, as string of bytes encoded as packed decimal.
#
# All of which require the decimal module's Decimal class definition.

from decimal import Decimal

# As a convenience, we map 'ebcdic' to 'cp037' by adding a new lookup function.
#
import codecs


def ebcdic_lookup(name, fallback=codecs.lookup):  # real signature unknown
    if name == "ebcdic":
        return codecs.lookup("cp037")
    return fallback(name)


codecs.register(ebcdic_lookup)

# Alphanumeric USAGE DISPLAY conversion.
# The COBOL program stored text.
def alpha_decode(data: bytes, metadata: 'XMetadata', field_metadata: 'XField') -> str:
    """Decode alpha or alphanumeric data.
    metadata has encoding.
    field_metadata is (currently) not used.

    Mock metadata objects
    >>> import types
    >>> meta = types.SimpleNamespace(reclen=6, encoding='ebcdic')
    >>> meta.decode = codecs.getdecoder(meta.encoding)
    >>> field_meta = types.SimpleNamespace()  # Used in other examples...

    >>> data = bytes([0xf9, 0xf8, 0xf7, 0xf6, 0xf5, 0x60])
    >>> alpha_decode(data, meta, field_meta)
    '98765-'

    """
    text, _ = metadata.decode(data)
    return text


# Numeric USAGE DISPLAY trailing sign conversion.
# The COBOL program stored text version of the number.
def display_decode(data: bytes, metadata: 'XMetadata', field_metadata: 'XField') -> Decimal:
    """Decode USAGE DISPLAY numeric data.
    metadata has encoding.
    field_metadata has attributes name, start, size, format, precision, usage.

    Mock metadata objects
    >>> import types
    >>> meta= types.SimpleNamespace(reclen=6, encoding='ebcdic')
    >>> meta.decode = codecs.getdecoder(meta.encoding)
    >>> field_meta = types.SimpleNamespace(precision=2)

    >>> data = bytes([0xf9, 0xf8, 0xf7, 0xf6, 0xf5, 0x60])
    >>> display_decode(data, meta, field_meta)
    Decimal('-987.65')

    """
    text, _ = metadata.decode(data)
    precision = field_metadata.precision or 0  # If None, default is 0.
    text, sign = text[:-1], text[-1]
    return Decimal(sign + text[:-precision] + "." + text[-precision:])


# Numeric USAGE COMP-3 conversion.
# The COBOL program encoded the number into packed decimal representation.
def comp3_decode(data: bytes, metadata: 'XMetadata', field_metadata: 'XField') -> Decimal:
    """Decode USAGE COMP-3 data.
    metadata has encoding, which is not used.
    field_metadata has attributes name, start, size, format, precision, usage.

    Note that the size is the overall resulting string of bytes.
    NOT the number of digits involved.

    Mock metadata objects
    >>> import types
    >>> meta = types.SimpleNamespace() # Not used
    >>> field_meta = types.SimpleNamespace(precision=2)

    >>> data = bytes((0x98, 0x76, 0x5d))
    >>> comp3_decode(data, meta, field_meta)
    Decimal('-987.65')

    """
    precision = field_metadata.precision or 0  # Default when precision is omitted
    digits = []
    for b in data[:-1]:
        hi, lo = divmod(b, 16)
        digits.append(str(hi))
        digits.append(str(lo))
    digit, sign_byte = divmod(data[-1], 16)
    digits.append(str(digit))
    text = "".join(digits)
    sign = "-" if sign_byte in (0x0b, 0x0d) else "+"
    return Decimal(sign + text[:-precision] + "." + text[-precision:])


# Encoder for simple alpha or alphanumeric.
def alpha_encode(data: Any, metadata: 'XMetadata', field_metadata: 'XField') -> bytes:
    """Encode alpha or alphanumeric data.
    metadata has encoding.
    field_metadata is not used.

    Mock metadata objects
    >>> import types
    >>> meta = types.SimpleNamespace(encoding='ebcdic')
    >>> meta.encode = codecs.getencoder(meta.encoding)
    >>> field_meta = types.SimpleNamespace(length=6)

    >>> data = '98765-'
    >>> actual = alpha_encode(data, meta, field_meta)
    >>> repr(actual)
    "b'\\\\xf9\\\\xf8\\\\xf7\\\\xf6\\\\xf5`'"
    >>> actual == bytes([0xf9, 0xf8, 0xf7, 0xf6, 0xf5, 0x60])
    True

    """
    bytes, _ = metadata.encode("{:<{size}s}".format(data, size=field_metadata.length))
    return bytes


# Encoder for numeric USAGE DISPLAY, trailing sign.
def display_encode(data: Decimal, metadata: 'XMetadata', field_metadata: 'XField') -> bytes:
    """Encode numeric USAGE DISPLAY trailing sign.
    metadata has encoding.
    field_metadata has attributes name, start, size, format, precision, usage.

    Mock metadata objects
    >>> import types, decimal
    >>> meta = types.SimpleNamespace(encoding='ebcdic')
    >>> meta.encode = codecs.getencoder(meta.encoding)
    >>> field_meta = types.SimpleNamespace(length=6, precision=2)

    >>> actual = display_encode(Decimal('-987.65'), meta, field_meta)
    >>> repr(actual)
    "b'\\\\xf9\\\\xf8\\\\xf7\\\\xf6\\\\xf5`'"
    >>> actual ==  bytes([0xf9, 0xf8, 0xf7, 0xf6, 0xf5, 0x60])
    True

    """
    precision = field_metadata.precision or 0
    text = "{0:0>{size}d}{1}".format(
        abs(int(data * Decimal(10) ** precision)),
        "-" if data < 0 else "+",
        size=field_metadata.length - 1,
    )
    bytes, _ = metadata.encode(text)
    return bytes


# Encoder for numeric USAGE COMP-3.
def comp3_encode(data: Decimal, metadata: 'XMetadata', field_metadata: 'XField') -> bytes:
    """Encode numeric USAGE COMP-3.
    metadata has encoding which is not used.
    field_metadata has attributes name, start, size, format, precision, usage.

    Note that the size is the overall resulting string of bytes.
    NOT the number of digits involved.
    This has 2 digits per byte + a digit and a sign.

    Mock metadata objects
    >>> import types
    >>> meta = types.SimpleNamespace(encoding='ebcdic')
    >>> field_meta = types.SimpleNamespace(length=3, precision=2)

    >>> actual = comp3_encode(Decimal('-987.65'), meta, field_meta)
    >>> repr(actual)
    "b'\\\\x98v]'"
    >>> actual == bytes((0x98, 0x76, 0x5d))
    True

    """
    precision = field_metadata.precision or 0
    value = abs(int(data * Decimal(10) ** precision))
    digits = [0x0d if data < 0 else 0x00]  # Trailing sign.
    nDigits = field_metadata.length * 2 - 1
    for i in range(nDigits):
        digits = [value % 10] + digits
        value //= 10
    b = bytes((hi * 16 + lo for hi, lo in list(zip(digits[::2], digits[1::2]))))
    return b


# Our expanded metadata to include more refined field-level definitions.
# First, we'll define some encode-decode pairs.
alphanumeric = (alpha_encode, alpha_decode)
usage_display = (display_encode, display_decode)
usage_comp3 = (comp3_encode, comp3_decode)

Encoder = Callable[[Any, Any, Any], bytes]
Decoder = Callable[[bytes, Any, Any], Any]
Usage = Tuple[Encoder, Decoder]

# Then we'll define a more sophisticated metadata that includes the
# precision and a reference to the relevant encode-decode pair.
#
# The overall metadata encoding name is transformed into an
# encode and decode function to save lookups on a field-by-field basis.
import collections

class XField(NamedTuple):
    name: str
    offset: int
    length: int
    precision: Optional[int]
    usage: Tuple[Callable, Callable]

class XMetadata(NamedTuple):
    fields: List[XField]
    reclen: int
    encoding: str

    @property
    def decode(self) -> Callable[[bytes], Tuple[str, int]]:
        return codecs.getdecoder(self.encoding)

    @property
    def encode(self) -> Callable[[str], Tuple[bytes, int]]:
        return codecs.getencoder(self.encoding)


metadata_comp3 = XMetadata(
    fields=[
        XField("player", 0, 20, None, alphanumeric),
        XField("bet", 20, 20, None, alphanumeric),
        XField("rounds", 40, 8, 2, usage_display),
        XField("final", 48, 8, 2, usage_comp3),
    ],
    reclen=56,
    encoding="ebcdic",  # for display fields and alphanumeric fields.
)

# A function to transform a namedtuple into a fixed-layout record.
def gamestat_record_comp3(gamestat: GameStat, metadata: XMetadata) -> bytes:
    record = [
        field.usage[0](getattr(gamestat, field.name), metadata, field)
        for field in metadata.fields
    ]
    text = b"".join(record)
    assert len(text) == metadata.reclen, "Got {0} != Should Be {1}".format(
        len(text), metadata.reclen
    )
    return text


# Example encoding app.
with (Path.cwd()/"data"/"ch10_blackjack_comp3.file").open("wb") as target:
    for gamestat in gamestat_iter(Player_Strategy, Martingale_Bet):
        data_bytes = gamestat_record_comp3(gamestat, metadata_comp3)
        target.write(data_bytes)

# Example decoding iterator using more sophisticated metadata.
def record2_iter(aFile: TextIO, metadata: XMetadata) -> Iterator[Dict[str, XField]]:
    for line in line_iter(aFile, metadata):
        field_data = (
            (field, line[field.offset:field.offset + field.length])
            for field in metadata.fields
        )
        record = dict(
            (field.name, field.usage[1](data, metadata, field))
            for field, data in field_data
        )
        yield record

test_reader_2 = """
    >>> with (Path.cwd()/"data"/"ch10_blackjack_comp3.file").open("rb") as source:
    ...     for record in record2_iter(source, metadata_comp3):
    ...        print(record)
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('100.00'), 'final': Decimal('142.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('27.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('25.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('100.00'), 'final': Decimal('157.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('100.00'), 'final': Decimal('87.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('18.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('100.00'), 'final': Decimal('161.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('10.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('22.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('53.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('37.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('27.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('100.00'), 'final': Decimal('188.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('58.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('100.00'), 'final': Decimal('103.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('28.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('60.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('100.00'), 'final': Decimal('150.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('9.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('13.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('97.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('100.00'), 'final': Decimal('93.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('72.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('12.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('36.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('35.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('78.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('68.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('39.00'), 'final': Decimal('0.00')}
    {'player': 'Player_Strategy     ', 'bet': 'Martingale_Bet      ', 'rounds': Decimal('47.00'), 'final': Decimal('0.00')}

"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
