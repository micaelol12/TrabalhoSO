class Column:
    Id = None
    Name = None
    Width = None
    ProcessAtribue = None
    
    def __init__(self,id,name,width,attribute):
        self.Id = id
        self.Name = name
        self.Width = width
        self.ProcessAtribue = attribute