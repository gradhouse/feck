# File: file_type.py
# Description: File type categories.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.


from enum import Enum

class FileType(Enum):
    """
    Enumeration for file type categories.

    This enum is used to categorize files based on their extension or format.
    """

    FILE_TYPE_UNKNOWN = 'UNKNOWN'

    FILE_TYPE_XML = 'XML'
