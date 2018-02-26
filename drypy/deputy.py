"""
.. module:: deputy
   :platform: Unix
   :synopsis: Sheriff-Deputy pattern decorator

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

from . import get_status
from .sham import sham

class sheriff:
    """Decorator which makes drypy to run *func.deputy*
    instead of *func*.

    Example:
        >>> @sheriff
        ... def my_func():
        ...    print("I'm the Sheriff!")
        ...
        >>> @my_func.deputy
        ... def my_other_func():
        ...    print("I'm the Deputy!")
        ...
        >>> my_func()
        I'm the Deputy!


    .. note::
       Providing a deputy is optional: when not provided drypy
       will automatically fallback on :class:`sham` behaviour.

    """
    def __init__(self, method=False):
        self._method = method
        self._deputy = None

    def __call__(self, func, *args, **kwargs):
        # keep a sheriff ref
        this = self

        if self._method:
            def decorator(self, *args, **kw):
                # if dryrun is disabled exec the original method
                if get_status() is False:
                    return func(self, *args, **kw)

                # dryrun on: exec deputy method
                if this.deputy:
                    return this.deputy(self, *args, **kw)

                # no deputy: fallback on sham
                sham_decorator = sham(method=True)(func)
                return sham_decorator(self, *args, **kw)
        else:
            def decorator(*args, **kw):
                # if dryrun is disabled exec the original function
                if get_status() is False:
                    return func(*args, **kw)

                # dryrun on: exec deputy function
                if this.deputy:
                    return this.deputy(*args, **kw)

                ## no deputy: fallback on sham
                sham_decorator = sham(method=False)(func)
                return sham_decorator(*args, **kw)

        decorator.deputy = this._set_deputy
        return decorator

    @property
    def deputy(self):
        return self._deputy

    def _set_deputy(self, func):
        """Mark the *sheriff* substitute.

        Args:
            func: The function drypy will run in place of *sheriff*.

        Returns:
            *func* itself.
        """
        # func must be a callable
        if not getattr(func, '__call__', None):
            msg = "{} object is not a callable".format(type(func).__name__)
            raise TypeError(msg)

        self._deputy = func
