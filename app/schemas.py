from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models import Device, DeviceDiagnostics, db

# --------------------------
#  Device Schema
# --------------------------
class DeviceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Device
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True  # If you need user_id or foreign keys

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    device_type = fields.Str(required=True)
    status = fields.Str(required=True)
    location = fields.Str(required=True)


# --------------------------
#  Diagnostics Schema
# --------------------------
class DeviceDiagnosticsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DeviceDiagnostics
        load_instance = True
        sqla_session = db.session
        include_fk = True

    id = fields.Int(dump_only=True)
    device_id = fields.Int(required=True)
    cpu_usage = fields.Float(required=True)
    memory_usage = fields.Float(required=True)
    timestamp = fields.DateTime(allow_none=True, missing=None)
