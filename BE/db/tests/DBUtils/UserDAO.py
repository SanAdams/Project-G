import asyncio
from prisma import Prisma
import json
from pathlib import Path
from dotenv import load_dotenv

# UserDataTransferObject Definition:
# This class is meant to take in json serialized user data
# and creates a record for that user

class UserDAO:
    async def createUser(data) -> None:

        # self.create(self, data)
        # Load the env variables from the root directory
        env_path = Path(__file__).resolve().parents[4] / '.env'
        load_dotenv(dotenv_path=env_path)

        db = Prisma()
        await db.connect()

        datingappuser = await db.datingappuser.create(data)

        print(f'Created User: {datingappuser.model_dump_json(indent=2)}')

        await db.disconnect()
    
    async def deleteUser() -> None:
        pass


    