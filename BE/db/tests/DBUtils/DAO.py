import asyncio
from prisma import Prisma
import json
from pathlib import Path
from dotenv import load_dotenv

class DAO:
    env_path: str
    def __init__(self):
        db = Prisma()
    async def transfer(data):
        