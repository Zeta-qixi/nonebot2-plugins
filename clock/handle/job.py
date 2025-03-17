from abc import abstractmethod
from ..model import Clock
from ..database.database import DB
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import  Dict, Optional, List
from ..uilts import db_to_message, message_to_db
from nonebot import logger

class JobHandle:
    def __init__(self, db: DB, scheduler: AsyncIOScheduler):
        self.db = db
        self.scheduler = scheduler
        self._load_jobs_from_db()

    def _load_jobs_from_db(self):
        """从数据库加载所有任务并调度"""
        clocks = self.db.select_all()
        for clock in clocks:
            self.add_clock_to_scheduler(clock)

    def add_clock_to_scheduler(self, clock: Clock):
        """将单个时钟添加到调度器中"""
        if not clock.is_enabled:
            return

        trigger = CronTrigger.from_crontab(
            clock.cron_expression)
        
        self.scheduler.add_job(
            self._job_function,
            trigger=trigger,
            id=str(clock.id),
            args=[clock]
        )
        logger.info(f"Added job {clock.id} with cron {clock.cron_expression}")

    @abstractmethod
    async def _job_function(self, clock: Clock):
        """执行提醒任务的函数"""
        ...
        
    def remove_clock_from_scheduler(self, job_id: str):
        """从调度器中移除作业"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Removed job {job_id}")
        except Exception as e:
            logger.error(f"Failed to remove job {job_id}: {str(e)}")
            
    def db_to_message(self, msg):
        return db_to_message(msg)
    
    def message_to_db(self, msg):
        return message_to_db(msg)


def get_clock_by_owner(handle: JobHandle,  gid: str = '', uid: str = '') ->  List[Clock]:
    """获取提醒任务"""
    return handle.db.select_by_owner(uid, gid)

def del_clock(handle: JobHandle, clock: Clock):
    """删除提醒任务"""
    
    if not clock:
        logger.warning(f"Clock with ID {clock.id} does not exist")
        return False
    
    handle.remove_clock_from_scheduler(str(clock.id))
    handle.db.delete(clock.id)
    logger.info(f"Deleted clock with ID {id}")
    return True

def enabled_clock(handle: JobHandle, clock: Clock):
    """启用提醒任务"""

    if not clock.is_enabled:
        # 如果任务被禁用，重新启用并将其添加到调度器
        clock.is_enabled = True
        handle.db.update(clock)
        handle.add_clock_to_scheduler(clock)
        logger.info(f"Enabled clock with ID {id}")
    return True

def disable_clock(handle: JobHandle, clock: Clock):
    """禁用提醒任务"""
    
    if clock.is_enabled:
        # 如果任务被启用，禁用并从调度器中移除
        clock.is_enabled = False
        handle.db.update(clock)
        handle.remove_clock_from_scheduler(str(clock.id))
        logger.info(f"Disabled clock with ID {id}")
    return True

def add_clock(handle: JobHandle, **kwargs):
    """添加新的提醒任务"""
    # 创建一个新的Clock对象
    clock = Clock.from_dict(kwargs)

    handle.db.add(clock)
    
    if clock.id:
        logger.info(f"Added new clock with ID {clock.id}")
    
        handle.add_clock_to_scheduler(clock)
            
        return True
    
    logger.error("Failed to add new clock")
    return False

