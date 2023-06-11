from rest_framework import serializers
from .models import Dataset
import re

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'

class CleanedDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'

    def to_representation(self, instance):
        result = super().to_representation(instance)
        for key, value in result.items():
            if isinstance(value, str):
                # This will replace any occurrences of "\n" or "\\n" with a space.
                value = value.replace("\\n", " ").replace("\n", " ")
                # This will remove extra spaces.
                value = re.sub(' +', ' ', value)
                result[key] = value.strip()
        return result