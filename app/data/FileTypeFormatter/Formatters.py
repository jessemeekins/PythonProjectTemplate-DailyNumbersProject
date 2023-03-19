#%%
class XMLFormatterClass:
    def XML_file_name():
        from datetime import datetime, timedelta
        today = datetime.today() - timedelta(hours=7)
        formatted_time = datetime.strftime(today, "%Y-%m-%d")
        # Use For Prod
        file_name =  f"ROS11 MFD{formatted_time}.xml"
        return file_name
    
    def XML_importer(): 
        import xml.etree.ElementTree as ET
        tree = ET.parse("/Users/jessemeekins/Documents/XML_EXPORTS/ROS11 MFD2023-03-16.xml")
        root = tree.getroot()
        return root
    
    def XML_fields_mapper(record) -> dict:
        # Try/Except returns all data required or defaults to None type  
        try:
            # EID of employee 
            eid = record.find('RscEmployeeIDCh').text
            # Name of employee 
            name = record.find('RscMasterNameCh').text
            # Rank of employee 
            rank = record.find('PosJobAbrvCh').text
            # Position of employee in XML Record 1.0 denotes paramedic
            # Value can be changed in Person Formula ID Field in Person Profile Settings under skill. 
            # EMT-P -> 1.1, EMT-A -> 1.2, EMT-B -> 1.3 
            # Current Testing is using 1.0
            try:
                # RscFormulaID maps back to Telestaff Person Formula ID, this will give license level
                position = record.find('RscFormulaIDCh').text
            except:
                # if RscFormulaID isnt available, Pull PosFormulaID -> Nozzle, Hookup ect.
                position = record.find('PosFormulaIDCh').text
            paycode = record.find('WstatAbrvCh').text
            # Unit abreviation 
            comp = record.find('PUnitAbrvCh').text
            # Start date and time 
            start = record.find('StaffingStartDt').text
            # End date and time 
            end = record.find('ShiftEndDt').text
            # Return a dictionary to be later added to the class dictionary self.personnelDict
            data = {'EID':eid, 'NAME':name, 'RANK':rank, 'POSITION':position, 'PAYCODE': paycode, 'COMP':comp, 'START':start, 'END': end}

            return data
        
        # If any values are not found or errors in parsing required data, 
        # program will continue collecting data without crashing.
        # Excpetion will be caught as variabble "e" as logged in log file
        except Exception as e:
            # Logging error to log file
            #print(e)
            # Returning Nonetype, record will not be added to class dict
            return None


class XLSXFormatterClass:
    def XLSX_importer() -> str:
        from datetime import datetime, timedelta
        today = datetime.today() - timedelta(hours=7)
        formatted_time = datetime.strftime(today, "%Y-%m-%d")
        return f"ROS11 MFD{formatted_time}.xlsx"

