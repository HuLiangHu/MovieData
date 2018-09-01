from __future__ import unicode_literals

import os
from abc import ABCMeta, abstractmethod

import requests
from urllib.request import urlretrieve



class FontDownloader(object):
    """Abstract class for downloading icon font CSS and TTF files"""
    

    def __init__(self, directory=None):
        """
        :param directory: path to download directory; temporary dir if None
        """
        self.directory = directory

    def _download_file_from_url(self,url, directory=None):
        """
        Download file from given URL and save it in given directory

        :param url: URL of file
        :param directory: path to download directory
        :return: path to downloaded file
        """
        # Files are saved in temporary folder if `directory` isn't specified
        if not directory:
            return urlretrieve(url)[0]
        else:
            # Get the filename from URL
            css_filename = os.path.join(directory, url.split('/')[-1])
            return urlretrieve(url, filename=css_filename)[0] 

   
    def require_dir(self,path):
        try:
            os.makedirs(path)
        except OSError as exc:
            pass
     

    def download_font(self,font_url, directory):
        """Downloads icon font TTF file and returns its path"""
        self.require_dir(directory)
        print (directory)
        return self._download_file_from_url(font_url, directory)

  