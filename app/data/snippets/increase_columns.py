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
