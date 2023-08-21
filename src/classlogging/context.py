"""Context manipulations"""

import typing as t
from contextvars import ContextVar
from threading import Lock

LOGGING_CONTEXT_HOLDER: ContextVar[t.Optional[t.Dict[str, dict]]] = ContextVar("LOGGING_CONTEXT_HOLDER", default=None)
_setter_lock = Lock()


def get_context_for_logger(logger_name: str) -> t.Optional[dict]:
    """Return all context variables for the logger"""
    all_contexts: t.Optional[dict] = LOGGING_CONTEXT_HOLDER.get()
    if all_contexts is None:
        return None
    return all_contexts.get(logger_name, None)


class LogContext:
    """Context wrapper"""

    def __init__(self, logger_name: str, **kwargs) -> None:
        self._logger_name: str = logger_name
        self._kwargs = kwargs

    def __enter__(self) -> None:
        """Set a variable for the logger"""
        with _setter_lock:
            all_contexts: dict = LOGGING_CONTEXT_HOLDER.get() or {}
            if self._logger_name not in all_contexts:
                all_contexts[self._logger_name] = {}
            all_contexts[self._logger_name].update(self._kwargs)
            LOGGING_CONTEXT_HOLDER.set(all_contexts)

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self._unset()
        return exc_type is None

    def _unset(self) -> None:
        with _setter_lock:
            all_contexts: dict = LOGGING_CONTEXT_HOLDER.get() or {}
            if self._logger_name not in all_contexts:
                return
            logger_context: dict = all_contexts[self._logger_name]
            for field_name in self._kwargs:
                if field_name not in logger_context:
                    continue
                logger_context.pop(field_name)
            if not logger_context:
                all_contexts.pop(self._logger_name)
            LOGGING_CONTEXT_HOLDER.set(all_contexts or None)
