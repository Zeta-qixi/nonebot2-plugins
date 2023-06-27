from mcstatus import JavaServer
from .ulits import mcje_status


async def get_status(address):
    
    server = JavaServer.lookup(address)
    mc = mcje_status(address)
    try:
        server.ping()
    except:
        mc.running = False
        return mc
    
    status = await server.async_status()
    mc.running = True
    if status:
        
        mc.version = status.version.name
        mc.online = int(status.players.online)
        if mc.online:
            mc.player_list += [i.name for i in status.players.sample]
            
        return mc