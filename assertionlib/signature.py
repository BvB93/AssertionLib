"""
assertionlib.signature
======================

Various functions for manipulating function signatures.

Index
-----
.. currentmodule:: assertionlib.signature
.. autosummary::
    generate_signature
    BACK_SIGNATURE
    _get_backup_signature
    _signature_to_str

API
---
.. autofunction:: generate_signature
.. autodata:: BACK_SIGNATURE
.. autofunction:: _get_backup_signature
.. autofunction:: _signature_to_str

"""

import sys
from typing import Callable, Optional, Type, Dict, Collection, Tuple, Any, List, Union
from inspect import Parameter, Signature, signature, _ParameterKind
from inspect import _empty  # type: ignore
from itertools import chain
import warnings

from .ndrepr import aNDRepr

if sys.version_info < (3, 7):
    from collections import OrderedDict
else:  # Dictionaries are ordered starting from python 3.7
    from builtins import dict as OrderedDict  # type: ignore # noqa

PO: _ParameterKind = Parameter.POSITIONAL_ONLY
POK: _ParameterKind = Parameter.POSITIONAL_OR_KEYWORD
VP: _ParameterKind = Parameter.VAR_POSITIONAL
KO: _ParameterKind = Parameter.KEYWORD_ONLY
VK: _ParameterKind = Parameter.VAR_KEYWORD

#: Annotation for (optional) exception types
ExType = Optional[Type[Exception]]


def _get_backup_signature() -> Signature:
    """Create a generic backup :class:`~inspect.Signature` instance.

    Used in :func:`generate_signature` incase a callables' signature cannot be read.

    Returns
    -------
    :class:`~inspect.Signature`
        ``<Signature (self, *args, invert_: bool = False, exception_: Union[Type[Exception], NoneType] = None, **kwargs) -> None>``

    See Also
    --------
    :attr:`Parameter.kind<inspect.Parameter.kind>`
        Describes how argument values are bound to the parameter.

    :data:`.BACK_SIGNATURE`
        A generic backup signature generated by this function.

    """  # noqa
    parameters = [
        Parameter(name='self', kind=POK),  # Avoid using positional-only
        Parameter(name='args', kind=VP),
        Parameter(name='invert', kind=KO, default=False, annotation=bool),
        Parameter(name='exception', kind=KO, default=None, annotation=ExType),  # type: ignore
        Parameter(name='post_process', kind=KO, default=None, annotation=Optional[Callable[[Any], Any]]),  # noqa: E105, E501
        Parameter(name='message', kind=KO, default=None, annotation=Optional[str]),
        Parameter(name='kwargs', kind=VK)
    ]
    return Signature(parameters=parameters, return_annotation=None)


#: A generic backup :class:`~inspect.Signature` generated
#: by :func:`._get_backup_signature`.
BACK_SIGNATURE: Signature = _get_backup_signature()


def generate_signature(func: Callable) -> Signature:
    """Generate a new function signatures with the ``self``, ``invert`` and ``exception`` parameters.

    Default to :data:`BACK_SIGNATURE` if a functions' signature cannot be read.

    Examples
    --------
    .. code:: python

        >>> import inspect

        >>> func = enumerate  # The builtin enumerate function
        >>> Signature = inspect.Signature

        # Print the signature of enumerate
        >>> sgn1: Signature = inspect.signature(func)
        >>> print(sgn1)
        (iterable, start=0)

        # Print the newly create signature
        >>> sgn2: Signature = generate_signatures(func)
        >>> print(sgn2)
        (self, iterable, *args, start=0, invert_: bool = False, exception_: Union[Type[Exception], NoneType] = None, **kwargs) -> None

    Parameters
    ----------
    func : :class:`~collections.abc.Callable`
        A callable object.

    Returns
    -------
    :class:`~inspect.Signature`
        The signature of **func** with the ``self`` and ``invert`` parameters.
        Return :data:`BACK_SIGNATURE` if funcs' signature cannot be read.

    """  # noqa
    try:
        sgn = signature(func)
    except ValueError:  # Not all callables have a signature which can be read.
        return BACK_SIGNATURE

    prm_dict: Dict[_ParameterKind, List[Parameter]] = OrderedDict({
        POK: [Parameter(name='self', kind=POK)], VP: [], KO: [], VK: []
    })

    # Fill the parameter dict
    for prm in sgn.parameters.values():
        if prm.name == 'self':
            name, _ = _get_cls_annotation(func)
            prm = Parameter(name=name, kind=POK)
        elif prm.kind is PO:  # Positional-only to positional or keyword
            prm = prm.replace(kind=POK)
        elif prm.kind is POK and prm.default is not _empty:  # keyword or positional to keyword only
            prm = prm.replace(kind=KO)
        prm_dict[prm.kind].append(prm)

    # Double check if the invert and exception parameters are already defined by **func**
    invert_name = _sanitize_name('invert', func, prm_dict[KO])
    exception_name = _sanitize_name('exception', func, prm_dict[KO])
    post_process_name = _sanitize_name('post_process', func, prm_dict[KO])
    message = _sanitize_name('message', func, prm_dict[KO])

    # Ensure the parameter dict contains the following 4 parameters
    prm_dict[KO].append(Parameter(name=invert_name, kind=KO, default=False, annotation=bool))
    prm_dict[KO].append(Parameter(name=exception_name, kind=KO, default=None, annotation=ExType))  # type: ignore  # noqa
    prm_dict[KO].append(Parameter(name=post_process_name, kind=KO,
                                  default=None, annotation=Optional[Callable[[Any], Any]]))
    prm_dict[KO].append(Parameter(name=message, kind=KO, default=None, annotation=Optional[str]))

    if not prm_dict[VP]:
        prm_dict[VP].append(Parameter(name='args', kind=VP))
    if not prm_dict[VK]:
        prm_dict[VK].append(Parameter(name='kwargs', kind=VK))

    # Construct and return a new signature
    parameters = list(chain.from_iterable(prm_dict.values()))
    return Signature(parameters=parameters, return_annotation=None)


