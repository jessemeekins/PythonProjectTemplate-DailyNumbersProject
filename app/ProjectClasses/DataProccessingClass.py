from ProjectClasses.DateAndTimeClass import DateTimeFormatter

class DataParser:
    def __init__(self, data:dict, mapper:object) -> None:
        self.data = data
        self.mapper = mapper
    
    def package(self, file_root_tag='Record') -> dict:
        records_dict = dict()
        for i, child in enumerate(self.data.iter(file_root_tag)):
            record = self.mapper.field_mapper(child)
            records_dict[i] = record
        return records_dict

class DataProccessing:
    def __init__(self, dictionary: dict) -> None:
        self.data = dictionary

    @staticmethod
    def _on_duty_checker(start_and_end_time: tuple) -> bool:
        return DateTimeFormatter.currently_working(start_and_end_time)

    def _currently_on_duty(self) -> dict:
        return filter(lambda x: self._on_duty_checker(x["shift_start_and_end"]), self.data.values())


    def _on_duty_paramedics(self, filtred:dict) -> list:
        paramedic_records = filter(lambda x: x["rank_of_person"] == 'FFP' or "EMTP" in x["profile_specialties"], filtred.values())        
        return list(paramedic_records)

    def _paramedic_locations(self, paramdics_list:list) -> list:
        als_companies = list(map(lambda x: x["current_company"], filter(lambda x: x["current_company"], paramdics_list)))
        return list(als_companies)

    def list_als_companies(self) -> list:
        on_duty = self._currently_on_duty()
        medics = self._on_duty_paramedics(on_duty)
        loc = self._paramedic_locations(medics)
        return loc

        
        ...



    #   records = list(filter(lambda x: "BC0" not in x, filter(lambda x: "EU0" not in x, ALS_record)))
    #   ALS_record = list(map(lambda x: x["current_company"] ,filter(lambda x: 'EMTP' in x["profile_specialties"], self.data.values())))