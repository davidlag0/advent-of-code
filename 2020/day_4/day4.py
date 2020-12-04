#!/usr/bin/env python3

# Advent of Code 2020, Day 4
import re

height_cm_pattern = re.compile(r'(\d{3})cm')
height_in_pattern = re.compile(r'(\d{2})in')
hair_color_pattern = re.compile(r'\#[0-9a-f]{6}')
passport_id_pattern = re.compile(r'\d{9}')

def get_passport_dict(key_value_line):
    return dict([kv.split(':') for kv in key_value_line.strip().split(' ')])

def is_valid_passport(passport, validate_fields=False):
    if validate_fields:
        if 'hgt' in passport:
            match_height_cm = re.match(height_cm_pattern, passport['hgt'])
            match_height_in = re.match(height_in_pattern, passport['hgt'])
            
        if not (('byr' in passport) and (1920 <= int(passport['byr']) <= 2002) and
            ('iyr' in passport) and (2010 <= int(passport['iyr']) <= 2020) and
            ('eyr' in passport) and (2020 <= int(passport['eyr']) <= 2030) and
            ((('hgt' in passport) and match_height_cm and (150 <= int(match_height_cm.group(1)) <= 193)) or
                (('hgt' in passport) and match_height_in and (59 <= int(match_height_in.group(1)) <= 76))) and
            ('hcl' in passport) and (re.match(hair_color_pattern, passport['hcl'])) and
            ('ecl' in passport) and (passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']) and
            ('pid' in passport) and (len(passport['pid']) == 9) and (re.match(passport_id_pattern, passport['pid']))):
            return False
        
    return ((len(passport) == 8) and ('cid' in passport)) or ((len(passport) == 7) and ('cid' not in passport))

def validate_passports(filename, validate_fields=False):
    valid_passports = 0
    
    with open(filename, 'r') as input:
        current_passport = {}
        
        for line in input:
            if len(line.strip()) > 0:
                current_passport.update(get_passport_dict(line))
            else:
                if current_passport:
                    if (is_valid_passport(current_passport, validate_fields)):
                        valid_passports += 1
                    current_passport = {}
        
        # Required for the last passport as we cannot know in advance whether the current
        # line is the last or not.
        if current_passport:
            if (is_valid_passport(current_passport, validate_fields)):
                valid_passports += 1            
            current_passport = {}
            
    return valid_passports

if __name__ == '__main__':
    print(f"Part 1: {validate_passports('day_4_input')}")
    print(f"Part 2: {validate_passports('day_4_input', validate_fields=True)}")
