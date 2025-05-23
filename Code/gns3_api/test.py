import gns3_actions
import httpx
import asyncio

async def main():
    await gns3_actions.aimport_project('192.168.57.133', '/home/diogo/Downloads/exercise.gns3project')

if __name__ == '__main__':
    asyncio.run(main())