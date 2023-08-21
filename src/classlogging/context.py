"""Context manipulations"""

import functools
import typing as t
from contextvars import ContextVar
from threading import Lock

_logging_context_holder: ContextVar[t.Optional[t.Dict[str, dict]]] = ContextVar("_logging_context_holder", default=None)
_setter_lock = Lock()


@functools.lru_cache()
def get_context_for_logger(logger_name: str) -> t.Optional[dict]:
    """Return all context variables for the logger"""
    all_contexts: t.Optional[dict] = _logging_context_holder.get()
    if all_contexts is None:
        return None
    result_vars: t.Dict[str, t.Tuple[str, t.Any]] = {}
    for context_name, context_vars in all_contexts.items():
        # Check if context name applies to the selected logger
        if logger_name != context_name and not logger_name.startswith(f"{context_name}."):
            continue
        # Iterate through all active context vars
        for ctx_var_name, ctx_var_value in context_vars.items():
            known_var_context, _ = result_vars.setdefault(ctx_var_name, (context_name, ctx_var_value))
            if len(known_var_context) < len(context_name):
                result_vars[ctx_var_name] = (context_name, ctx_var_value)
    return {k: v for k, (_, v) in result_vars.items()}


class LogContext:
    """Context wrapper"""

    def __init__(self, logger_name: str, **kwargs) -> None:
        self._logger_name: str = logger_name
        self._kwargs = kwargs

    def __enter__(self) -> None:
        """Set a variable for the logger"""
        with _setter_lock:
            all_contexts: dict = _logging_context_holder.get() or {}
            if self._logger_name not in all_contexts:
                all_contexts[self._logger_name] = {}
            all_contexts[self._logger_name].update(self._kwargs)
            _logging_context_holder.set(all_contexts)
            get_context_for_logger.cache_clear()

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self._unset()
        return exc_type is None

    def _unset(self) -> None:
        with _setter_lock:
            all_contexts: dict = _logging_context_holder.get() or {}
            if self._logger_name not in all_contexts:
                return
            logger_context: dict = all_contexts[self._logger_name]
            for field_name in self._kwargs:
                if field_name not in logger_context:
                    continue
                logger_context.pop(field_name)
            if not logger_context:
                all_contexts.pop(self._logger_name)
            _logging_context_holder.set(all_contexts or None)
            get_context_for_logger.cache_clear()
