#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Starts from catalog.gatech.edu and attempts to read all degree
information into JSON format at once.

Could perhaps use a name more appropriate to its function.
Job of this module: get all relevant DOMs under their degrees/programs.

Comment: let users go through a checklist for their major and
indicate the classes they've already taken as well as 
those that are supplementary; allow them to mark off certain
requirements as already completed, say, if done with AP credit
or something of that sort.

Initially created for the 2018-2019 catalog.

NOTE: It's become known to me that you can in fact download
your DegreeWorks audits as PDF files, which you can then
potentially convert to text using pdftotext or something or
other and then upload to this package/webapp to be parsed.
'''

from config import catalog_url, supported_degrees, excluded_programs, excluded_degrees, no_reqs_tabs
from config import num_programs, num_degrees, num_degrees_with_threads, num_threads
from requirements import get_reqs
from utils import get_hrefs
from lxml import html
import logging
import requests
import json


log = logging.getLogger('catalog')


def scrape_raw():
    '''
    Scrapes the raw catalog data into Python dicts.
    '''

    global num_programs
    global num_degrees
    global num_degrees_with_threads
    global num_threads

    catalog = requests.get(catalog_url + '/programs')
    catalog_tree = html.fromstring(catalog.content)
    catalog_dict = {}

    programs = catalog_tree.xpath('//*[@id="alltextcontainer"]/ul')[0]
    for program in programs:
        # DOM formats name as such: 'Aerospace Engineering.   '
        program_name = program.text.strip()[:-1]
        if program_name in excluded_programs:
            log.info("Skipped excluded program {}.".format(program_name))
            continue
        program_dict = {}
        log.info("Getting degree programs under {}".format(program_name))
        for degree_type in program:
            subpath = degree_type.attrib['href'].strip()
            degree_name = degree_type.text.strip()
            full_degree_name = degree_name + " in " + program_name
            if full_degree_name in excluded_degrees:
                log.info("Skipped excluded degree {}.".format(full_degree_name))
                continue
            if degree_name in supported_degrees:
                degree_dom = html.fromstring(requests.get(catalog_url + subpath).content)
                degree_dict = {'overview' : list(filter(None, get_overview(degree_dom)))}
                tabs = degree_dom.xpath('//*[@id="tabs"]')
                if not tabs:
                    log.info("No tabs found for {}, only getting overview".format(full_degree_name))
                else:
                    reqs_tab = degree_dom.xpath('//*[@id="requirementstexttab"]')
                    if not reqs_tab:
                        concentrations_tab = degree_dom.xpath('//*[@id="concentrationstexttab"]')
                        threads_tab = degree_dom.xpath('//*[@id="threadstexttab"]')
                        container = None
                        if concentrations_tab:
                            log.info("Opening concentrations for {}".format(full_degree_name))
                            container = degree_dom.xpath('//*[@id="concentrationstextcontainer"]')[0]
                        if threads_tab:
                            log.info("Opening threads for {}".format(full_degree_name))
                            container = degree_dom.xpath('//*[@id="threadstextcontainer"]')[0]
                        if container is None:
                            log.info("{} had no requirements, threads, or concentrations".format(full_degree_name))
                        else:
                            hrefs, degree_dict['threads'] = get_hrefs(container), {}
                            for href in hrefs:
                                thread_dom = html.fromstring(requests.get(catalog_url + href).content)
                                result = get_reqs(thread_dom, program_name in no_reqs_tabs, full_degree_name)
                                if result:
                                    degree_dict['threads'][result[1]] = result[0]
                                num_threads += 1
                            num_degrees_with_threads += 1
                    else:
                        result = get_reqs(degree_dom, original_degree_name=full_degree_name)
                        if result:
                            degree_dict['requirements'] = result[0]
                program_dict[degree_name] = degree_dict
                num_degrees += 1
        catalog_dict[program_name] = program_dict
        num_programs += 1
        print("\n")
    log.info("Processed {} degrees in {} programs.".format(str(num_degrees), str(num_programs)))
    log.info("Processed {} concentrations/threads in {} degrees".format(str(num_threads), str(num_degrees_with_threads)))
    log.info("Have you noticed that EVERY degree is a science degree, according to our catalog?")
    return catalog_dict


def get_overview(degree_dom):
    return [s.strip() for s in degree_dom.xpath('//*[@id="textcontainer"]')[0].xpath('.//text()')]


if __name__ == "__main__":
    with open('data.json', 'w') as f:
        json.dump(scrape_raw(), f)