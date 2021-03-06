import importlib

from werkzeug.urls import url_parse


def is_external(parsed_url, prefix):
    """Return true if the given URL is within a web app at `prefix`

    Both arguments should be results of url_parse (or parse_absolute_url)
    """
    return (
        parsed_url.scheme != prefix.scheme
        or parsed_url.ascii_host != prefix.ascii_host
        or parsed_url.port != prefix.port
        or not parsed_url.path.startswith(prefix.path)
    )


def parse_absolute_url(url):
    """Parse absolute URL

    Returns the same result as werkzeug.urls.url_parse, but works on
    absolute HTTP and HTTPS URLs only.
    The result port is always an integer.
    """
    parsed = url_parse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Need an absolute URL")

    if parsed.scheme not in ('http', 'https'):
        raise ValueError("URL scheme must be http or https")

    if parsed.port == None:
        if parsed.scheme == 'http':
            parsed = parsed.replace(netloc=parsed.host + ':80')
        elif parsed.scheme == 'https':
            parsed = parsed.replace(netloc=parsed.host + ':443')
        else:
            raise ValueError("URL scheme must be http or https")

    return parsed


def import_variable_from_module(name, *, default_variable_name=None):
    """Import a variable from a named module

    Given a name like "package.module:namespace.variable":
    - import module "package.module"
    - get the attribute "namespace" from the module
    - return the attribute "variable" from the "namespace" object
    """
    module_name, sep, variable_name = name.partition(':')
    if not sep:
        variable_name = default_variable_name
    if not variable_name:
        raise ValueError(f'Missing variable name: {name!r}')

    module = importlib.import_module(module_name)

    result = module
    for attribute_name in variable_name.split('.'):
        result = getattr(result, attribute_name)

    return result
