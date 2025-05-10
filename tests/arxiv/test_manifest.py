# File: test_manifest.py
# Description: Unit tests for the arXiv Manifest class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import copy


from feck.arxiv.manifest import Manifest

# Sample valid xml_dict
valid_xml_dict = {
    'arXivSRC': {
        'file': [
            {
                'content_md5sum': 'cacbfede21d5dfef26f367ec99384546',
                'filename': 'src/arXiv_src_0001_001.tar',
                'first_item': 'astro-ph0001001',
                'last_item': 'quant-ph0001119',
                'md5sum': '949ae880fbaf4649a485a8d9e07f370b',
                'num_items': '2364',
                'seq_num': '1',
                'size': '225605507',
                'timestamp': '2010-12-23 00:13:59',
                'yymm': '0001'
            }
        ],
        'timestamp': '2010-12-23 00:00:00'
    }
}

# Test cases
def test_is_arxiv_xml_valid_with_valid_data():
    """
    Test that the method returns True for a valid xml_dict.
    """
    assert Manifest._is_arxiv_xml_valid(valid_xml_dict) is True

def test_is_arxiv_xml_valid_with_missing_top_level_key():
    """
    Test that the method returns False when the top-level key is missing.
    """
    invalid_dict = {}
    assert Manifest._is_arxiv_xml_valid(invalid_dict) is False

def test_is_arxiv_xml_valid_with_missing_arxivsrc_keys():
    """
    Test that the method returns False when 'arXivSRC' keys are missing.
    """

    invalid_dict = copy.deepcopy(valid_xml_dict)
    del invalid_dict['arXivSRC']['file']

    assert Manifest._is_arxiv_xml_valid(invalid_dict) is False

    invalid_dict = copy.deepcopy(valid_xml_dict)
    del invalid_dict['arXivSRC']['timestamp']

    assert Manifest._is_arxiv_xml_valid(invalid_dict) is False


def test_is_arxiv_xml_valid_with_non_string_value_in_timestamp():
    """
    Test that the method returns False when a value in 'file' is not a string.
    """
    invalid_dict = copy.deepcopy(valid_xml_dict)
    invalid_dict['arXivSRC']['timestamp'] = 1234  # should be a string

    assert Manifest._is_arxiv_xml_valid(invalid_dict) is False


def test_is_arxiv_xml_valid_with_invalid_file_structure():
    """
    Test that the method returns False when 'file' entries have missing keys.
    """
    invalid_dict = {
        'arXivSRC': {
            'file': [
                {
                    'content_md5sum': 'cacbfede21d5dfef26f367ec99384546',
                    'filename': 'src/arXiv_src_0001_001.tar'
                    # Missing other required keys
                }
            ],
            'timestamp': '2010-12-23 00:00:00'
        }
    }
    assert Manifest._is_arxiv_xml_valid(invalid_dict) is False

def test_is_arxiv_xml_valid_with_invalid_types():
    """
    Test that the method returns False when data types are incorrect.
    """
    invalid_dict = {
        'arXivSRC': {
            'file': [
                {
                    'content_md5sum': 12345,  # Should be a string
                    'filename': 'src/arXiv_src_0001_001.tar',
                    'first_item': 'astro-ph0001001',
                    'last_item': 'quant-ph0001119',
                    'md5sum': '949ae880fbaf4649a485a8d9e07f370b',
                    'num_items': '2364',
                    'seq_num': '1',
                    'size': '225605507',
                    'timestamp': '2010-12-23 00:13:59',
                    'yymm': '0001'
                }
            ],
            'timestamp': '2010-12-23 00:00:00'
        }
    }
    assert Manifest._is_arxiv_xml_valid(invalid_dict) is False

