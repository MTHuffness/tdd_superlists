from django import forms
from .models import Item
from django.core.exceptions import ValidationError

EMPTY_LIST_ERROR = "You can't have an empty list item"
DUPLICATE_LIST_ERROR = "You've already got this in your list"


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {'text': forms.fields.TextInput(
            attrs={'placeholder': 'Enter a to-do item',
                   'class': 'form-control input-lg'})}
        error_messages = {'text': {'required': EMPTY_LIST_ERROR}}

    def save(self, for_list):
        # instance represents the database object that is being modified or created.
        self.instance.list = for_list
        return super().save()


class ExistingListItemForm(ItemForm):
    """
    Creates a new class for concurrent form data entered. inherits from the regular form
    as they are essentially the same. only difference is this class uses the validate_unique()
    method to compare its data with the current data already entered.
    """

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            # takes the validation error, adjust the message, and pass it back to the form.
            e.error_dict = {'text': [DUPLICATE_LIST_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)
