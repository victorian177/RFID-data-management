import json
import numpy
import os
import pandas
import datetime


class ID:
    """
    Super class containing general ID functionalities:

    name -> name of the facility that is using the ID functionalities
    info -> dictionary containing the data that is entered during registration (id and rfid info is specified already)
    cat_info -> specifies what data is entered into the 'info' fields that are specified as categorical
    """

    # specifies the types of data that can entered into for ID pandas dataframe
    TYPES = {
        "obj": object,
        "int": "Int64",
        "flt": numpy.float64,
        "cat": "category"
    }

    def __init__(self, name, info={}, cat_info={}) -> None:
        self.name = name        
        try:
            os.mkdir(f"{self.name}")
        except FileExistsError:
            pass
        self.data, self.cat_data = self.data_manager(info=info, cat_info=cat_info)

    def data_manager(self, info, cat_info):
        """
        Stores the info field in relevant files:
        
        data -> contains the ids and their requisite information
        metadata -> contains the data names and data types
        cat_data -> contains the data names with categorical data types and the information to be expected from them
        """
        common_info = {"id": "obj", "rfid": 'obj'}
        try:
            with open(f"{self.name}/{self.name}_metadata.json", 'r') as meta_file:
                metadata = json.load(meta_file)
        except FileNotFoundError:
            inf = list(common_info.keys()) + list(info.keys())
            data = pandas.DataFrame(columns=inf)
            data.set_index("id", inplace=True)
            data.to_csv(f"{self.name}/{self.name}_data.csv")

            with open(f"{self.name}/{self.name}_metadata.json", 'w') as meta_file:
                metadata = {**common_info, **info}
                json.dump(metadata, meta_file)
            
            with open(f"{self.name}/{self.name}_catdata.json", 'w') as cat_file:
                cat_data = cat_info
                json.dump(cat_data, cat_file)

        else:
            metadata = {i: ID.TYPES[metadata[i]] for i in metadata}
            data = pandas.DataFrame(pandas.read_csv(f"{self.name}/{self.name}_data.csv", dtype=metadata))
            data.set_index("id", inplace=True)
            with open(f"{self.name}/{self.name}_catdata.json", 'r') as cat_file:
                cat_data = json.load(cat_file)

        return data, cat_data

    def register(self, args):
        """Recieves a list containing the information and creates a new slot to store the data if data does not exist"""
        try:
            self.data.loc[args[0]]
        except KeyError:
            self.data.loc[args[0]] = args[1:]
            self.data.to_csv(f"{self.name}/{self.name}_data.csv")
        else:
            print("ID already exists.")            

    def remove(self, indx):
        """Removes an id from the data"""
        self.data.drop(index=indx, inplace=True, errors="ignore")
        self.data.to_csv(f"{self.name}/{self.name}_data.csv")

    def identifier(self, idntfr):
        """Returns whether or not an ID exists inside a database or not"""
        try:
            self.data.loc[idntfr]
        except KeyError:
            return False
        else:
            return True


class Access(ID):

    """Based on your ID registration data"""
    def __init__(self, name, info={}, cat_info={}, places="") -> None:
        super().__init__(name, info, cat_info)
        self.accss_plcs = self.access_places(places)
        self.access_data = self.access_data_manager()

    def access_places(self, places=""):
        try:
            with open(f"{self.name}/{self.name}_access_places.txt", 'r') as access_file:
                access_places = list(access_file.read().split())
        except FileNotFoundError:
            with open(f"{self.name}/{self.name}_access_places.txt", 'w') as access_file:
                access_places = places
                access_file.write(access_places)
        return access_places

    def access_data_manager(self):
        try:
            with open(f"{self.name}/{self.name}_access_data.json", 'r') as access_file:
                access_data = json.load(access_file)
        except FileNotFoundError:
            with open(f"{self.name}/{self.name}_access_data.json", 'w') as access_file:
                access_data = {}
                json.dump(access_data, access_file)
        return access_data

    def register(self, args, place_data):
        super().register(args)
        self.access_editor(idntfr=args[0], place_data=place_data, edit=False)

    def access_editor(self, idntfr, place_data, edit=True):
        if edit:
            try:
                self.access_data[idntfr]
            except KeyError:
                print('ID does not exist in database.')
            else:
                self.access_data[idntfr] = place_data.split()
        else:
            self.access_data[idntfr] = place_data.split()

        with open(f"{self.name}/{self.name}_access_data.json", 'w') as access_file:
            json.dump(self.access_data, access_file)

    def access_checkr(self, idntfr, place):
        if place in self.access_data[idntfr]:
            return True
        return False

    def remove(self, idntfr):
        super().remove(idntfr)
        self.access_data.pop(idntfr)
        with open(f"{self.name}/{self.name}_access_data.json", 'w') as access_file:
            json.dump(self.access_data, access_file)

        
