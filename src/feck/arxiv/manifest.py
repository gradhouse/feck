# File: manifest.py
# Description: arXiv manifest class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.

from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
from zoneinfo import ZoneInfo

from feck.file.handler.xml_handler import XmlHandler


class Manifest:
    """
    Represents a manifest for managing metadata and contents,
    specifically designed for use with arXiv-related data.

    The manifest is stored as a dictionary with two main components:
      - 'metadata': A dictionary to store metadata information.
      - 'contents': A list to store content-related data.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the Manifest class.

        This constructor sets up the internal manifest dictionary and
        populates it with default values by calling the `_set_defaults` method.
        """

        self._manifest = dict()
        self._set_defaults()

    def clear(self) -> None:
        """
        Clears the manifest and resets it to its default state.

        This method removes all existing data from the manifest and
        reinitializes it with default values by calling the `_set_defaults` method.
        """

        self._manifest.clear()
        self._set_defaults()

    def _set_defaults(self) -> None:
        """
        Sets the default values for the manifest.

        This private method initializes the manifest with the following structure:
          - 'metadata': An empty dictionary to hold metadata.
          - 'contents': An empty list to hold content-related data.
        """
        self._manifest = {
            'metadata': {},
            'contents': []
        }

    def import_arxiv_xml(self, file_path: str) -> None:
        """
        Load manifest from an arXiv XML file.

        :param file_path: str, path to the arXiv XML file.
            The file is generally called arXiv_src_manifest.xml

        :raises FileNotFoundError: If the file is not found.
        :raises TypeError: If the file content is not in arXiv XML format.
        :raises ValueError: If a file entry is inconsistent.
        """

        self.clear()

        if not os.path.isfile(file_path):
            raise FileNotFoundError('arXiv XML file not found')

        xml_dict = XmlHandler.read_xml_to_dict(file_path)

        if not Manifest._is_arxiv_keys_present(xml_dict):
            raise TypeError('Entries missing in arXiv XML file')

        # set the metadata
        self._manifest['metadata'] = {
            'manifest_filename': os.path.basename(file_path),
            'timestamp_iso': Manifest._convert_arxiv_timestamp_to_iso(xml_dict['arXivSRC']['timestamp'])
        }

        self._manifest['contents'] = [Manifest._process_file_entry(file_entry)
                                      for file_entry in xml_dict['arXivSRC']['file']]

    @staticmethod
    def _process_file_entry(file_entry: dict) -> dict:
        """
        Process a single arXiv manifest 'file' entry.

        :param file_entry: dict, entry in the 'file' list of the arXiv manifest XML dictionary.
        :return: dict, processed entry to be added to the manifest.

        :raises ValueError: If the file entry is inconsistent.
        """

        if not Manifest._is_file_entry_consistent(file_entry):
            raise ValueError('Entry inconsistent')

        local_dict = {
            'filename': file_entry['filename'],
            'size_bytes': int(file_entry['size']),
            'timestamp_iso': Manifest._convert_arxiv_file_entry_timestamp_to_iso(file_entry['timestamp']),
            'year': int(
                f"19{file_entry['yymm'][:2]}" if int(file_entry['yymm'][:2]) > 90 else f"20{file_entry['yymm'][:2]}"),
            'month': int(file_entry['yymm'][2:]),
            'sequence_number': int(file_entry['seq_num']),
            'n_submissions': int(file_entry['num_items']),
            'hash': {
                'MD5': file_entry['md5sum'],
                'MD5_contents': file_entry['content_md5sum'],
            }
        }

        return local_dict

    @staticmethod
    def _is_arxiv_keys_present(xml_dict: dict) -> bool:
        """
        Determine if a arXiv source manifest XML dictionary has all required keys.

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

    @staticmethod
    def _convert_arxiv_timestamp_to_iso(timestamp: str) -> str:
        """
        Convert the arXiv XML timestamp xml['arXivSRC']['timestamp'] from EST to ISO 8601 GMT.

        :param timestamp: str, arXiv manifest timestamp.
            The arXiv manifest timestamp is initially in the same time zone as New York.
            The input format is for example 'Mon Apr  7 04:58:03 2025'
        :return: str, ISO 8601 GMT format timestamp.
            The output format is for example '2025-04-07T08:58:03+00:00'
        """

        eastern = ZoneInfo('America/New_York')
        original_time_format = '%a %b %d %H:%M:%S %Y'
        datetime_original = datetime.strptime(timestamp, original_time_format)
        datetime_est = datetime_original.replace(tzinfo=eastern)
        datetime_gmt = datetime_est.astimezone(ZoneInfo('UTC'))

        return datetime_gmt.isoformat()

    @staticmethod
    def _convert_arxiv_file_entry_timestamp_to_iso(timestamp: str) -> str:
        """
        Convert the arXiv XML file timestamp xml['arXivSRC']['file'][k]['timestamp'] from EST to ISO 8601 GMT.

        :param timestamp: str, arXiv manifest timestamp.
            The arXiv manifest timestamp is initially in the same time zone as New York.
            The input format is for example '2010-12-23 00:13:59'
        :return: str, ISO 8601 GMT format timestamp.
            The output format is for example '2025-04-07T08:58:03+00:00'
        """

        eastern = ZoneInfo('America/New_York')
        original_time_format = '%Y-%m-%d %H:%M:%S'
        datetime_original = datetime.strptime(timestamp, original_time_format)
        datetime_est = datetime_original.replace(tzinfo=eastern)
        datetime_gmt = datetime_est.astimezone(ZoneInfo('UTC'))

        return datetime_gmt.isoformat()

    @staticmethod
    def _is_file_entry_consistent(file_entry: dict) -> bool:
        """
        Determines if the file entry is consistent within the manifest.

        This checks that:
            1. The filename matches the pattern: src/arXiv_src_{yymm}_{seq_num}.tar
            2. The month is in range

        :param file_entry: dict, entry in the 'file' list of the arXiv manifest XML dictionary
        :return: bool, True if consistent, False otherwise.
        """

        is_consistent = True

        seq_num = int(file_entry['seq_num'])
        yymm = file_entry['yymm']
        entry_filename = file_entry['filename']
        generated_filename = f"src/arXiv_src_{yymm}_{seq_num:03d}.tar"  # consistency check

        if entry_filename != generated_filename:
            is_consistent = False

        month = int(file_entry['yymm'][2:])

        if month <= 0 or month > 12:
            is_consistent = False

        return is_consistent

    def get_statistics(self) -> dict:
        """
        Get summary statistics of the manifest.

        :return: dict, summary statistics of the manifest.
            The dictionary key is a (year, month) tuple.
            The dictionary value is also a dictionary with the keys 'size_bytes' and 'n_submissions'.
        """

        statistics = dict()
        for entry in self._manifest['contents']:
            key = (entry['year'], entry['month'])
            if key not in statistics:
                statistics[key] = {'size_bytes': 0, 'n_submissions': 0}
            statistics[key]['size_bytes'] += entry['size_bytes']
            statistics[key]['n_submissions'] += entry['n_submissions']

        return statistics

    def plot_summary_statistics(self) -> None:
        """
        Plot summary statistics of the manifest.

        The generated plots are:
            - the number of submissions per month
            - size of all submissions per month in GB
            - average submission size in MB
        """

        statistics = self.get_statistics()

        dates = [datetime(year, month, 1) for year, month in statistics.keys()]

        # Extract values for each metric
        n_submissions = np.array([entry['n_submissions'] for entry in statistics.values()])
        size_bytes = np.array([entry['size_bytes'] for entry in statistics.values()])

        plt.figure(figsize=(10, 5))
        plt.plot(dates, n_submissions, '.', label='n_submissions')
        plt.gcf().autofmt_xdate()
        plt.xlabel('Date (Year-Month)')
        plt.ylabel('Number of Submissions')
        plt.title('Number of Submissions per Month')
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.plot(dates, 1.0e-9 * size_bytes, '.', color='orange', label='size_bytes')
        plt.gcf().autofmt_xdate()
        plt.xlabel('Date (Year-Month)')
        plt.ylabel('Size (GB)')
        plt.title('Size in GB per Month')
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.plot(dates, 1.0e-6 * (size_bytes / n_submissions), '.', color='green', label='size_bytes')
        plt.gcf().autofmt_xdate()
        plt.xlabel('Date (Year-Month)')
        plt.ylabel('Average Submission Size (MB)')
        plt.title('Averaged Monthly Submission Size in MB')
        plt.grid(True)
        plt.show()
