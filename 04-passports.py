from assets.config import USER_SESSION_ID
from requests import get
import re

response = get('https://adventofcode.com/2020/day/4/input', cookies={'session': USER_SESSION_ID})
if response.ok:
    with open('assets/04-input.txt', 'w') as f:
        f.write(response.text)

with open('assets/04-input.txt', 'r') as f:
    mass = f.read()
    passlists = [re.split(r'\s', p) for p in mass.split('\n\n')]

passports = list()
for l in passlists:
    d = dict()
    for pair in l:
        kvp = re.split(':', pair, maxsplit=2)
        try:
            d.update({kvp[0]: kvp[1]})
        except IndexError:
            pass
    passports.append(d)

fields = [
    'byr',  #(Birth Year)
    'iyr',  #(Issue Year)
    'eyr',  #(Expiration Year)
    'hgt',  #(Height)
    'hcl',  #(Hair Color)
    'ecl',  #(Eye Color)
    'pid',  #(Passport ID)
    'cid'  #(Country ID)
]

### Part 1 ###
required_fields = fields.copy()
required_fields.remove('cid')
valid_passports = [p for p in passports
                   if set(required_fields).issubset(p.keys())]

print(f'{len(valid_passports):,} are valid of {len(passports):,}.')

### Part 2 ###
def validate_hgt(hgt: str) -> bool:
    match = re.match(r'([0-9]{1,3})(cm|in)$', hgt)
    try:
        lower = {'cm': 150, 'in': 59}
        upper = {'cm': 193, 'in': 76}
        h = int(match[1])
        unit = match[2]
        return lower[unit] <= h <= upper[unit]
    except (ValueError, IndexError, TypeError):
        return False

def validate(p: dict) -> bool:
    if not set(required_fields).issubset(p.keys()):
        return False
    validators = {
        'byr': lambda y: 1920 <= int(y) <= 2002,
        'iyr': lambda y: 2010 <= int(y) <= 2020,
        'eyr': lambda y: 2020 <= int(y) <= 2030,
        'hgt': lambda h: validate_hgt(h),
        'hcl': lambda c: re.match(r'#[0-9a-f]{6}$', c) is not None,
        'ecl': lambda c: c in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid': lambda i: re.match(r'[0-9]{9}$', i) is not None,
        'cid': lambda i: True
    }
    try:
        return all([validators[k](v) for k,v in p.items()])
    except TypeError:
        return False

checks = [validate(p) for p in passports]
print(f'{sum(checks):,} of {len(passports):,} passed checks.')
