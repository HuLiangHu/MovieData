from __future__ import unicode_literals
from six import unichr

import os
import re
from collections import OrderedDict
import subprocess

#from PIL import Image, ImageFont, ImageDraw

class IconFont(object):
    """Base class that represents web icon font"""
    def __init__(self,ttf_file):
        """ 
        :param ttf_file: path to icon font TTF file
        :param keep_prefix: whether to keep common icon prefix
        """ 
        self.ttf_file = ttf_file
        
    def image_to_string(self,img, cleanup=True, plus='-psm 6 digits'): 
        subprocess.check_output('tesseract ' + img + ' ' +
                                img + ' ' + plus, stderr=subprocess.STDOUT,shell=True)


        text = ''
        with open(img + '.txt', 'r') as f:
            text = f.read().strip()
        if cleanup:
            os.remove(img + '.txt')
        return text
         
    def export_icon(self, fontnum, size, color='black', scale='auto',
                    filename=None, export_dir='exported'):
        """
        Exports given icon with provided parameters.
        If the desired icon size is less than 150x150 pixels, we will first
        create a 150x150 pixels image and then scale it down, so that
        it's much less likely that the edges of the icon end up cropped.
        :param icon: valid icon name
        :param filename: name of the output file
        :param size: icon size in pixels
        :param color: color name or hex value
        :param scale: scaling factor between 0 and 1,
                      or 'auto' for automatic scaling
        :param export_dir: path to export directory
        """ 
        content = unichr(fontnum)
        org_size = size
        size = max(150, size)

        image = Image.new("RGB", (size, size), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        if scale == 'auto':
            scale_factor = 1
        else:
            scale_factor = float(scale)

        font = ImageFont.truetype(self.ttf_file, int(size * scale_factor))
        width, height = draw.textsize(content, font=font)

       
        draw.text((float(size - width) / 2, float(size - height) / 2),
                  content, font=font, fill=color)
 

        # Default filename
        if not filename:
            filename = str(fontnum) + '.jpg'

        # Save file
        image.save(os.path.join(export_dir, filename)) 
        return self.image_to_string(os.path.join(export_dir, filename))