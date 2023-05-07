#%%
from functools import reduce


#%%
def multiply(*args):
    return reduce(lambda x, y: x*y, args)

s = multiply(4,6,7,8,4,3,2,343,567,7)
s
#%%
def first_true(iterable, default=False, pred=None):
    return next(filter(pred, iterable), default)

#%%

first_true(["y",5,7,10],default=False, pred=lambda x: x == 'y')

#%%
def starmap(func, iter: list[tuple]):
    for i in iter:
        yield func(*i)
    

combos = [(15,57),(68,2, 3, 4),(3,1)]

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