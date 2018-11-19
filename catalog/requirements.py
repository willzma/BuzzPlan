'''
Functions for massaging requirements data from catalog.gatech.edu into Python dicts.
Objects could help to solve the problem of multiple options for a course req.
'''

from courses import lookup_course, parse_hours
from utils import asciify_spaces
from words import words
from lxml import html
import logging
import re


log = logging.getLogger('catalog')


def get_footnotes(container):
    '''
    In the future, include optional keys for footnote index when noted in the table;
    then when this is called, return a list with the corresponding footnotes.

    A more advanced solution could maybe even eventually use NLP to figure out meaning.
    Otherwise, annotation by hand is probably necessary.
    '''
    raise NotImplementedError


def get_reqs(degree_dom, no_reqs_tab=False, original_degree_name=None):
    '''
    Currently assumes the more consistent bachelor's degree format.
    '''
    reqs = degree_dom if no_reqs_tab else degree_dom.xpath('//*[@id="requirementstexttab"]')[0]
    full_degree_name = degree_dom.xpath('//*[@id="content"]/h1/text()')[0]
    table = reqs.xpath("//*[contains(@class, 'sc_courselist')]")
    if not table:
        log.warning("Requirements for " + full_degree_name + " not in table format, skipping...")
        return None
    else:
        table = table[0][3]
    
    log.info("Reading requirements for {}".format(full_degree_name))

    reqs_dict = {'requirements': []}
    for row in table:
        row_type, row_text = row.attrib['class'], row.xpath('.//text()')
        if 'areaheader' in row_type:
            log.info("Parsing requirements for {} area".format(row_text[0]))
        code, hours, href, is_or = None, None, None, False
        comment, blockindent, last, areaheader = None, False, False, False
        node_queue = [row]
        while node_queue:
            node = node_queue.pop(0)
            if 'title' in node.attrib:
                code = asciify_spaces(node.attrib['title'])
            if 'href' in node.attrib:
                href = node.attrib['href']
            if 'class' in node.attrib:
                if 'orclass' in node.attrib['class']:
                    is_or = True
                if node.attrib['class'] == 'courselistcomment':
                    comment = node.xpath('.//text()')[0] if comment is None else comment
                if node.attrib['class'] == 'blockindent':
                    blockindent = True
                if node.attrib['class'] == 'hourscol':
                    text = node.xpath('.//text()')
                    hours = parse_hours(text[0].strip()) if len(text) else (-1)
                if node.attrib['class'] == 'listsum':
                    last = True
                if 'areaheader' in node.attrib['class']:
                    areaheader, content = True, node.xpath('.//text()')
                    if content is not None and content[0].strip() == 'Total Credit Hours':
                        last = True
            node_queue.extend(node)
        if is_or and comment:
            raise ValueError("Probably want to look at this, chief.")
        if is_or: # Append to the previous requirement
            reqs_dict['requirements'][-1]['codes'].append(code)
        elif comment and not code:
            # Search manually written annotations/additions to fill in most unstructured data
            if full_degree_name in words and comment in words[full_degree_name]:
                reqs_dict['requirements'].append({'codes': words[full_degree_name][comment], 'hours': hours})
            elif original_degree_name in words and comment in words[original_degree_name]:
                reqs_dict['requirements'].append({'codes': words[original_degree_name][comment], 'hours': hours})
            elif comment in words['General']:
                reqs_dict['requirements'].append({'codes': words['General'][comment], 'hours': hours})
            elif 'Any' in comment: # Any's are high complexity, encode to save space (just call JS API later)
                any_encodings, any_parts = [], comment.split(',')
                for part in any_parts:
                    abbrs = re.findall(r'[A-Z]{2,}', part)
                    any = '@any({})'.format(abbrs[-1])
                    any = any + '.filter({})'.format(abbrs[0]) if len(abbrs) > 1 else any
                    any_encodings.append(any)
                reqs_dict['requirements'].append({'codes': [any_encodings], 'hours': hours})
            else:
                reqs_dict['requirements'].append({'codes': [], 'hours': hours}) # Safe (could be empty)
        elif blockindent: # Append to the previous requirement (note that this has lesser priority)
            reqs_dict['requirements'][-1]['codes'].append(code)
        elif last: # Set number of credit hours for the degree/thread/concentration
            reqs_dict['total_credit_hours'] = hours
        else:
            if areaheader:
                if hours != (-1):
                    reqs_dict['requirements'].append({'codes': [], 'hours': hours})
            elif not code:
                log.warning("Skipped table row with no course code {}".format(html.tostring(row)))
            else:
                if hours == (-1):
                    log.warning("{}: No hours for course {} in table, looking up...".format(full_degree_name, code))
                    code, name, hours, description = lookup_course(code)
                current_req = {'codes': [code], 'hours': hours}
                reqs_dict['requirements'].append(current_req)
    return reqs_dict, full_degree_name
                