from .data_loader import DataLoader

class Push:
    def __init__(self, path):
        self.helper = DataLoader(path)

    def del_manga(self, user, manga):
        ...

    def add_manga(self, user, manga):
        self.helper.data[user][manga] = 0

    def get_response(self):
        ...