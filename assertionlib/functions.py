"""
assertionlib.functions
======================

Various functions related to the :class:`.AssertionManager` class.

Index
-----
.. currentmodule:: assertionlib.functions
.. autosummary::
    get_sphinx_domain
    create_assertion_doc
    bind_callable
    allclose
    len_eq
    str_eq

API
---
.. autofunction:: get_sphinx_domain
.. autofunction:: create_assertion_doc
.. autofunction:: bind_callable
.. autofunction:: allclose
.. autofunction:: len_eq
.. autofunction:: str_eq

"""

import os
import types
import inspect
import textwrap
from typing import Callable, Any, Optional, Union, Sized, Dict, Mapping, Tuple, Type

from .signature import generate_signature, _signature_to_str


def bind_callable(class_type: Union[type, Any], func: Callable,
                  name: Optional[str] = None) -> None:
    """Take a callable and use it to create a new assertion method for **class_type**.

    The created callable will have the same signature as **func** except for one additional
    keyword argument by the name of ``func`` (default value: ``False``).
    Setting this keyword argument to ``True`` will invert the output of the assertion,
    *i.e.* it changes ``assert func(...)`` into ``assert not func(...)``.

    Examples
    --------
    Supplying the builtin :func:`len` function will create (and bind) a callable which
    performs the :code:`assert len(obj)` assertion.

    Parameters
    ----------
    class_type : :class:`type` or :data:`Any<typing.Any>`
        A class (*i.e.* a :class:`type` instance) or class instance.

    func : :data:`Callable<typing.Callable>`
        A callable object whose output will be asserted by the created method.

    name : :class:`str`, optional
        The name of the name of the new method.
        If ``None``, use the name of **func**.


    :rtype: :data:`None`

    """
    name = name if name is not None else func.__name__

    # Create the new function
    function, signature_str = _create_assertion_func(func)

    # Update the docstring and sanitize the signature
    signature_str = signature_str.replace(f'({func.__name__}, ', '(')
    signature_str = signature_str.replace(', *args', '').replace(', **kwargs', '')
    signature_str = signature_str.replace(', invert=invert, exception=exception', '')
    function.__doc__ = create_assertion_doc(func, signature_str)

    # Update annotations
    try:
        function.__annotations__ = func.__annotations__.copy()
    except AttributeError:
        function.__annotations__ = {}
    finally:
        function.__annotations__['return'] = None
        function.__annotations__['invert'] = bool
        function.__annotations__['exception'] = Optional[Type[Exception]]

    # Set the new method
    if isinstance(class_type, type):  # A class
        setattr(class_type, name, function)
    else:  # A class instance
        method = types.MethodType(function, class_type)
        setattr(class_type, name, method)


def _create_assertion_func(func: Callable) -> Tuple[types.FunctionType, str]:
    """Generate the assertion function for :func:`bind_callable`.

    Parameters
    ----------
    func : :data:`Callable<typing.Callable>`
        A callable object forming the basis of the to-be created assertion function.

    """
    # sgn1 is a Signature instance with the signature for the to-be returned FunctionType
    # sgn2 is a string with all arguments for self.assert_()
    sgn = generate_signature(func)
    sgn_str = _signature_to_str(sgn, 'func')

    # Create the code object for the to-be returned function
    code_compile = compile(
        f'def {func.__name__}{sgn}: self.assert_{sgn_str}',
        "<string>", "exec"
    )
    for code in code_compile.co_consts:
        if isinstance(code, types.CodeType):
            break

    # Extract the default arguments for positional or keyword parameters
    defaults = code_compile.co_consts[-1]
    if isinstance(defaults, str):  # no default arguments
        defaults = None
    func_new = types.FunctionType(code, {'func': func}, func.__name__, defaults)

    # Set default values for keyword-only parameters
    KO = inspect.Parameter.KEYWORD_ONLY
    kwdefault = {k: v.default for k, v in sgn.parameters.items() if v.kind is KO}
    if kwdefault:
        func_new.__kwdefaults__ = kwdefault

    return func_new, sgn_str


#: A string with the (to-be formatted) docstring returned by :func:`wrap_docstring`
BASE_DOCSTRING: str = """Perform the following assertion: :code:`assert {name}{signature}`.

Parameters
----------
invert : :class:`bool`
    Invert the output of the assertion: :code:`assert not {name}{signature}`.

exception : :class:`type` [:exc:`Exception`], optional
    Assert that **exception** is raised during/before the assertion operation.

See also
--------
{domain}:
{summary}

"""


