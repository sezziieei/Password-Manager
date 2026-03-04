class PasswordEntry:
    def __init__(self, website, username, password):
        self.website = website
        self.username = username
        self.password = password

    def __str__(self):
        return f"Website: {self.website}, Username: {self.username}"