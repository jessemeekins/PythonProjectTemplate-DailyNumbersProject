#%%


class FilePathBuilder:

    configuration = {
        "PAR" : ('local', 'ROS11'),
        "STAFF": ('network', "ROS12"),
        "WEB": ('web', "ROS13"),
        "ALS": ("local", "ROS12")
    }
    file_source = {
        'local': '/Users/jessemeekins/Documents/XML_EXPORTS/',
        'network': '/usr/bin/files/exports/',
        'web': 'https://192.168.1.244:5000'    
    }
    file_name = {
        'ROS11': 'ROS11 MFD2023-10-02.xml',
        'ROS12': 'ROS12 MFD2023-10-11.xml',
        'ROS13': 'ROS13 MFD2023-10-11.xml'
    }
    def __init__(self, config: tuple) -> None:
        self.config = config
        
    def file_path_formatter(self) -> str:
        conf = self.configuration.get(self.config, '')
        path = self.file_source.get(conf[0], '')
        name = self.file_name.get(conf[1], '')
        
        return f"{path}{name}"
  
    

class TelestaffFilePathFormatter(FilePathBuilder):
    def __init__(self, config) -> None:
        super().__init__(config)

report1 = TelestaffFilePathFormatter("PAR").file_path_formatter()
report2 = TelestaffFilePathFormatter("STAFF").file_path_formatter()
report3 = TelestaffFilePathFormatter("ALS").file_path_formatter()

print(report1)
print(report2)
print(report3)
        


    
