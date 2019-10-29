import peewee

from .config import config
from .log import logger

db = peewee.SqliteDatabase(config.DB_PATH)


class SsrSub(peewee.Model):
    name = peewee.CharField(max_length=50)
    url = peewee.TextField()

    class Meta:
        database = db

    def __str__(self):
        return (
            'id: {}\n'
            'name: {}\n'
            'url: {}\n'
        ).format(self.id, self.name, self.url)


class SsrConf(peewee.Model):
    server = peewee.CharField(max_length=100)
    server_port = peewee.IntegerField()
    protocol = peewee.CharField(max_length=50)
    method = peewee.CharField(max_length=50)
    obfs = peewee.CharField(max_length=50)
    password = peewee.TextField()
    obfs_param = peewee.TextField()
    protocol_param = peewee.TextField()
    remarks = peewee.TextField()
    group = peewee.CharField(max_length=50)
    sub = peewee.ForeignKeyField(SsrSub, null=True, on_delete='CASCADE')

    class Meta:
        database = db

    def __str__(self):
        return (
            'id: {}\n'
            'remarks: {}\n'
            'group: {}\n'
        ).format(self.id, self.remarks, self.group)


try:
    db.connect()
except peewee.OperationalError:
    logger.critical('Can not open the database. Is the database folder created?')
    exit(1)
db.create_tables([SsrConf, SsrSub])
