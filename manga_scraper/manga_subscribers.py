import sqlite3
from .database import database_file
from nonebot.adapters.onebot.v11.bot import Bot


def get_updates_and_subscribers(conn):
    
    cursor = conn.cursor()
    # Get all mangas with update_flag = 1
    cursor.execute("""
        SELECT m.url, m.title, m.last_update, u.uid, u.provider
        FROM manga m
        JOIN user_subscriptions u ON  m.url = u.manga_url
        WHERE m.update_flag = 1
    """)
    
    return cursor.fetchall()


def reset_update_flag(conn, manga_url):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE manga
        SET update_flag = 0
        WHERE url = ?
    """, (manga_url,))
    conn.commit()
    

async def send_msg_notification(bot: Bot, url, title, last_update , id, provider):
    
    msg = f"{title}: {last_update}\n{url}"
    if provider == 'private':
        await bot.send_private_msg(user_id=int(id), message=msg)
    elif provider == 'group':
        await bot.send_group_msg(int(id), message=msg)
    
    
    
async def auto_notify(bot: Bot):
    conn = sqlite3.connect(database_file)
    updates = get_updates_and_subscribers(conn)
    
    if not updates:
        print("No updates to notify.")
        conn.close()
        return
    
    for update in updates:
        
        await send_msg_notification(bot, *update)
        reset_update_flag(conn, update[0])  # Reset update flag after notifying
    
    conn.close()
