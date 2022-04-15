"""
Tracing for the graphql-core library.

https://github.com/graphql-python/graphql-core
"""

import logging
import os

import graphql
import graphql.execution
import wrapt
from ddtrace.util import unwrap

from ddtrace_graphql.base import traced_graphql_wrapped

logger = logging.getLogger(__name__)


def patch(span_kwargs=None, span_callback=None, ignore_exceptions=()):
    """
    Monkeypatches graphql-core library to trace graphql calls execution.
    """

    def wrapper(func, _, args, kwargs):
        return traced_graphql_wrapped(
            func,
            args,
            kwargs,
            span_kwargs=span_kwargs,
            span_callback=span_callback,
            ignore_exceptions=ignore_exceptions,
        )

    logger.debug("Patching `graphql.graphql` function.")

    wrapt.wrap_function_wrapper(graphql, "graphql", wrapper)

    logger.debug("Patching `graphql.execution.execute` function.")

    wrapt.wrap_function_wrapper(graphql.execution, "execute", wrapper)


def unpatch():
    logger.debug("Unpatching `graphql.graphql` function.")
    unwrap(graphql, "graphql")
    logger.debug("Unpatching `graphql.execution.execute` function.")
    unwrap(graphql.execute, "execute")
