import requests
import re
import os
from fontTools.ttLib import TTFont


def font_creator(html):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }

    woff_name = re.search(r"url\('//vfile.meituan.net/colorstone/(.*\.woff)'\)", html).group(1)


    file_list = os.listdir('./font')
    if woff_name not in file_list:
        woff_url = 'http://vfile.meituan.net/colorstone/' + woff_name
        response_woff = requests.get(woff_url, headers=headers).content
        with open('./font/' + woff_name, 'wb') as f:
            f.write(response_woff)


    baseFonts = TTFont('./font/basefonts.woff')
    base_nums = ['9', '4', '2', '1', '3', '7', '8', '0', '6', '5']
    base_fonts = ['uniECE2', 'uniF284', 'uniF5F6', 'uniE3CA', 'uniF798', 'uniF7E7', 'uniF020', 'uniE4A7', 'uniF4B5',
                  'uniE0FC']


    onlineFonts = TTFont('./font/' + woff_name)
    uni_list = onlineFonts.getGlyphNames()[1:-1]
    temp = {}

    for i in range(10):
        onlineGlyph = onlineFonts['glyf'][uni_list[i]]
        for j in range(10):
            baseGlyph = baseFonts['glyf'][base_fonts[j]]
            if onlineGlyph == baseGlyph:
                temp["&#x" + uni_list[i][3:].lower() + ';'] = base_nums[j]


    pat = '(' + '|'.join(temp.keys()) + ')'
    html = re.sub(pat, lambda x: temp[x.group()], html)

    return html