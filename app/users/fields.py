from django.db.models import EmailField as DjangoEmailField


class EmailField(DjangoEmailField):
    def to_python(self, value):
        value = super(EmailField, self).to_python(value)

        if isinstance(value, str):
            value = value.lower()

        return value
