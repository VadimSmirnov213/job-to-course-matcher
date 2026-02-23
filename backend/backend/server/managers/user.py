from database import DB


class User:
    users = DB.get_collection('users_cfo')

    @staticmethod
    def helper(coroutine):
        result = {
            'login': coroutine['login'],
        }
        return

    def __init__(self, login: str, parameters: dict = None):
        self._id = login
        self.password = parameters['password']

        if parameters:
            for key in parameters:
                self.__dict__[key] = parameters[key]

    def __setattr__(self, key, value):
        if key == '_id':
            if type(value) is not str:
                raise ValueError('The id parameter must be an string')
        super().__setattr__(key, value)

    @classmethod
    async def get(cls, login):
        user_dict = await cls.users.find_one({'_id': login})

        if not user_dict:
            return None
        return cls(login=login, parameters=user_dict)

    async def add(self):
        await self.users.insert_one(self.__dict__)
        print()

    async def update(self, parameters: dict):
        self.__dict__.update(parameters)

        await self.users.update_one({'_id': self._id}, {'$set': self.__dict__})

    async def delete(self):
        await self.users.delete_one({'_id': self._id})

    async def response(self):
        data = self.__dict__
        data.pop('password')
        return data

    @classmethod
    async def login(cls, login: str, password: str):
        user: User = await cls.get(login)
        if user.password == password:
            return user
        return None
