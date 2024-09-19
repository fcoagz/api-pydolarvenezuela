from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()

class UserSchema(ma.Schema):
    created_at = fields.DateTime(format='%d/%m/%Y, %I:%M %p')
    class Meta:
        fields = ("id", "name", "token", "is_premium", "created_at")

class MonitorSchema(ma.Schema):
    last_update = fields.DateTime(format='%d/%m/%Y, %I:%M %p')
    class Meta:
        fields = ("key", "title", "price", "price_old", "last_update", "image", "percent", "change", "color", "symbol")

class HistoryPriceSchema(ma.Schema):
    last_update = fields.DateTime(format='%d/%m/%Y, %I:%M %p')
    class Meta:
        fields = ("price", "last_update")