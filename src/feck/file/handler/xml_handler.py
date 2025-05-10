# File: xml_handler.py
# Description: Extensible Markup Language (XML) file handler methods.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

import os
import xml.etree.ElementTree as xml_element_tree_implementation
import xmltodict as xmltodict_implementation

from feck.file.file_type import FileType


class XmlHandler:
    """
    A class to handle Extensible Markup Language (XML) files.
    """

    _file_extension_map = {
        '.xml': [FileType.FILE_TYPE_XML]
    }

    @staticmethod
    def get_file_extension_map() -> dict:
        """
        Get the file extension map.
        :return: dict, dictionary of file extension and a list of associated file types.
        """

        return XmlHandler._file_extension_map

    @staticmethod
    def get_file_type_from_extension(file_extension: str) -> list:
        """
        Determine the file type from the file extension.

        :param file_extension: str, file extension
        :return: list, list of file type categories FileType determined by extension.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.
        """

        return XmlHandler._file_extension_map.get(file_extension.lower(), [FileType.FILE_TYPE_UNKNOWN])

    @staticmethod
    def get_file_type_from_format(file_path: str) -> FileType:
        """
        Determine the file type from the file format.

        :param file_path: str, path to the file
        :return: FileType, file type determined by the file format.
            If the file type is unknown, return FILE_TYPE_UNKNOWN.
        """

        is_xml = XmlHandler.is_xml_format(file_path)
        if is_xml:
            file_type_category = FileType.FILE_TYPE_XML
        else:
            file_type_category = FileType.FILE_TYPE_UNKNOWN

        return file_type_category

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
