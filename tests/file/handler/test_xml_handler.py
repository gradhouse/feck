# File: test_xml_handler.py
# Description: Unit tests for the XmlHandler class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
import tempfile
import pytest

from feck.file.file_type import FileType
from feck.file.handler.xml_handler import XmlHandler


def test_get_file_extension_map():
    """
    Test the get_file_extension_map method.

    This test verifies that the method returns the correct mapping of file extensions
    to their corresponding file types.
    """
    expected_map = {
        '.xml': [FileType.FILE_TYPE_XML]
    }
    assert XmlHandler.get_file_extension_map() == expected_map


@pytest.mark.parametrize("file_extension, expected_file_type", [
    (".xml", [FileType.FILE_TYPE_XML]),
    (".unknown", [FileType.FILE_TYPE_UNKNOWN]),
    (".XML", [FileType.FILE_TYPE_XML]),  # Test case-insensitivity
])
def test_get_file_type_from_extension(file_extension, expected_file_type):
    """
    Test the get_file_type_from_extension method.

    This test ensures that the method correctly maps file extensions to their
    corresponding file types, including handling unknown extensions and case-insensitivity.
    """
    assert XmlHandler.get_file_type_from_extension(file_extension) == expected_file_type


def test_get_file_type_from_format_xml(mocker):
    """
    Test the get_file_type_from_format method when the file is XML.

    This test mocks the is_xml_format method to return True and verifies that
    the get_file_type_from_format method correctly identifies the file type as XML.
    """
    mocker.patch("feck.file.handler.xml_handler.XmlHandler.is_xml_format", return_value=True)
    assert XmlHandler.get_file_type_from_format("dummy_path.xml") == FileType.FILE_TYPE_XML


def test_get_file_type_from_format_unknown(mocker):
    """
    Test the get_file_type_from_format method when the file is not XML.

    This test mocks the is_xml_format method to return False and verifies that
    the get_file_type_from_format method correctly identifies the file type as unknown.
    """
    mocker.patch("feck.file.handler.xml_handler.XmlHandler.is_xml_format", return_value=False)
    assert XmlHandler.get_file_type_from_format("dummy_path.unknown") == FileType.FILE_TYPE_UNKNOWN


def test_is_xml_format_with_valid_xml():
    """
    Test the is_xml_format method with valid XML content.

    This test creates a temporary file containing valid XML content and verifies
    that the method correctly identifies it as XML.
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        temp_file.write("<root><child>Test</child></root>")
        temp_file_path = temp_file.name

    try:
        assert XmlHandler.is_xml_format(temp_file_path) is True
    finally:
        os.remove(temp_file_path)


def test_is_xml_format_with_invalid_xml():
    """
    Test the is_xml_format method with invalid XML content.

    This test creates a temporary file containing invalid XML content (missing a closing tag)
    and verifies that the method correctly identifies it as not being XML.
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        temp_file.write("<root><child>Test</child>")  # Missing closing tag
        temp_file_path = temp_file.name

    try:
        assert XmlHandler.is_xml_format(temp_file_path) is False
    finally:
        os.remove(temp_file_path)


def test_is_xml_format_with_non_xml_content():
    """
    Test the is_xml_format method with non-XML content.

    This test creates a temporary file containing non-XML content and verifies
    that the method correctly identifies it as not being XML.
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        temp_file.write("This is not XML content.")
        temp_file_path = temp_file.name

    try:
        assert XmlHandler.is_xml_format(temp_file_path) is False
    finally:
        os.remove(temp_file_path)


def test_is_xml_format_file_not_found(mocker):
    """
    Test the is_xml_format method when the file does not exist.

    This test mocks the os.path.isfile method to return False and verifies that
    the method raises a FileNotFoundError when the file is not found.
    """
    mocker.patch("os.path.isfile", return_value=False)
    with pytest.raises(FileNotFoundError):
        XmlHandler.is_xml_format("non_existent_file.xml")


def test_is_xml_format_with_mocked_file(mocker):
    """
    Test the is_xml_format method with mocked valid XML content.

    This test mocks the file reading process to simulate a file containing valid XML content
    and verifies that the method correctly identifies it as XML.
    """
    mock_data = "<root><child>Test</child></root>"
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_data))
    mocker.patch("os.path.isfile", return_value=True)
    assert XmlHandler.is_xml_format("mocked_file.xml") is True


def test_is_xml_format_with_mocked_invalid_xml(mocker):
    """
    Test the is_xml_format method with mocked invalid XML content.

    This test mocks the file reading process to simulate a file containing invalid XML content
    (missing a closing tag) and verifies that the method correctly identifies it as not being XML.
    """
    mock_data = "<root><child>Test</child>"  # Missing closing tag
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_data))
    mocker.patch("os.path.isfile", return_value=True)
    assert XmlHandler.is_xml_format("mocked_file.xml") is False
