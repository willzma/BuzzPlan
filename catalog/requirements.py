'''
Functions for massaging requirements data from catalog.gatech.edu into Python dicts.
Objects could help to solve the problem of multiple options for a course req.
'''

from config import catalog_url, courses_href, unique_abbrs
from courses import lookup_abbrs
from lxml import etree
from lxml import html
import requests
import re

def get_hours(row):
    '''
    Given a row in the DOM, returns credit hours; if not found, -1.
    '''
    for cell in row[1:]:
        if 'class' in cell.attrib:
            if cell.attrib['class'] == 'hourscol':
                if len(cell.xpath('.//text()')):
                    return int(cell.xpath('.//text()')[0].strip())
    return -1

def get_reqs(full_degree_name, degree_info):
    '''
    Currently assumes the more consistent bachelor's degree format.
    '''
    reqs = degree_info.xpath('//*[@id="requirementstexttab"]')[0]
    table = reqs.xpath("//*[contains(@class, 'sc_courselist')]")
    if not table:
        print("Requirements for " + full_degree_name + " not in table format, skipping...")
        return None
    else:
        table = table[0][3]

    reqs_dict, current_area = {}, None
    area_dict, current_req = None, 0
    for row in table:
        row_type, row_text = row.attrib['class'], row.xpath('.//text()')
        if 'areaheader' in row_type: # is a req area
            current_area, area_dict = row_text[0], {}
            area_dict[0], current_req = {}, 0
            print(current_area)
        else:
            if 'class' in row[0].attrib: # course defined
                definition, select = row[0].attrib['class'], len(row[0][0])
                elem = row[0][0][0] if select else row[0][0]
                href = elem.attrib['href'] if 'href' in elem.attrib else None
                code = elem.attrib['title'].replace(u'\xa0', ' ') if 'title' in elem.attrib else None
                if 'orclass' in definition: # append to previous req
                    print('wew')
                elif select:
                    print('mem')
                elif 'courselistcomment' in elem.attrib['class']:
                    print('requirement with no name')
                else: # new req
                    hours = get_hours(row)
                    if hours == -1:
                        raise KeyError(full_degree_name + ": No hours for course " + code)
            else: # courselistcomment such as 'Select one of the following:'
                comment = str(row[0].xpath('.//text()'))
                if "Any" in comment:
                    abbrs = re.findall(r'[A-Z]{2,}', comment)
                    print(lookup_abbrs(abbrs))