def _get_cls_annotation(func: Callable) -> Tuple[str, Union[str, type]]:
    """Return an annotation for ``self`` or ``cls``."""
    if hasattr(func, '__self__'):
        cls: Union[str, type] = func.__self__.__class__  # type: ignore
    elif hasattr(func, '__objclass__'):
        cls = func.__objclass__  # type: ignore
    elif hasattr(func, '__qualname__') and '.' in func.__qualname__:
        cls_name: str = func.__qualname__.split('.')[0]
        cls = cls_name
    else:
        cls = func.__class__

    if not isinstance(cls, str):
        cls_name = cls.__name__
    return cls_name.lower(), cls


def _sanitize_name(name: str, func: Callable, prm_list: Collection[Parameter]) -> str:
    """Return **name** if it is not present in **container**, otherwise append it with ``'_'`` and try again."""  # noqa
    if name in {prm.name for prm in prm_list}:
        warnings.warn(f"The '{name}' parameter is already defined in {aNDRepr.repr(func)}; "
                      f"renaming new parameter to '{name}_'", RuntimeWarning, stacklevel=2)
        return _sanitize_name(name + '_', func, prm_list)
    else:
        return name


#: A dictionary for creating format string for specific parameter kinds.
#: Used by :func:`_signature_to_str`.
_KIND_TO_STR: Dict[_ParameterKind, str] = {
    PO: '{}',
    POK: '{}',
    VP: '*{}',
    VK: '**{}',
}


def _signature_to_str(sgn: Signature, func_name: Optional[str] = None) -> str:
    """Create a string from a signature.

    * The ``self`` parameter will be substituted for **func_name**,
      *i.e.* the name of the to-be asserted function.
    * Annotations will be removed
    * keyword arguments will have their default values replaced with their respective keys.

    Examples
    --------
    .. code:: python

        >>> import inspect

        >>> Signature = inspect.Signature

        >>> def func(self, a: int, b: float, *args, c=1, d=2, **kwargs) -> None:
        ...     pass

        >>> sgn: Signature = inspect.signature(func)
        >>> print(sgn)
        (self, a: int, b: float, *args, c=1, d=2, **kwargs) -> None

        >>> sgn_str: str = _signature_to_str(sgn, func_name='fancy_func_name')
        >>> print(sgn_str)
        (fancy_func_name, a, b, *args, c=c, d=d, **kwargs)

    Parameters
    ----------
    sgn : :class:`~inspect.Signature`
        A Signature object.

    func_name : :class:`str`, optional
        If not ``None``, replace all references to ``self`` with **func_name**.

    Returns
    -------
    :class:`str`
        A stringified version of **sgn**.

    """
    func_name = 'self' if func_name is None else func_name
    parameters = []
    for name, prm in sgn.parameters.items():
        if name == 'self':
            value = func_name
        elif prm.default is not _empty:
            value = f'{name}={name}'
        else:
            value = _KIND_TO_STR[prm.kind].format(name)
        parameters.append(value)

    return '(' + ', '.join(i for i in parameters) + ')'
