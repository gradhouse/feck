# File: manifest.py
# Description: arXiv manifest class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.


from feck.file.handler.xml_handler import XmlHandler


class Manifest:
    """
    arXiv manifest class.
    """

    @staticmethod
    def _is_arxiv_xml_valid(xml_dict: dict) -> bool:
        """
        Determine if a arXiv source manifest XML dictionary is valid.

        The dictionary must adhere to the following structure to be considered valid:

        - Top-level keys:
            - 'arXivSRC': A dictionary containing:
                - 'timestamp': str
                - 'file': A list of dictionaries, where each dictionary must contain the following keys,
                    each key has a string value:
                    - 'content_md5sum'
                    - 'filename'
                    - 'first_item'
                    - 'last_item'
                    - 'md5sum'
                    - 'num_items'
                    - 'seq_num'
                    - 'size'
                    - 'timestamp'
                    - 'yymm'

        :param xml_dict: dict, arXiv manifest XML dictionary.
        :return: bool, True if valid, False otherwise.
        """

        expected_top_level_keys = {'arXivSRC'}
        expected_src_keys = {'file', 'timestamp'}
        expected_file_keys = {'content_md5sum', 'filename', 'first_item', 'last_item', 'md5sum', 'num_items', 'seq_num',
                              'size', 'timestamp', 'yymm'}
        
        is_valid = False

        if set(xml_dict.keys()) == expected_top_level_keys:
            if set(xml_dict['arXivSRC'].keys()) == expected_src_keys:
                if (isinstance(xml_dict['arXivSRC']['timestamp'], str)
                        and isinstance(xml_dict['arXivSRC']['file'], list)):
                    is_valid = all([set(entry.keys()) == expected_file_keys for entry in xml_dict['arXivSRC']['file']])
                    if is_valid:
                        is_valid = all([isinstance(value, str) for entry in xml_dict['arXivSRC']['file']
                                        for _, value in entry.items()])

        return is_valid
