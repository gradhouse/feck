# File: test_file_type.py
# Description: Unit tests for the FileType class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from feck.file.file_type import FileType


def test_enum_members_exist():
    """
    Test that the FileType members are present
    """
    assert hasattr(FileType, 'FILE_TYPE_UNKNOWN')
    assert hasattr(FileType, 'FILE_TYPE_XML')


def test_enum_values():
    """
    Test that the FileType enum values match expected values
    """
    assert FileType.FILE_TYPE_UNKNOWN.value == 'UNKNOWN'
    assert FileType.FILE_TYPE_XML.value == 'XML'

def test_enum_no_extra_members():
    """
    Test that no new members have been added to the FileType enum.
    """
    expected_members = {'FILE_TYPE_UNKNOWN', 'FILE_TYPE_XML'}
    actual_members = set(FileType.__members__.keys())
    assert actual_members == expected_members, f"Unexpected members found: {actual_members - expected_members}"
