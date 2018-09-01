from itertools import chain
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode
from douban.spiders.fonthelper.font_to_png import IconFont, FontDownloader
import json
import os
import base64
import hashlib


def extract_fonts(fontdata):
    filename = hashlib.md5(fontdata).hexdigest() + ".woff"
    fontfile = os.path.join("fonts", filename)
    export_dir = "fonts/" + filename.split('.')[0]

    try:

        os.makedirs(export_dir)

    except OSError as exc:
        pass

    if os.path.isfile(os.path.join(export_dir, 'mappings.json')):
        with open(os.path.join(export_dir, 'mappings.json')) as data_file:
            return json.load(data_file)
    else:
        fontdata = base64.b64decode(fontdata)
        with open(fontfile, 'wb') as f:
            f.write(fontdata)

    icon_font = IconFont(fontfile)
    ttf = TTFont(fontfile)

    font_mapping = {}
    contents = []
    for x in ttf["cmap"].tables:
        for id, name in x.cmap.items():
            if name != 'glyph00000':
                if id not in contents:
                    contents.append(id)
    for content in contents:
        if content != 120:
            number = icon_font.export_icon(content, 100, export_dir=export_dir)
            font_mapping[str(content)] = int(number)
            # font_mapping.append((content,number))

    with open(os.path.join(export_dir, 'mappings.json'), 'w') as fp:
        json.dump(font_mapping, fp)
        return font_mapping


if __name__ == '__main__':
    font_mapping = extract_fonts(
        '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')
    print (font_mapping)


