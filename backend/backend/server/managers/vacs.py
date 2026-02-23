from database import DB


class Vacs:
    vacs = DB.get_collection('vacs_cfo')

    @classmethod
    async def get_all(cls):
        vacs_db = cls.vacs.find()
        result = []
        async for vac_db in vacs_db:
            row = vac_db
            row['_id'] = str(row['_id'])
            # del row['_id']
            result.append(row)
        return result



