# convert Django model instances to JSON (and vice versa)

from rest_framework import serializers
from .models import Song

"""
- in Django REST Freamework (DRF), serializers handles the conversion of complex data types into Python native datatypes (Model -> JSON/XML)
- these can be then rendered into JSON, XML, or other content types
- they can also handle deserialization (JSON/XML -> Model)
- validation: DRF includes built-in validation for common fields (e.g. email, URL, etc.)
"""

# ModelSerializer auto-generates fields based on Song model
class SongSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(read_only=True)
    updated_at = serializers.DateField(read_only=True)
    
    class Meta:
        model = Song
        fields = '__all__' # all model fields in the API