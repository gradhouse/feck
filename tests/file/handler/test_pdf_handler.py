# File: test_pdf_handler.py
# Description: Unit tests for the PdfHandler class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
import pytest

from feck.file.handler.pdf_handler import PdfHandler
from feck.file.file_type import FileType

# test data directory
TEST_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
TEST_DATA_DIRECTORY = os.path.join(TEST_DIRECTORY, 'sample_files')


@pytest.mark.parametrize("file_extension, expected_type", [
    ('.pdf', [FileType.FILE_TYPE_PDF]),
    ('.pdfq', [FileType.FILE_TYPE_UNKNOWN]),
    ('', [FileType.FILE_TYPE_UNKNOWN]),
])
def test_get_file_type_from_extension(file_extension, expected_type):
    """
    Test the get_file_type_from_extension function
    """
    file_type = PdfHandler.get_file_type_from_extension(file_extension)
    assert file_type == expected_type

@pytest.mark.parametrize("filename, expected_is_pdf_file", [
    ('ps/ps_file.ps', False),                 # not a pdf file
    ('pdf/pdf_file.pdf', True),               # pdf file with correct formatting
    ('pdf/pdf_file_wrong_header.pdf', False), # pdf file with incorrect format header
    ('pdf/pdf_file_bad_truncated.pdf', False) # pdf file where the file is too short
])
def test_is_pdf_format(filename, expected_is_pdf_file):
    """
    Test the is_pdf_format method when a file is present
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    is_pdf_file = PdfHandler.is_pdf_format(full_path)
    assert is_pdf_file == expected_is_pdf_file

def test_is_pdf_format_raise_file_not_found():
    """
    Test the is_pdf_format method when the file is not found or the path directs to a non-file.
    """
    # test case: directory, is_pdf_format is only for files
    file_path = TEST_DATA_DIRECTORY
    with pytest.raises(FileNotFoundError):
        PdfHandler.is_pdf_format(file_path)

    # test case: file not found
    file_path = 'this_is_not_a_file'
    with pytest.raises(FileNotFoundError):
        PdfHandler.is_pdf_format(file_path)

@pytest.mark.parametrize("filename, expected_file_type", [
    ('ps/ps_file.ps', FileType.FILE_TYPE_UNKNOWN),                # not a pdf file
    ('pdf/pdf_file.pdf', FileType.FILE_TYPE_PDF),                  # pdf file with correct formatting
    ('pdf/pdf_file_wrong_header.pdf', FileType.FILE_TYPE_UNKNOWN), # pdf file with incorrect format header
    ('pdf/pdf_file_bad_truncated.pdf', FileType.FILE_TYPE_UNKNOWN) # pdf file where the file is too short
])
def test_get_file_type_from_format(filename, expected_file_type):
    """
    Test the get_file_type_from_format method when the file is present.
    """
    full_path = os.path.join(TEST_DATA_DIRECTORY, filename)
    file_type = PdfHandler.get_file_type_from_format(full_path)
    assert file_type == expected_file_type

def test_get_file_extension_map():
    """
    Test that get_file_extension_map returns the correct file extension map.
    """

    expected_map = {'.pdf': [FileType.FILE_TYPE_PDF]}
    result = PdfHandler.get_file_extension_map()

    assert isinstance(result, dict), "The result should be a dictionary."
    assert result == expected_map, "The returned file extension map is incorrect."
