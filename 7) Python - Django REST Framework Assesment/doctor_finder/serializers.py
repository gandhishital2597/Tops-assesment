from rest_framework import serializers
from .models import Doctor

# A reasonable, closed list for demo validation purposes.
# Swap this for a ChoiceField / lookup table in a real production system.
ALLOWED_SPECIALIZATIONS = [
    'Cardiology', 'Dermatology', 'Pediatrics', 'Orthopedics',
    'Neurology', 'General Medicine', 'Ent', 'Gynecology', 'Psychiatry',
]


class DoctorSerializer(serializers.ModelSerializer):
    """
    Section A.2 demo: serializer as validation layer with
    custom field-level validation via validate_<field_name>.
    """

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'city']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        if any(ch.isdigit() for ch in value):
            raise serializers.ValidationError("Name cannot contain digits.")
        return value.title()

    def validate_specialization(self, value):
        value = value.strip().title()
        if value not in ALLOWED_SPECIALIZATIONS:
            raise serializers.ValidationError(
                f"'{value}' is not a recognized specialization. "
                f"Choose from: {', '.join(ALLOWED_SPECIALIZATIONS)}"
            )
        return value

    def validate_city(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("City name is too short.")
        return value.title()
