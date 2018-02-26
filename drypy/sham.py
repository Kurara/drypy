"""
.. module:: sham
   :platform: Unix
   :synopsis: Basic decorator to implement dryrun

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import logging
from . import get_status

logger = logging.getLogger(__name__)


class sham:
    """Decorator which makes drypy to log the call of the target
    function without executing it.

    Example:
        >>> @sham(method=False)
        ... def foo(bar, baz=None):
        ...     pass
        ...
        >>> foo(bar, baz=42)
        INFO:drypy.sham:[DRYRUN] call to 'foo(bar, baz=42)'

    """
    def __init__(self, method=False):
        self._method = method

    def __call__(self, func):
        # keep a ref of sham instance
        this = self

        if self._method:
            def decorator(self, *args, **kwargs):
                # if dry run is disabled exec the original method
                if get_status() is False:
                    return func(self, *args, **kwargs)
                else:
                    this._log_args(func, *args, **kwargs)
                    return None
        else:
            def decorator(*args, **kwargs):
                # if dry run is disabled exec the original function
                if get_status() is False:
                    return func(*args, **kwargs)
                else:
                    this._log_args(func, *args, **kwargs)
                    return None

        return decorator

    def _log_args(self, func, *args, **kw):
        func_args = []
        if args:
            func_args.extend([str(arg) for arg in args])
        if kw:
            func_args.extend(["{k}={v}".format(k=k, v=v)
                              for k, v in kw.items()])

        msg = "[DRYRUN] call to '{func}({args})'"
        msg = msg.format(func=func.__name__, args=", ".join(func_args))

        logger.info(msg)
