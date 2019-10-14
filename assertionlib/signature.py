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
    _estimate_signature
    _signature_to_str

API
---
.. autofunction:: generate_signature
.. autodata:: BACK_SIGNATURE
.. autofunction:: _estimate_signature
.. autofunction:: _signature_to_str

"""

from typing import Callable, Optional, Type
from inspect import Parameter, Signature, signature, _empty

PO = Parameter.POSITIONAL_ONLY
POK = Parameter.POSITIONAL_OR_KEYWORD
VP = Parameter.VAR_POSITIONAL
KO = Parameter.KEYWORD_ONLY
VK = Parameter.VAR_KEYWORD

# Annotation for (optional) exception types
ExType = Optional[Type[Exception]]


def _get_backup_signature() -> Signature:
    """Create a generic :class:`Signature<inspect.Signature>` instance.

    Returns
    -------
    :class:`Signature<inspect.Signature>`
        A signature with the following parameters:

        * ``self``: Positional or keyword
        * ``*args``: Variational position
        * ``invert``: Keyword only (default value: ``False``)
        * ``exception``: Keyword only (default value: ``None``)
        * ``**kwargs``: Variational keyword

    See also
    --------
    :attr:`Parameter.kind<inspect.Parameter.kind>`
        Describes how argument values are bound to the parameter.

    :data:`.BACK_SIGNATURE`
        A generic backup signature generated by this function.

    """
    parameters = [
        Parameter(name='self', kind=POK),  # Avoid using positional-only
        Parameter(name='args', kind=VP),
        Parameter(name='invert', kind=KO, default=False, annotation=bool),
        Parameter(name='exception', kind=KO, default=None, annotation=ExType),
        Parameter(name='kwargs', kind=VK)
    ]
    return Signature(parameters=parameters, return_annotation=None)


#: A generic backup signature generated by :func:`._estimate_signature`.
BACK_SIGNATURE: Signature = _get_backup_signature()


def generate_signature(func: Callable) -> Signature:
    """Generate a new function signatures with the ``self``, ``invert`` and ``exception`` parameters.  # noqa

    Examples
    --------
    .. code:: python

        >>> import inspect

        # The builtin enumerate function
        >>> func = enumerate
        >>> Signature = inspect.Signature

        # Print the signature of enumerate
        >>> signature1: Signature = inspect.signature(func)
        >>> print(signature1)
        (iterable, start=0)

        # Print the newly create signature
        >>> signature2: Signature = generate_signatures(func)
        >>> print(signature2)
        (self, /, iterable, start=0, invert_: bool = False) -> None

    Parameters
    ----------
    func : :data:`Callable<typing.Callable>`
        A callable object.

    Returns
    -------
    :class:`Signature<inspect.Signature>`
        The signature of **func** with the ``self`` and ``invert`` parameters.
        Return :data:`.BACK_SIGNATURE` if funcs' signature cannot be read.

    """
    try:
        sgn = signature(func)
    except ValueError:  # Not all callables have a signature that can be read.
        return BACK_SIGNATURE

    has_VP = False  # Does the signature contain an *args-like argument?
    has_VK = False  # Does the signature contain a **kwargs-like argument?

    parameters = [Parameter(name='self', kind=POK)]
    for name, prm in sgn.parameters.items():
        if prm.kind is VP:
            has_VP = True
        elif not has_VP and prm.default is not _empty:
            parameters.append(Parameter(name='args', kind=VP))
            has_VP = True
        elif prm.kind is VK:  # Add the `invert` argument before a **kwargs-like argument
            parameters.append(Parameter(name='invert', kind=KO, default=False, annotation=bool))
            parameters.append(Parameter(name='exception', kind=KO, default=None, annotation=ExType))  # noqa
            has_VK = True

        if has_VP:  # Convert positional-only to positional or keyword
            prm = Parameter(name=prm.name, kind=KO, default=prm.default, annotation=prm.annotation)
        elif prm.kind is PO:  # Convert positional-only to positional or keyword
            prm = Parameter(name=prm.name, kind=POK, default=prm.default, annotation=prm.annotation)
        parameters.append(prm)

    # The signature does not contain a **kwargs-like argument; the invert parameter has not been set
    if not has_VP:
        parameters.append(Parameter(name='args', kind=VP))
    if not has_VK:
        parameters.append(Parameter(name='invert', kind=KO, default=False, annotation=bool))
        parameters.append(Parameter(name='exception', kind=KO, default=None, annotation=ExType))
        parameters.append(Parameter(name='kwargs', kind=VK))

    # print(repr([p.kind for p in parameters]))
    return Signature(parameters=parameters, return_annotation=None)


#: A dictionary for creating format string for specific parameter kinds
_KIND_TO_STR: dict = {
    PO: '{}',
    POK: '{}',
    VP: '*{}',
    VK: '**{}',
}


def _signature_to_str(sgn: Signature, func_name: str) -> str:
    """Create a string from a signature.

    * The ``self`` parameter will be substituted for **func_name**,
      *i.e.* the name of the to-be asserted function.
    * Annotations will be removed
    * keyword arguments will have their default values replaced with their respective keys.

    """
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
