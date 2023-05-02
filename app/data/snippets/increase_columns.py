#%%
import string

num = 15

companies = {"B1": {"PU001", "PU002", "PU005", "PU007"}, "B2": {"PU004", "PU0015"}}

start_letter = 'I'
start_index = ord(start_letter) - ord('A')

for company in companies.values():
    new_comp = list(company)
    for i, letter in enumerate(string.ascii_uppercase[start_index:start_index+len(company)]):
        print(f"['{letter}{num}'] = {new_comp[i]}")
    num += 1

import re

string = "ASH,CPR,DL,EMTP,ENG,PU046,TRKRM"

matches = re.findall(r'\b[A-Z]{2}\d{3}\b', string)

if matches:
    print(matches[0])
else:
    print("Match not found.")