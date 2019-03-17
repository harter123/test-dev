import json
from django.core import serializers

class Base:
    def serializer_json(self, field):
        s = serializers.serialize('json', self, fields=field)
        return s

    def serializer_dict(self, field):
        s = self.serializer_json(field)
        d = json.loads(s)
        return d