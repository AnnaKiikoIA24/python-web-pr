# Користувач
class User:  
    id: int
    login: str
    password: str
    firstName: str
    lastName: str
    role: bool
    idGroup: int
    name: str

    def __init__(id, login, password, firstName, lastName, role, idGroup):
        self.id = id
        self.login = login
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.role = role
        self.idGroup = idGroup
    
    def __init__(id, login, password, firstName, lastName, role, idGroup, nameGroup):
        self.id = id
        self.login = login
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.role = role
        self.idGroup = idGroup
        self.name = nameGroup