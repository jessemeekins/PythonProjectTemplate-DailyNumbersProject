#%%
# XML files prefixes and extensions 

def XML_importer() -> str:
    from datetime import datetime, timedelta
    today = datetime.today() - timedelta(hours=7)
    formatted_time = datetime.strftime(today, "%Y-%m-%d")
    return f"ROS11 MFD{formatted_time}.xml"


def XLSX_importer() -> str:
    from datetime import datetime, timedelta
    today = datetime.today() - timedelta(hours=7)
    formatted_time = datetime.strftime(today, "%Y-%m-%d")
    return f"ROS11 MFD{formatted_time}.xlsx"

