import peewee

from .config import config

db = peewee.SqliteDatabase(config.DB_URL)


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
    sub = peewee.ForeignKeyField(SsrSub, null=True)

    class Meta:
        database = db

    def __str__(self):
        return (
            'id: {}\n'
            'remarks: {}\n'
            'group: {}\n'
        ).format(self.id, self.remarks, self.group)


db.connect()
db.create_tables([SsrConf, SsrSub])
