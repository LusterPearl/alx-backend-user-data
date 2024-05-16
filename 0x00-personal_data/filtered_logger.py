#!/usr/bin/env python3
"""
Module for obfuscating log messages containing sensitive fields.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated.
    Arguments:
    - fields: List of strings representing all fields to obfuscate.
    - redaction: String representing what the field will be obfuscated with.
    - message: String representing the log line.
    - separator: String representing by which character the fields.
    Returns:
    - Obfuscated log message.
    """
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern, lambda m: f'{
                  m.group().split("=")[0]}={redaction}', message)
