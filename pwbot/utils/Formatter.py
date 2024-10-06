class Formatter:
    def __init__(self):
        pass

    def alreadyRegistered(self):
        return f"You have already registered your nation!"

    def alreadyRegisteredAdmin(self, user):
        return f"{user.display_name} has already been registered!"

    def registrationSuccessful(self, aa, query):
        if aa == "vyo" or aa == 13111 or aa == "valyrian order":
            return f"{query.getName()} has been successfully registered to Valyrian Order"
        elif aa == "vg" or aa == 13173 or aa == "varangian guard":
            return f"{query.getName()} has been successfully registered to Varangian Guard"