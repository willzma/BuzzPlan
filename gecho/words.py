'''
Requirements sometimes (about 10% of the time) give vague words instead of an actual course list.
As such, encoded here is the actual meaning of some of those vague words. Effectively overrides.
'''

from gecho.courses import get_core_area, lookup_abbr

words = {
    'General': {
        'Lab Science': [
            'PHYS 2211', 
            'PHYS 2212', 
            'EAS 1600', 
            'EAS 1601', 
            'EAS 2600', 
            'CHEM 1310', 
            'CHEM 1211K', 
            'CHEM 1212K', 
            'BIO 1220', 
            'BIO 1510', 
            'BIO 1520'
        ],
        'Junior Design Option': [
            'LMC 3432', 
            'LMC 3431', 
            'CS 3311', 
            'CS 3312'
        ],
        'Free Electives': [
            'FREE 9999'
        ]
    },
    'BS in Aerospace Engineering': {
        'AE Options': [
            'AE 4040',
            'AE 4220',
            'AE 4552',
            'AE 4580',
            'AE 4791',
            'ME 4791'
        ],
        'Math Option': [
            'MATH 3215', 
            'MATH 3670',
            'MATH 4305',
            'MATH 4317',
            'MATH 4320',
            'MATH 4347',
            'MATH 4541',
            'MATH 4581',
            'MATH 4640'
        ]
    },
    'BS in Applied Languages and Intercultural Studies': {
        'Tech Requirement': [
            'AE 1770',
            'ARCH 4220',
            'BC 3630',
            'BMED 2400',
            'CEE 1770',
            'CHEM 1315',
            'CP 4510',
            'CS 1301',
            'CS 1315',
            'CS 1316',
            'CS 1331',
            'CS 1332',
            'CS 4235',
            'EAS 4430',
            'EAS 4610',
            'ECE 2030',
            'ID 3103',
            'ID 4103',
            'LMC 3402',
            'LMC 3410',
            'ME 1770',
            'ME 2016',
            'MGT 2200',
            'MGT 4051',
            'MGT 4058',
            'MGT 4052',
            'MUSI 4630',
            'PHYS 3266'
        ]
    },
    'Bachelor of Science in Applied Languages and Intercultural Studies - Chinese': {
        'ML Electives': lookup_abbr('CHIN', start=3000, end=4999)
    },
    'Bachelor of Science in Applied Languages and Intercultural Studies - French': {
        'ML Electives': lookup_abbr('FREN', start=3000, end=4999)
    },
    'Bachelor of Science in Applied Languages and Intercultural Studies - German': {
        'ML Electives': lookup_abbr('GRMN', start=3000, end=4999)
    },
    'Bachelor of Science in Applied Languages and Intercultural Studies - Japanese': {
        'ML Electives': lookup_abbr('JAPN', start=3000, end=4999)
    },
    'Bachelor of Science in Applied Languages and Intercultural Studies - Russian': {
        'ML Electives': lookup_abbr('RUSS', start=3000, end=4999)
    },
    'Bachelor of Science in Applied Languages and Intercultural Studies - Spanish': {
        'ML Electives': lookup_abbr('SPAN', start=3000, end=4999)
    },
    'BS in Applied Physics': {
        'Any PHYS or Technical Electives': [
            'BIOL 4478', 
            'CHEM 3411', 
            'CHEM 3412', 
            'CHEM 3511', 
            'EAS 2750', 
            'EAS 4300', 
            'EAS 4430', 
            'ECE 4501', 
            'MATH 2106', 
            'MATH 3215', 
            'MATH 3235', 
            'MATH 4320', 
            'MATH 4347', 
            'MATH 4348', 
            'MATH 4581', 
            'NRE 3301', 
            'NRE 4610'
        ] + lookup_abbr('PHYS', filter_degree='BS')
    },
    'BS in Biology': {
        'Biology Lab': [
            'BIOL 2336',
            'BIOL 2338',
            'BIOL 2345',
            'BIOL 2355',
            'BIOL 3451'
        ],
        'Biology Electives 3000-level or higher': lookup_abbr('BIOL', start=3000),
        'Biology Electives at 3000-level or higher': lookup_abbr('BIOL', start=3000)
    },
    'BS in Biomedical Engineering': {
        'BMED Depth Electives': [
            'BMED 2699'
        ] + lookup_abbr('BMED', start=3000, end=4999)
    },
    'BS in Business Administration': {
        'Non-MGT Electives': [
            '@any().remove(MGT, ACCT)'
        ]
    },
    'BS in Chemical and Biomolecular Engineering': {
        'CHBE Electives': [
            'CHBE 4020', 
            'CHBE 4310', 
            'CHBE 4535', 
            'CHBE 4752', 
            'CHBE 4757', 
            'CHBE 4760', 
            'CHBE 4763', 
            'CHBE 4764', 
            'CHBE 4765', 
            'CHBE 4770', 
            'CHBE 4775', 
            'CHBE 4776', 
            'CHBE 4791', 
            'CHBE 4793', 
            'CHBE 4794', 
            'CHBE 4803'
        ],
        '2000-level Technical Elective or higher': [
            'AE 4451', 
            'AE 4461', 
            'AE 4883', 
            'BMED 2400', 
            'BMED 3400', 
            'BMED 3510', 
            'BMED 4477', 
            'BMED 4751', 
            'BMED 4784', 
            'CEE 2040', 
            'CEE 2300', 
            'CEE 4300', 
            'CEE 4330', 
            'CEE 4620', 
            'CHBE 4020', 
            'CHBE 4310', 
            'CHBE 4535', 
            'CHBE 4752', 
            'CHBE 4757', 
            'CHBE 4763', 
            'CHBE 4764', 
            'CHBE 4765', 
            'CHBE 4770', 
            'CHBE 4775', 
            'CHBE 4776', 
            'CHBE 4791', 
            'CHBE 4793', 
            'CHBE 4794', 
            'CHBE 4803', 
            'CHBE 6120', 
            'CHBE 6794', 
            'COE 2001', 
            'COE 3001', 
            'COE 3002', 
            'ECE 2025', 
            'ECE 2030', 
            'ECE 2040', 
            'ECE 3025', 
            'ECE 3040', 
            'ECE 3065', 
            'ECE 3071', 
            'ECE 3080', 
            'ECE 3710', 
            'ECE 3741', 
            'ISYE 2027', 
            'ISYE 2028', 
            'ISYE 3025', 
            'ISYE 3039', 
            'ISYE 3133', 
            'ISYE 3232', 
            'ISYE 4803', 
            'ME 2202', 
            'ME 3057', 
            'ME 4011', 
            'MSE 2021', 
            'MSE 3002', 
            'MSE 4751', 
            'MSE 4803', 
            'NRE 3301', 
            'NRE 4328', 
            'NRE 4610', 
            'NRE 4803', 
            'NRE 6501'
        ],
        '3000-level Technical Elective or higher': [
            'AE 4451', 
            'AE 4461', 
            'AE 4883', 
            'BMED 2400', 
            'BMED 3400', 
            'BMED 3510', 
            'BMED 4477', 
            'BMED 4751', 
            'BMED 4784', 
            'CEE 2040', 
            'CEE 2300', 
            'CEE 4300', 
            'CEE 4330', 
            'CEE 4620', 
            'CHBE 4020', 
            'CHBE 4310', 
            'CHBE 4535', 
            'CHBE 4752', 
            'CHBE 4757', 
            'CHBE 4763', 
            'CHBE 4764', 
            'CHBE 4765', 
            'CHBE 4770', 
            'CHBE 4775', 
            'CHBE 4776', 
            'CHBE 4791', 
            'CHBE 4793', 
            'CHBE 4794', 
            'CHBE 4803', 
            'CHBE 6120', 
            'CHBE 6794', 
            'COE 2001', 
            'COE 3001', 
            'COE 3002', 
            'ECE 2025', 
            'ECE 2030', 
            'ECE 2040', 
            'ECE 3025', 
            'ECE 3040', 
            'ECE 3065', 
            'ECE 3071', 
            'ECE 3080', 
            'ECE 3710', 
            'ECE 3741', 
            'ISYE 2027', 
            'ISYE 2028', 
            'ISYE 3025', 
            'ISYE 3039', 
            'ISYE 3133', 
            'ISYE 3232', 
            'ISYE 4803', 
            'ME 2202', 
            'ME 3057', 
            'ME 4011', 
            'MSE 2021', 
            'MSE 3002', 
            'MSE 4751', 
            'MSE 4803', 
            'NRE 3301', 
            'NRE 4328', 
            'NRE 4610', 
            'NRE 4803', 
            'NRE 6501'
        ]
    },
    'BS in Chemistry': {
        'CHEM 4000- or 6000-level Electives': lookup_abbr('CHEM', start=4000, end=4999) + 
            lookup_abbr('CHEM', start=6000, end=6999),
        'Biochemistry Lab Elective': [
            'BIOL 3450', 
            'BIOL 3451', 
            'BIOL 3380', 
            'BIOL 3381', 
            'CHEM 4582'
        ],
        'CHEM 4000- or 6000-level': lookup_abbr('CHEM', start=4000, end=4999) + 
            lookup_abbr('CHEM', start=6000, end=6999),
        '3000-level Technical Electives': lookup_abbr('CHBE', start=3000, end=3999) + 
            lookup_abbr('MSE', start=3000, end=3999)
    },
    'BS in Civil Engineering': {
        'Ethics Requirement (Civil Engineering approved)': [
            'PHIL 3105', 
            'PHIL 3109', 
            'PHIL 3127'
        ],
        'CE Electives': [c for c in lookup_abbr('CEE', start=3000) 
                        if c not in ['CEE 4801', 'CEE 8811', 'CEE 8812']]
    },
    'BS in Computational Media': {
        'CM or Media Courses': [

        ],
        'CM or Literary Courses': [

        ],
        'CM or LMC Literary Courses': [

        ]
    },
    'BS in Computer Engineering': {
        'Science Elective': [
            'APPH 3751',
            'BIOL 1510', 
            'BIOL 1520', 
            'BIOL 3751', 
            'CHEM 1212K', 
            'CHEM 1315', 
            'EAS 1600', 
            'EAS 1601', 
            'EAS 2600', 
            'PHYS 2021', 
            'PHYS 2022', 
            'PHYS 2213'
        ],
        'Ethics Requirement': get_core_area('Ethics'),
        'Probability/Statistics': [
            'CEE 3770',
            'ISYE 3770',
            'MATH 3670',
            'ECE 3077'
        ],
        'Professional Communications': [
            'ECE 3005',
            'ECE 3006'
        ]
    },
    'BS in Electrical Engineering': {
        'Science Elective': [
            'APPH 3751',
            'BIOL 1510', 
            'BIOL 1520', 
            'BIOL 3751', 
            'CHEM 1212K', 
            'CHEM 1315', 
            'EAS 1600', 
            'EAS 1601', 
            'EAS 2600', 
            'PHYS 2021', 
            'PHYS 2022', 
            'PHYS 2213'
        ],
        'Ethics Requirement': get_core_area('Ethics'),
        'Probability/Statistics': [
            'CEE 3770',
            'ISYE 3770',
            'MATH 3670',
            'ECE 3077'
        ],
        'Professional Communications': [
            'ECE 3005',
            'ECE 3006'
        ]
    }
}

def export():
    import json
    with open('words.json', 'w') as f:
        json.dump(words, f)