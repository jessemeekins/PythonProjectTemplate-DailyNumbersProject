#%%

import time
from functools import wraps

def retry(CheckException, tries=4, delay=3, backoff=2, logger=None):
    def d_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            if mtries >1:
                try:
                    return f(*args, **kwargs)
                except CheckException as e:
                    msg = f"{str(e)}, retrying in {mdelay} seconds..." 
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                time.sleep(mdelay)
                mtries -= 1 
                mdelay *= backoff
                return f(*args, **kwargs)
            else:
                pass
        return f_retry
    return d_retry
