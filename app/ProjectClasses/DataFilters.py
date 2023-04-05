from datetime import datetime

class DataFilters:

    @staticmethod
    def ISO_8601_reformatter(start_and_end_time: tuple) -> tuple[datetime,datetime]:
        sdate, stime = start_and_end_time[0].split('T')
        edate, etime = start_and_end_time[1].split('T')
        stime, _ = stime.split("-")
        etime, _ = etime.split("-")
        start_time = datetime.strptime(sdate+" "+stime, "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(edate+" "+etime, "%Y-%m-%d %H:%M:%S.%f")
        return (start_time, end_time)
    
    @staticmethod
    def _get_tupled_times(_data: dict) -> tuple:
        return _data["shift_start_and_end"]

    @staticmethod
    def _currently_working(tupled_times: tuple[datetime,datetime]) -> bool:
        now = datetime.now()
        return now > tupled_times[0] and now < tupled_times[1]

    @staticmethod
    def _paramedic(data:dict) -> bool:
        return data["rank_of_person"] == "FFP" or "EMTP" in data["profile_specialties"]       
        
    @staticmethod
    def _company_identifier(data:dict) -> str:
        return data["current_company"]
    
    @staticmethod
    def _company_abrev_first_two_letters(data:str):
        return data["current_company"][0:2]
        



class ALS(DataFilters):
    def __init__(self, data: dict) -> None:
        self.data = data
    
    def list_als_companies(self):
        """Mini Procotcal method for finding ALS companies in service"""
        
        als_dict = dict()
        for i, record in enumerate(self.data.values()):
            # gets tuple with string reprs of datetime from file
            t_times = self._get_tupled_times(record)
            # reformats ISO 8601 into datetime objects for further comparisems
            formatted_times = self.ISO_8601_reformatter(t_times)
            #performs check to see if recrods is within a certain timeframe
            on_duty = self._currently_working(formatted_times)
            # checks to see if record is == to a paramedic
            paramedic = self._paramedic(record)
            # Get the company CAD abrv
            comp = self._company_identifier(record)

            # Checking the dictionary for company abrv 
            if on_duty and paramedic:
                # retrieves a string repr of the fire companies abrv
                als_dict[comp] = {"ALS": True}
            else:
                ...
        return als_dict
    
