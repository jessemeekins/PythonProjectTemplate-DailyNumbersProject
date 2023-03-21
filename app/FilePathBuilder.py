#%%
class FilePathBuilder:

    configuration = {
        "PAR" : {"path":'local', "file":'ROS11', "debug": True},
        "STAFF": {"path":'network', "file":'ROS12', "debug": False},
        "WEB": {"path":'web', "file":'ROS13'},
        "ALS": {"path":'local', "file":'ROS12'}
    }
    file_source = {
        'local': '/Users/jessemeekins/Documents/XML_EXPORTS/',
        'network': '/usr/bin/files/exports/',
        'web': 'https://192.168.1.244:5000/'    
    }
    file_name = {
        'ROS11': 'ROS11 MFD2023-10-02.xml',
        'ROS12': 'ROS12 MFD2023-10-11.xml',
        'ROS13': 'ROS13 MFD2023-10-11.xml'
    }

    def __init__(self, config: str) -> None:
        self.config = config
            
    def get_filepath(self) -> str:
        conf = self.configuration.get(self.config, '')
        path = self.file_source.get(conf["path"], '')
        name = self.file_name.get(conf["file"], '')
        return f"{path}{name}"
    
    def debug(self) -> bool:
        conf = self.configuration.get(self.config, '')
        debug = conf.get("debug", True)
        return debug
  

class TelestaffFilePathBuilder(FilePathBuilder):
    def __init__(self, config: str) -> None:
        super().__init__(config)
    






    
