from importlib import import_module
from typing import Any


def load_class(cls_with_ns: str) -> (Any | None):
    groups = cls_with_ns.split('.')
    ns = ".".join(groups[:-1])
    cls_name = groups[-1]

    try:
        mod = import_module(ns)
        cls = getattr(mod, cls_name)
        return cls
    except:
        return None
