#%%
"""
Copyright (c) 2023 Jesse Meekins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import itertools
from DateAndTimeClass import DateTimeFormatter

def even(x) -> bool:
    return x%2==0 

def multiply(x, y):
    return x*y


def first_true(iterable, default=False, pred=None):
    return next(filter(pred, iterable), default)

#%%
first_true(["y",5,7,10],default=False, pred=lambda x: x == 'y')

#%%
def starmap(func, iter: list[tuple]):
    for i in iter:
        yield func(*i)
        
        
        

combos = [(15,57),(68,2)]

x = starmap(multiply,combos)

list(x)

#%%
try:
    working = DateTimeFormatter.currently_working(mapped_record["START"], mapped_record["END"])
    if working:
        records_dict[mapped_record["EID"]] = mapped_record
except:
    pass

def first_true(iterable, default=False, pred=None):
    return next(filter(pred, iterable), default)

#   records = list(filter(lambda x: "BC0" not in x, filter(lambda x: "EU0" not in x, ALS_record)))
#   ALS_record = list(map(lambda x: x["current_company"] ,filter(lambda x: 'EMTP' in x["profile_specialties"], self.data.values())))