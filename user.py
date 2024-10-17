class User:
    name = ""
    surname = ""
    username = ""
    username_short = ""
    password = ""
    password_citrix = ""
    job_title = ""
    entity_number = ""
    data_start = ""
    oid = -1

    def __init__(self):
        pass
    '''
    def __init__(self, name, surname):
        self.name = name.strip()
        self.surname = surname.strip()
        self.username = self.name[0].lower() + "." + self.surname.lower() + "@maticagroup.com"
        self.username_short = self.name[0].lower() + "." + self.surname.lower()
    '''
    def print(self):
        print(self.name, self.surname, self.username, sep=", ")
