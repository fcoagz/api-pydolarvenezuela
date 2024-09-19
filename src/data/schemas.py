from flask_marshmallow import Marshmallow
from marshmallow import fields, pre_dump
from ..consts import TIME_ZONE

ma = Marshmallow()

class UserSchema(ma.Schema):
    created_at = fields.DateTime(format='%d/%m/%Y, %I:%M %p')

    @pre_dump
    def adjust_timezone(self, data, **kwargs):
        if data.created_at:
            data.create_at = data.last_update.astimezone(TIME_ZONE)
        return data
    class Meta:
        fields = ("id", "name", "token", "is_premium", "created_at")

class MonitorSchema(ma.Schema):
    last_update = fields.DateTime(format='%d/%m/%Y, %I:%M %p')

    @pre_dump
    def adjust_timezone(self, data, **kwargs):
        if data.last_update:
            data.last_update = data.last_update.astimezone(TIME_ZONE)
        return data
    class Meta:
        fields = ("key", "title", "price", "price_old", "last_update", "image", "percent", "change", "color", "symbol")

class HistoryPriceSchema(ma.Schema):
    last_update = fields.DateTime(format='%d/%m/%Y, %I:%M %p')

    @pre_dump
    def adjust_timezone(self, data, **kwargs):
        if data.last_update:
            data.last_update = data.last_update.astimezone(TIME_ZONE)
        return data
    class Meta:
        fields = ("price", "last_update")