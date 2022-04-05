import html
import re

import scrapy
from itemloaders.processors import Compose, Join, MapCompose, TakeFirst


def clean_list(r_list):
    '''receives list of description text, unescapes html entities,
        removes empty list items and returns the first 3 items
        contining the target data'''
    t_list = []
    for raw_text in r_list:
        cln_text = html.unescape(raw_text)
        if cln_text != str(' '):
            t_list.append(cln_text)
    return t_list[:3]


def find_dim_element(search_dmns, find_dmns, t_list):
    '''Searches list of parsed description text and returns the dimensions
        and their position in the list'''
    for count, text in enumerate(t_list):
        if bool(re.search(search_dmns, text)):
            dmns = re.findall(find_dmns, text)
            pos = count
            count += 1
        elif bool(re.search(r'(\d\s*[wW]+)', text)):
            dmns = re.findall(find_dmns, text)[:2]
            dmns.reverse()
            pos = count
            count += 1
        else:
            pass
    return dmns, pos


def find_media_0(t_list):
    '''Determines/assigns position of media data when dimensions
        data is found in text_list[0]'''
    if not bool(re.search(r'[(]+[^\d]+', t_list[1])):
        return t_list[1]
    else:
        return t_list[2]


def find_media_1(t_list):
    '''Determines/assigns position of media data when dimensions
        data is found in text_list[1]'''
    if not bool(re.search(r'[(]+[^\d]+', t_list[1])):
        return t_list[0]
    else:
        return t_list[2]


def find_media_2(t_list):
    '''Determines/assigns position of media data when dimensions
        data is found in text_list[2]'''
    if bool(re.search(r'(\d|\bWall\b)', t_list[1])):
        return t_list[0]
    else:
        return t_list[1]


def find_media(dmns_pos, t_list):
    '''Assigns media data relative to the position of dimensions data
        in list of parsed description text'''
    if dmns_pos == 0:
        media = find_media_0(t_list)
    elif dmns_pos == 1:
        media = find_media_1(t_list)
    else:
        media = find_media_2(t_list)
    return media


class ArtItem(scrapy.Item):
    '''Initiate ArtItem'''
    url = scrapy.Field()
    title = scrapy.Field()
    media = scrapy.Field()
    width_cm = scrapy.Field()
    height_cm = scrapy.Field()
    price_gbp = scrapy.Field()
