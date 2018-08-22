from datetime import datetime

from app.models.user import User
from . import Van
from flask_mongoengine import MongoEngine

db = MongoEngine()


class Reply(db.Document):
    __tablename__ = 'replys'
    index = db.IntField(default=-1)  # 唯一ID
    floor = db.IntField(default=0)  # 回复的楼层，0代表楼主
    replyed_user = db.StringField(default='')  # 被回复的人
    content = db.StringField(default='')  # 回复的内容
    author = db.StringField(default='')  # 作者
    ct = db.DateTimeField(default=datetime.now)  # 信息创建时间
    block = db.BooleanField(default=False)  # 状态

    def __init__(self, *args, **kwargs):
        super(Reply, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<content:{}>'.format(self.content)

    def _set_index(self):
        self.index = Van.next_id(self.__class__.__name__)

    @classmethod
    def register(cls, *args, **kwargs):
        r = cls(*args, **kwargs)
        r._set_index()
        r.save()
        return r
