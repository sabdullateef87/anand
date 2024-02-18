import json
class UserResponse:
    def __init__(self, email, first_name, last_name) -> None:
        self.email=email
        self.first_name=first_name
        self.last_name=last_name

    def json(self):
        return self.__dict__
    
    def __str__(self) -> str:
        return f'{self.first_name} - {self.last_name}'