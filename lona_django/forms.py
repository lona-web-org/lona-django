from django.db.models import TextField, BooleanField
from django.core.exceptions import ValidationError

from lona.html import (
    TextInput,
    TextArea,
    CheckBox,
    Widget,
    Table,
    Tr,
    Th,
    Td,
    Ul,
    Li,
)


class DjangoModelForm(Widget):
    INCLUDE_FIELDS = []
    EXCLUDE_FIELDS = []

    def __init__(self, model_object, include_fields=None, exclude_fields=None):
        self.include_fields = include_fields or self.INCLUDE_FIELDS
        self.exclude_fields = exclude_fields or self.EXCLUDE_FIELDS

        if self.include_fields and self.exclude_fields:
            raise ValueError('include_fields and exclude_fields are both set')

        self.model_object = model_object
        self.model_fields = self.get_model_fields()
        self.errors = {}
        self.nodes = self.render()

    def get_model_fields(self):
        model_fields = {}

        for field in self.model_object._meta.fields:
            if self.include_fields and field.name not in self.include_fields:
                continue

            if self.exclude_fields and field.name in self.exclude_fields:
                continue

            model_fields[field.name] = field

        return model_fields

    # errors ##################################################################
    def get_fields(self):
        """
        returns {
            'field_name': (django_field, field_input),
        }
        """

        fields = {}

        for node in self.nodes:
            for field_input in node.query_selector_all('input,textarea'):
                if 'name' not in field_input.attributes:
                    continue

                field_name = field_input.attributes['name']

                if field_name not in self.model_fields:
                    continue

                fields[field_name] = (
                    self.model_fields[field_name],
                    field_input,
                )

        return fields

    def has_errors(self):
        return bool(self.errors)

    def clear_errors(self):
        self.errors.clear()

    def add_error(self, field_name, error):
        if field_name not in self.errors:
            self.errors[field_name] = []

        self.errors[field_name].append(error)

    def clean(self):
        pass

    def _clean(self):
        self.clear_errors()

        for field_name, (field, field_input) in self.get_fields().items():
            try:
                field.clean(field_input.value, self.model_object)

            except ValidationError as error:
                for _error in error:
                    self.add_error(field_name, str(_error))

        self.clean()

    # model form api ##########################################################
    def reset(self):
        for field_name, (field, field_input) in self.get_fields().items():
            field_input.value = self.django_value(
                field,
                getattr(
                    self.model_object,
                    field_name
                ),
            )

    def save(self):
        self.clear_errors()
        self._clean()
        self.update()

        if self.has_errors():
            return False

        for field_name, (field, field_input) in self.get_fields().items():
            setattr(
                self.model_object,
                field_name,
                field_input.value,
            )

            self.model_object.save()

        return True

    def get_value(self, field_name):
        for _field_name, (field, field_input) in self.get_fields().items():
            if field_name == _field_name:
                return field_input.value

        raise AttributeError(
            '{} has no attribute {}',
            str(self.model_object.__class__),
            field_name,
        )

    def set_value(self, field_name, value):
        for _field_name, (field, field_input) in self.get_fields().items():
            if field_name == _field_name:
                field_input.value = str(value)

                return

        raise AttributeError(
            '{} has no attribute {}',
            str(self.model_object.__class__),
            field_name,
        )

    # HTML ####################################################################
    def django_field_to_lona_input(self, field):
        if isinstance(field, BooleanField):
            return CheckBox()

        if isinstance(field, TextField):
            return TextArea()

        return TextInput()

    def django_value(self, field, value):
        if isinstance(field, CheckBox) or \
           isinstance(field, BooleanField):
            return bool(value) or False

        return str(value) or ''

    def render(self):
        nodes = [
            Table(),
        ]

        for field_name, field in self.model_fields.items():
            field_input = self.django_field_to_lona_input(field)

            field_input.bubble_up = True
            field_input.attributes['name'] = field_name

            field_input.value = self.django_value(
                field_input,
                getattr(self.model_object, field_name),
                )

            field_input.class_list.add('modal-form')

            nodes[0].append(
                Tr(
                    Th(field.verbose_name),
                    Td(
                        field_input,
                        Ul(_class='error-list'),
                    ),
                )
            )

        return nodes

    def update(self):
        for field_name, (field, field_input) in self.get_fields().items():
            tr = field_input.closest('tr')
            error_list = tr.query_selector('ul.error-list')

            if not error_list:
                continue

            error_list.clear()

            if field_name not in self.errors:
                continue

            for error in self.errors[field_name]:
                error_list.append(Li(error))
