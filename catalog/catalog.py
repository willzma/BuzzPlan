#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Starts from catalog.gatech.edu and attempts to read all degree
information into JSON/Firebase format at once.

Could perhaps use a name more appropriate to its function.

Comment: let users go through a checklist for their major and
indicate the classes they've already taken as well as 
those that are supplementary; allow them to mark off certain
requirements as already completed, say, if done with AP credit
or something of that sort.

Initially created for the 2018-2019 catalog.
'''

from config import catalog_url, supported_degrees, excluded_programs
from config import num_programs, num_degrees, num_degrees_no_concentrations
from requirements import get_reqs
from lxml import etree
from lxml import html
import pyrebase
import requests

def scrape():
    global num_programs
    global num_degrees
    global num_degrees_no_concentrations

    # Download the programs page... use to navigate
    catalog = requests.get(catalog_url + '/programs')
    catalog_tree = html.fromstring(catalog.content)

    # The programs contains only itself in the DOM
    programs = catalog_tree.xpath('//*[@id="alltextcontainer"]/ul')[0]
    for program in programs:
        # DOM formats name as such: 'Aerospace Engineering.   '
        program_name = program.text.strip()[:-1]
        if program_name in excluded_programs:
            continue
        print("\n")
        print(program_name)
        for degree_type in program:
            subpath = degree_type.attrib['href'].strip()
            degree_name = degree_type.text.strip()
            full_degree_name = degree_name + " in " + program_name
            if degree_name in supported_degrees:
                degree_info = html.fromstring(
                    requests.get(catalog_url + subpath).content)
                overview = get_overview(degree_info)
                tabs = degree_info.xpath('//*[@id="tabs"]')
                if not tabs:
                    print("No tabs found for " + full_degree_name + ", only getting overview")
                else:
                    reqs_tab = degree_info.xpath('//*[@id="requirementstexttab"]')
                    if not reqs_tab:
                        print("Need to find concentrations/threads/specializations")
                    else:
                        get_reqs(full_degree_name, degree_info)
                    num_degrees_no_concentrations += 1
                num_degrees += 1
        num_programs += 1
        print("\n")
    print("Processed " + str(num_degrees) + " degrees in "  + str(num_programs) + " programs.")
    print(str(num_degrees_no_concentrations) + " of " + str(num_degrees) + " degrees had no concentrations.")

def get_overview(degree_info):
    return degree_info.xpath('//*[@id="textcontainer"]')[0]

if __name__ == "__main__":
    scrape()