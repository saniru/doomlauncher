class Port(object):
    """Handles parsing of port profiles"""

    def __init__(self, data):
        schema = ["rowid", "name", "path", "icon", "compat", "config"]
        self.data = data
        for count, ele in enumerate(data):
            setattr(self, schema[count], ele)

        self.compat = dict([i.split(":") for i in self.compat.splitlines()])
        self.config = self.config.splitlines()

    def __repr__(self):
        return f"<Port({self.data})>"

    def __str__(self):
        return f"{self.name.upper()}"

    def GetPortArgs(self, complevel):
        chosencompat = self.compat.get(complevel, self.compat["default"])
        # try:
        #     chosencompat = self.compat[complevel]
        # except KeyError:
        #     chosencompat = self.compat["default"]
        print(chosencompat)
        return " ".join([self.path, chosencompat, *self.config])
