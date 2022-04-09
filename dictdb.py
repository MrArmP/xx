from json import dumps, loads
from json.decoder import JSONDecodeError
from os.path import exists
from os import remove, chdir
from os.path import dirname, abspath
p = dirname(abspath(__file__)); chdir(p)
class db:
    def __init__(self, dbName: str):
        self.dbName = f"{dbName}.json"
        self.mydb = {}
        try:
            self.mydb = loads(open(self.dbName, "r").read()) if exists(self.dbName) else {} 
        except JSONDecodeError:
            pass
    def set_data(self, where, data):
        self.mydb[str(where)] = data
        return True
    def set_data_save(self, where, data):
        self.mydb[str(where)] = data
        self.save_all()
        return True
    def get_data(self, where):
        if self.checkExist(where):
            try:
                return self.mydb[str(where)]
            except KeyError:
                return True
        else:
            return True
    def checkExist(self, where):
        try:
            if self.mydb[str(where)]:
                return True
        except KeyError:
            return False
    def save_all(self):
        with open(self.dbName, "w") as w:
            w.write(dumps(self.mydb, indent=4))
            w.close()
    def del_data(self, where):
        del self.mydb[str(where)]
    def del_data_save(self, where):
        del self.mydb[str(where)]
    def reset(self):
        try:
            self.mydb = {}
            remove(self.dbName)
        except FileNotFoundError:
            return False
    def data_is(self, where, data):
        if self.checkExist(where):
            try:
                if self.mydb[str(where)] == data:
                    return True
            except KeyError:
                return False
        else:
            return False
class listdb:
    def __init__(self, dbName):
        self.dbName = f"{dbName}.json"
        self.mydb = loads(open(self.dbName, "r").read()) if exists(self.dbName) else {} 
    def save(self):
        with open(self.dbName, "w") as w:
            w.write(dumps(self.mydb, indent=4))
    def add_list(self, where):
        try:
            self.mydb[str(where)]
        except KeyError:
            self.mydb[str(where)] = []
        self.save()
    def add_element(self ,where ,data):
        self.mydb[str(where)].append(data) if data not in self.mydb[str(where)] else None
        self.save()
    def get_elemenet(self, where):
        try:
            return self.mydb[str(where)]
        except KeyError:
            return False