class Attendance(ID):
    def __init__(self, name, info={}, cat_info={}) -> None:
        super().__init__(name, info, cat_info)
        self.attend_data = self.attendance_data_manager()

    def attendance_data_manager(self):
        try:
            attend_data = pandas.DataFrame(pandas.read_csv(f"{self.name}/{self.name}_attend_data.csv"))
        except FileNotFoundError:
            attend_data = pandas.DataFrame(columns=["time", "id", "en_ex"])
            attend_data["time"] = pandas.to_datetime(attend_data["time"])
            attend_data["en_ex"] = attend_data["en_ex"].astype('category')
            attend_data.set_index('time', inplace=True)
            attend_data.to_csv(f"{self.name}/{self.name}_attend_data.csv")
        else:
            attend_data["time"] = pandas.to_datetime(attend_data["time"])
            attend_data["en_ex"] = attend_data["en_ex"].astype('category')
            attend_data.set_index('time', inplace=True)

        return attend_data
    
    def attendance_logger(self, idntfr):
        if self.attend_data[self.attend_data['id'] == idntfr].empty:
            self.attend_data.loc[pandas.Timestamp(datetime.datetime.now())] = [idntfr, 'en']
        else:
            if self.attend_data[self.attend_data['id'] == idntfr].iloc[-1]['en_ex'] == 'ex':
                self.attend_data.loc[pandas.Timestamp(datetime.datetime.now())] = [idntfr, 'en']
            else:
                self.attend_data.loc[pandas.Timestamp(datetime.datetime.now())] = [idntfr, 'ex']
        self.attend_data.to_csv(f"{self.name}/{self.name}_attend_data.csv")

class Record(ID):
    def __init__(self, name, info={}, cat_info={}) -> None:
        super().__init__(name, info, cat_info)
        try:
            os.mkdir(f"{self.name}/{self.name}_records")
        except FileExistsError:
            pass
        self.record_data = self.record_data_manager()

    def record_data_manager(self):
        try:
            record_data = pandas.DataFrame(pandas.read_csv(f"{self.name}/{self.name}_record_data.csv"))
        except FileNotFoundError:
            record_data = pandas.DataFrame(columns=["id", "id_files"])
            record_data.set_index("id", inplace=True)
            record_data.to_csv(f"{self.name}/{self.name}_record_data.csv")
        else:
            record_data.set_index("id", inplace=True)
    
        return record_data

    def register(self, args):
        super().register(args)
        self.record_data.loc[args[0]] = [f'{self.name}/{self.name}_records/{args[0]}.txt']
        self.record_data.to_csv(f"{self.name}/{self.name}_record_data.csv")
        self.record_editor(args[0], ': Created id file.')

    def record_editor(self, idntfr, id_data):
        try:
            self.record_data.loc[idntfr]
        except KeyError:
            pass
        else:
            try:
                with open(f"{self.record_data.loc[idntfr, 'id_files']}", 'r') as file:
                    file.read()
            except FileNotFoundError:
                with open(f"{self.record_data.loc[idntfr, 'id_files']}", 'w') as file:
                    file.write(datetime.datetime.today().strftime("%Y-%m-%d %H:%M"))
                    file.write(id_data)
            else:
                with open(f"{self.record_data.loc[idntfr, 'id_files']}", 'a') as file:
                    file.write(datetime.datetime.today().strftime("%Y-%m-%d %H:%M"))
                    file.write(id_data)

