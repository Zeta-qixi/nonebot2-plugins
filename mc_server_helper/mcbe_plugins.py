from mcstatus import BedrockServer
from dataclasses import dataclass
from .ulits import mcbe_status


async def get_status(address):
    
    server = BedrockServer.lookup(address)
    mc = mcbe_status(address)
    try:
        status = await server.async_status()
        mc.running = True
        mc.version = status.version.version
    except:
        mc.running = False
        return mc
    

    if status:
         
        mc.online = int(status.players_online)
        return mc