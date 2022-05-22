from ideas import import_hook
from reconstructor import compile_kb


def transform_kb(source: str, **kwargs):
    if "# $kbmodule" in source:
        source = source.replace("# $kbmodule", "from kbcore import rule")
        output = compile_kb(source)
        return output
    return source


def add_hook():
    return import_hook.create_hook(transform_source=transform_kb)
