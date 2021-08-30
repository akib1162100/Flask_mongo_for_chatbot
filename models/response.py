from dataclasses import dataclass
@dataclass
class Response:
    status : int
    data : str
    message : str
    
    # def __init__(self, status, data, message):
    #     self.status = status
    #     self.data = data
    #     self.message = message
    