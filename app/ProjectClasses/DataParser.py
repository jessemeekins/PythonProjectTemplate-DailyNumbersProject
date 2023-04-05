
class DataParser:
    def __init__(self, data, mapper:object, key_tag='Record') -> None:
        self.data = data
        self.mapper = mapper
        self.key = key_tag

    def xml_into_dictionary(self) -> dict:
        records_dict = dict()
        for i, child in enumerate(self.data.iter(self.key)):
            record = self.mapper.field_mapper(child)
            records_dict[i] = record
        return records_dict