"""
type_safety.py

This module provides helper functions for input/output validation and type checking,
ensuring that functions receive the correct types and values.
"""

from typing import Any, Type

def validate_input(value: Any, expected_type: Type, param_name: str = "parameter") -> None:
    """
    Validate that the input is of the expected type.
    Raises a TypeError if the validation fails.
    """
    if not isinstance(value, expected_type):
        raise TypeError(f"{param_name} must be of type {expected_type.__name__}, got {type(value).__name__} instead.")

def validate_output(value: Any, expected_type: Type, param_name: str = "output") -> None:
    """
    Validate that the output is of the expected type.
    Raises a TypeError if the validation fails.
    """
    if not isinstance(value, expected_type):
        raise TypeError(f"{param_name} must be of type {expected_type.__name__}, got {type(value).__name__} instead.")
