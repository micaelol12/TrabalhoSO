from Enums import Coluna


class Column:
    Id:Coluna = None
    Name:str = None
    Width:int = None
    ProcessAtribute:str = None
    
    def __init__(self,id,name,width,attribute):
        self.Id = id
        self.Name = name
        self.Width = width
        self.ProcessAtribute = attribute