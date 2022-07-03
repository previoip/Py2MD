class TokenContainer:
    def __init__(self):
        self.__ids = []
        self.__names = []
        self.__tokens = []

    def appendItem(self, id, name, token):
        self.__ids.append(id)
        self.__names.append(name)
        self.__tokens.append(token)

    def getById(self, id):
        index = self.__ids.index(id)
        return self.__tokens[index]
    
    def getIds(self):
        return self.__ids.copy()

    def getNames(self):
        return self.__names.copy()

class Token:
    def __init__(self, Container: 'TokenContainer', id: str, name: str, isinline: bool, \
            fn: 'Function', accepts_param=False, param_type=None, param_len=1):
        self.__Container = Container
        self.id = id
        self.name = name
        self.isinline = isinline
        self.__Container.appendItem(id, name, self)
        self.fn = fn
        self.accepts_param = accepts_param
        self.param_type = param_type
        self.param_len = param_len


    def __repr__(self):
        # return f'<{self.name} accepts_param={self.accepts_param} param_type={str(self.param_type)} \>'
        return f'<{self.name}\>'

    def opt_param(self, acceptsParam, paramtype=None):
        self.accepts_param = acceptsParam
        if acceptsParam:
            self.param_type = paramtype


