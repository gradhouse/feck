# File: xml_handler.py
# Description: Extensible Markup Language (XML) file handler methods.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
import xml.etree.ElementTree as xml_element_tree_implementation
import xmltodict as xmltodict_implementation


class XmlHandler:
    """
    A class to handle Extensible Markup Language (XML) files.
    """

    @staticmethod
    def is_xml_format(file_path: str) -> bool:
        """
        Determine if the file content is in Extensible Markup Language (XML) format.

        :param file_path: str, path to the file
        :return: bool, True if the file is in XML format, False otherwise.

        :raises FileNotFoundError: If the file is not found.
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError('file not found')

        try:
            with open(file_path, 'r') as file_handle:
                xml_element_tree_implementation.parse(file_handle)
            is_xml_format = True
        except xml_element_tree_implementation.ParseError:
            is_xml_format = False

        return is_xml_format
