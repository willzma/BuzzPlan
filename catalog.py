#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Starts from catalog.gatech.edu and attempts to read all degree
information into JSON/Firebase format at once.

Could perhaps use a name more appropriate to its function.

Last updated: November 5, 2018
"""

from lxml import etree
from lxml import html
import pyrebase
import requests

catalog_url = 'http://catalog.gatech.edu'
supported_degrees = ['BS', 'MS']

# Useful catalog numbers/statistics
num_programs = 0
num_degrees = 0
num_degrees_no_concentrations = 0

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
        print("\n")
        print(program_name)
        for degree_type in program:
            subpath = degree_type.attrib['href'].strip()
            degree_name = degree_type.text.strip()
            if degree_name in supported_degrees:
                degree_info = html.fromstring(
                    requests.get(catalog_url + subpath).content)
                overview = get_overview(degree_info)
                tabs = degree_info.xpath('//*[@id="tabs"]')
                if not tabs:
                    print("No tabs were found, only getting overview")
                else:
                    requirements_tab = degree_info.xpath('//*[@id="requirementstexttab"]')
                    if not requirements_tab:
                        print("Need to find concentrations/threads/specializations")
                    else:
                        parse_requirements(degree_info)
                    num_degrees_no_concentrations += 1
                num_degrees += 1
        num_programs += 1
        print("\n")
    print(num_programs, num_degrees, num_degrees_no_concentrations)

def get_overview(degree_info):
    return degree_info.xpath('//*[@id="textcontainer"]')[0]

def parse_requirements(degree_info):
    requirements = degree_info.xpath('//*[@id="requirementstexttab"]')[0]
    table = requirements.xpath("//*[contains(@class, 'sc_courselist')]")[0][3]
    print(html.tostring(table))

if __name__ == "__main__":
    scrape()