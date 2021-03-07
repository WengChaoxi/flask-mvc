
def db_connecter():
    print('[定时任务]：数据库活动 TODO')

class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'db_connect_job',
            'func': 'jobs.timer:db_connecter',
            'args': None,
            'trigger': 'interval',
            'seconds': 5*3600
        }
    ]
