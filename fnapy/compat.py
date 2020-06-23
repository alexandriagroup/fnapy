# -*- coding: utf-8 -*-
import sys

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = _ver[0] == 2

#: Python 3.x?
is_py3 = _ver[0] == 3

#: Python 3.3.x
is_py33 = is_py3 and _ver[1] == 3

#: Python 3.4.x
is_py34 = is_py3 and _ver[1] == 4

#: Python 2.7.x
is_py27 = is_py2 and _ver[1] == 7


try:  # pragma: no cover
    import __pypy__

    is_pypy = True
except:  # pragma: no cover
    __pypy__ = None
    is_pypy = False


if is_py3:
    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    integer_types = (int,)
    numeric_types = integer_types + (float,)

    def iterkeys(d):
        return iter(d.keys())

    def itervalues(d):
        return iter(d.values())

    def iteritems(d):
        return iter(d.items())

    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value

    def is_bytes(x):
        return isinstance(x, (bytes, memoryview, bytearray))

    from collections.abc import Callable

    def callable(obj):
        return isinstance(obj, Callable)


else:
    builtin_str = str
    bytes = str
    str = unicode
    basestring = basestring
    integer_types = (int, long)
    numeric_types = integer_types + (float,)

    def iterkeys(d):
        return d.iterkeys()

    def itervalues(d):
        return d.itervalues()

    def iteritems(d):
        return d.iteritems()

    exec("def reraise(tp, value, tb=None):\n raise tp, value, tb")

    def is_bytes(x):
        return isinstance(x, (buffer, bytearray))

    callable = callable


def with_metaclass(meta, base=object):
    return meta("NewBase", (base,), {})


def to_unicode(obj, encoding="utf-8"):
    """
    Convert ``obj`` to unicode"""
    # unicode support
    if isinstance(obj, str):
        return obj

    # bytes support
    if is_bytes(obj):
        if hasattr(obj, "tobytes"):
            return str(obj.tobytes(), encoding)
        return str(obj, encoding)

    # string support
    if isinstance(obj, basestring):
        if hasattr(obj, "decode"):
            # ignoring utf8 errors, as fnac send us malformed
            # utf8 xml sometimes ...
            return obj.decode(encoding, errors="ignore")
        else:
            return str(obj, encoding)

    return str(obj)
