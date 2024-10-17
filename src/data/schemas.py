from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow import fields, pre_dump
from ..consts import TIME_ZONE
ma = Marshmallow()

class BaseSchema(ma.Schema):
    def __init__(self, *args, **kwargs):
        self.custom_format = kwargs.pop('custom_format', 'default')
        super().__init__(*args, **kwargs)
    
    @pre_dump
    def adjust_timezone(self, data, **kwargs):
        if 'last_update' in data and data['last_update']:
            last_update = datetime.fromisoformat(data['last_update']).astimezone(TIME_ZONE)
            if self.custom_format == 'iso':
                data['last_update'] = last_update.isoformat()
            elif self.custom_format == 'timestamp':
                data['last_update'] = last_update.timestamp()
            else:
                data['last_update'] = last_update.strftime('%d/%m/%Y, %I:%M %p')
        return data

class UserSchema(ma.Schema):
    created_at = fields.DateTime(format='%d/%m/%Y, %I:%M %p')

    @pre_dump
    def adjust_timezone(self, data, **kwargs):
        if data.created_at:
            data.created_at = data.created_at.astimezone(TIME_ZONE)
        return data
    class Meta:
        fields = ("id", "name", "token", "is_premium", "created_at")

class MonitorSchema(BaseSchema):
    last_update = fields.String()
    price_old = fields.Float(missing=0.0, allow_none=True, default=0.0)
    
    class Meta:
        fields = ("key", "title", "price", "price_old", "last_update", "image", "percent", "change", "color", "symbol")

class HistoryPriceSchema(BaseSchema):
    last_update = fields.String()
    
    class Meta:
        fields = ("price", "last_update")