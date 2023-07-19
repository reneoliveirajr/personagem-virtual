import asyncio
import atexit

from encerra import Encerra
from interface import Interface


async def run():
    interface = Interface()
    await interface.main()


if __name__ == '__main__':
    asyncio.run(run())
    atexit.register(Encerra.encerra)