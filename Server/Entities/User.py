import Patient

class User:
    name = ""
    surname = ""
    email = ""
    password = ""
    PatientsAssigned = []

    def __init__(self, name: str, surname: str, email: str, password: str):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password