def create_assertion_doc(func: Callable, signature: Optional[str] = None) -> str:
    """Create a new NumPy style assertion docstring from the docstring of **func**.

    The summary of **funcs'** docstring, if available, is added to the ``"See also"`` section,
    in addition with an intersphinx-compatible link to **func**.

    Examples
    --------
    .. code:: python

        >>> docstring: str = wrap_docstring(isinstance)
        >>> print(docstring)
        Perform the following assertion: :code:`assert isinstance(obj, class_or_tuple)`.

        Parameters
        ----------
        invert : :class:`bool`
            Invert the output of the assertion: :code:`assert not isinstance(obj, class_or_tuple)`.

        exception : :class:`type` [:exc:`Exception`], optional
            Assert that **exception** is raised during/before the assertion operation.

        See also
        --------
        :func:`isinstance`:
            Return whether an object is an instance of a class or of a subclass thereof.

    Parameters
    ----------
    func : :data:`Callable<typing.Callable>`
        A callable whose output is to-be asserted.

    signature : :class:`str`, optional
        Provide a custom signature for **func**.
        If ``None``, default to ``(*args, **kwargs)``.

    Returns
    -------
    :class:`str`
        A new docstring constructed from **funcs'** docstring.

    """
    domain = get_sphinx_domain(func)
    sgn = signature if signature is not None else '(*args, **kwargs)'

    # Extract the first line from the func docstring
    try:
        func_summary = textwrap.indent(func.__doc__, 4 * ' ')
    except AttributeError:
        func_summary = '    No description.'

    # Return a new docstring
    try:
        name = func.__qualname__
    except AttributeError:
        name = func.__name__
    return BASE_DOCSTRING.format(name=name, signature=sgn, domain=domain, summary=func_summary)


#: A dictionary which translates certain __module__ values to actual valid modules
MODULE_DICT: Dict[str, str] = {
    'builtins': '',
    'genericpath': 'os.path.',
    'posixpath': 'os.path.',
    '_operator': 'operator.'
}


def _is_builtin_func(func: Callable) -> bool:
    """Check if **func** is a builtin function."""
    try:
        return inspect.isbuiltin(func) and '.' not in func.__qualname__
    except AttributeError:
        return False


def get_sphinx_domain(func: Callable, module_mapping: Mapping[str, str] = MODULE_DICT) -> str:
    """Create a Sphinx domain for **func**.

    Examples
    --------
    .. code:: python

        >>> from collections import OrderedDict

        >>> value1: str = get_sphinx_domain(int)
        >>> print(value1)
        :class:`int<int>`

        >>> value2: str = get_sphinx_domain(list.count)
        >>> print(value2)
        :meth:`list.count<list.count>`

        >>> value3: str = get_sphinx_domain(OrderedDict)
        >>> print(value3)
        :class:`OrderedDict<collections.OrderedDict>`

        >>> value4: str = get_sphinx_domain(OrderedDict.keys)
        >>> print(value4)
        :meth:`OrderedDict.keys<collections.OrderedDict.keys>`

    Parameters
    ----------
    func : :data:`Callable<typing.Callable>`
        A class or (builtin) method or function.

    module_mapping : :class:`dict` [:class:`str`, :class:`str`]
        A dictionary for mapping :attr:`__module__` values to actual module names.
        Useful for whenever there is a discrepancy between the two,
        *e.g.* the `genericpath` module of :func:`os.path.join`.

    Returns
    -------
    :class:`str`
        A string with a valid Sphinx refering to **func**.

    Raises
    ------
    TypeError
        Raised if **func** is neither a class or a (builtin) function or method.

    """
    name = func.__qualname__ if hasattr(func, '__qualname__') else func.__name__

    try:
        _module = func.__module__
    except AttributeError:  # Unbound methods don't have the `__module__` attribute
        _module = func.__objclass__.__module__

    try:
        module = MODULE_DICT[_module]
    except KeyError:
        module = _module + '.' if _module is not None else ''

    if inspect.isbuiltin(func) or inspect.isfunction(func) or _is_builtin_func(func):
        return f':func:`{name}<{module}{name}>`'
    elif inspect.ismethod(func) or inspect.ismethoddescriptor(func) or inspect.isbuiltin(func):
        return f':meth:`{name}<{module}{name}>`'
    elif inspect.isclass(func):
        return f':class:`{name}<{module}{name}>`'
    raise TypeError(f"{repr(name)} is neither a (builtin) function, method nor class")


#: A dictionary mapping to-be replaced substring to their replacements
README_MAPPING: Dict[str, str] = {'``': '|', '()': ''}


def load_readme(readme: str = 'README.rst', replace: Mapping[str, str] = README_MAPPING,
                **kwargs: Any) -> str:
    r"""Load and return the content of a readme file located in the same directory as this file.

    Equivalent to importing the content of ``../README.rst``.

    Parameters
    ----------
    readme : :class:`str`
        The name of the readme file.

    replace : :class:`dict` [:class:`str`, :class:`str`]
        A mapping of to-be replaced substrings contained within the readme file.

    \**kwargs : :data:`Any<typing.Any>`
        Optional keyword arguments for the :meth:`read<io.TextIOBase.read>` method.

    Returns
    -------
    :class:`str`
        The content of ``../README.rst``.

    """
    readme_abs: str = os.path.join(os.path.dirname(__file__), readme)
    with open(readme_abs, 'r') as f:
        ret = f.read(**kwargs)
    for old, new in replace.items():
        ret = ret.replace(old, new)
    return ret


def len_eq(a: Sized, b: int) -> bool:
    """Check if the length of **a** is equivalent to **b**."""
    return len(a) == b


def allclose(a: float, b: float, rtol: float = 1e-07) -> bool:
    """Check if the absolute differnce between **a** and **b** is smaller than **rtol**."""
    delta = abs(a - b)
    return delta < rtol


def str_eq(a: Any, b: str, use_repr: bool = True) -> bool:
    """Check if the string-representation of **a** is equivalent to **b**."""
    if use_repr:
        return repr(a) == b
    return str(a) == b
