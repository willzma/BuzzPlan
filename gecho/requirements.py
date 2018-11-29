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


log = logging.getLogger('gecho')


def get_footnotes(container):
    '''
    In the future, include optional keys for footnote index when noted in the table;
    then when this is called, return a list with the corresponding footnotes.

    A more advanced solution could maybe even eventually use NLP to figure out meaning.
    Otherwise, annotation by hand is probably necessary.
    '''
    raise NotImplementedError


def get_reqs(degree_dom, stats, no_reqs_tab=False, original_degree_name=None):
    '''
    Currently assumes the more consistent bachelor's degree format.
    '''
    has_errors = False

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
        stats.num_rows += 1
        row_type, row_text = row.attrib['class'], row.xpath('.//text()')
        if 'areaheader' in row_type:
            log.info("Parsing requirements for {} area".format(row_text[0]))
        code, hours, href, is_or = None, None, None, False
        comment, blockindent, last, areaheader = None, False, False, None
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
                    content = node.xpath('.//text()')
                    if content is not None:
                        areaheader = content[0].strip()
                        last = content[0].strip() == 'Total Credit Hours'
            node_queue.extend(node)
        if areaheader and not last:
            if hours != (-1):
                reqs_dict['requirements'].append({'comment': areaheader, 'codes': [], 'hours': hours})
            else:
                stats.num_areaheaders += 1
        elif last and not code: # Set number of credit hours for the degree/thread/concentration
            reqs_dict['total_credit_hours'] = hours
        elif is_or and code: # Append to the previous requirement
            reqs_dict['requirements'][-1]['codes'].append(code)
            stats.num_courses += 1
        elif comment and not code:
            req = {'comment': comment, 'codes': [], 'hours': hours}
            # Search manually written annotations/additions to fill in most unstructured data
            if full_degree_name in words and comment in words[full_degree_name]:
                req['codes'] = words[full_degree_name][comment]
            elif original_degree_name in words and comment in words[original_degree_name]:
                req['codes'] = words[original_degree_name][comment]
            elif comment in words['General']:
                req['codes'] = words['General'][comment]
            elif 'Any' in comment: # Any's are high complexity, encode to save space (just call JS API later)
                any_encodings, any_parts = [], comment.split(',')
                for part in any_parts:
                    abbrs = re.findall(r'[A-Z]{2,}', part)
                    any = '@any({})'.format(abbrs[-1])
                    any = any + '.filter({})'.format(abbrs[0]) if len(abbrs) > 1 else any
                    any_encodings.append(any)
                req['codes'] = any_encodings
            else:
                stats.num_tables_with_unresolved_comments += 1
            reqs_dict['requirements'].append(req) # Safe default option (potentially empty codes)
            stats.num_comments += 1
        elif blockindent and code: # Append to the previous requirement (note that this has lesser priority)
            reqs_dict['requirements'][-1]['codes'].append(code)
            stats.num_courses += 1
        else:
            if not code:
                log.warning("Skipped table row with no course code {}".format(html.tostring(row)))
                stats.num_rows_with_no_course_codes += 1
                has_errors = True
            else:
                if hours == (-1):
                    log.warning("{}: No hours for course {} in table, looking up...".format(full_degree_name, code))
                    code, name, hours, description = lookup_course(code)
                current_req = {'codes': [code], 'hours': hours}
                reqs_dict['requirements'].append(current_req)
                stats.num_courses += 1
    if has_errors:
        stats.num_tables_with_errors += 1
    return reqs_dict, full_degree_name
                