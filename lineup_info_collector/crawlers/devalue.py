"""Minimal decoder for `devalue`-flattened JSON payloads.

As embedded by Nuxt's `__NUXT_DATA__` script tag. Only the subset needed to
read plain JSON-shaped data (objects, arrays, strings, numbers, booleans,
null) plus the handful of special type tags devalue uses for everything else
is implemented.

See https://github.com/Rich-Harris/devalue for the reference format.
"""

from collections.abc import Callable

JSONValue = None | bool | int | float | str | list["JSONValue"] | dict[str, "JSONValue"]

_UNDEFINED = -1
_HOLE = -2
_NAN = -3
_POSITIVE_INFINITY = -4
_NEGATIVE_INFINITY = -5
_NEGATIVE_ZERO = -6

_SENTINELS: dict[int, JSONValue] = {
    _UNDEFINED: None,
    _NAN: float("nan"),
    _POSITIVE_INFINITY: float("inf"),
    _NEGATIVE_INFINITY: float("-inf"),
    _NEGATIVE_ZERO: -0.0,
}


def _as_ref(value: JSONValue) -> int:
    """Narrow a devalue array/object entry to the integer index it must be.

    Every entry inside a devalue chunk is either one of the negative
    sentinel constants or an index into the flat array — never a bare
    literal — so a non-int here means the payload is malformed.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        message = f"Expected a devalue index reference, got {value!r}"
        raise TypeError(message)
    return value


def unflatten(parsed: list[JSONValue]) -> JSONValue:
    """Reconstruct the original value from a devalue-flattened array.

    Args:
        parsed: The flat array as decoded from the raw JSON text (e.g. the
            contents of a Nuxt `__NUXT_DATA__` script tag).

    Returns:
        The reconstructed value rooted at `parsed[0]`.
    """
    hydrated: dict[int, JSONValue] = {}

    def hydrate(index: int) -> JSONValue:
        if index in _SENTINELS:
            return _SENTINELS[index]
        if index in hydrated:
            return hydrated[index]

        value = parsed[index]

        if value is None or not isinstance(value, list | dict):
            hydrated[index] = value
        elif isinstance(value, dict):
            obj: dict[str, JSONValue] = {}
            hydrated[index] = obj
            for key, ref in value.items():
                obj[key] = hydrate(_as_ref(ref))
        elif value and isinstance(value[0], str):
            hydrated[index] = _hydrate_tagged(value, hydrate)
        else:
            array: list[JSONValue] = [None] * len(value)
            hydrated[index] = array
            for i, ref in enumerate(value):
                if ref == _HOLE:
                    continue
                array[i] = hydrate(_as_ref(ref))

        return hydrated[index]

    return hydrate(0)


def _hydrate_tagged(value: list[JSONValue], hydrate: Callable[[int], JSONValue]) -> JSONValue:
    """Decode one of devalue's tagged special-type chunks, e.g. `["Date", "..."]`."""
    tag = value[0]
    if tag == "Date":
        return value[1]
    if tag == "Set":
        return [hydrate(_as_ref(ref)) for ref in value[1:]]
    if tag == "RegExp":
        return value[1]
    if tag == "BigInt":
        text = value[1]
        return int(text) if isinstance(text, str) else None
    if tag in ("Map", "null"):
        pairs = ((hydrate(_as_ref(value[i])), hydrate(_as_ref(value[i + 1]))) for i in range(1, len(value), 2))
        return {str(k): v for k, v in pairs}
    # Unknown/custom reducer (e.g. Vue's "Reactive", "ShallowReactive", "Ref"):
    # devalue's own unflatten unwraps these to their single payload reference.
    return hydrate(_as_ref(value[1]))
