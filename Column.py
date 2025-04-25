class Column:
    Id = None
    Name = None
    Width = None
    ProcessAtribute = None
    
    def __init__(self,id,name,width,attribute):
        self.Id = id
        self.Name = name
        self.Width = width
        self.ProcessAtribute = attribute