from formidable.forms import (
    FormidableForm, fields
)
from formidable import constants


class CheckboxConditionsTestForm(FormidableForm):
    checkbox_a = fields.BooleanField(
        label='My checkbox',
        accesses={'padawan': constants.EDITABLE,
                  'jedi': constants.EDITABLE,
                  'human': constants.EDITABLE,
                  'robot': constants.REQUIRED}
    )
    checkbox_ab = fields.BooleanField(
        label='My checkbox 2',
        accesses={'padawan': constants.EDITABLE,
                  'jedi': constants.EDITABLE,
                  'human': constants.EDITABLE,
                  'robot': constants.REQUIRED}
    )
    a = fields.CharField(
        label='a',
        accesses={'padawan': constants.EDITABLE,
                  'jedi': constants.EDITABLE,
                  'human': constants.REQUIRED,
                  'robot': constants.REQUIRED}
    )
    b = fields.CharField(
        label='b',
        accesses={'padawan': constants.EDITABLE,
                  'jedi': constants.EDITABLE,
                  'human': constants.READONLY,
                  'robot': constants.REQUIRED}
    )


class DropdownConditionsTestForm(FormidableForm):
    main_dropdown = fields.ChoiceField(
        choices=(
            ('ab', 'AB'),
            ('b', 'B'),
            ('no_condition', 'No_condition')
        ),
        accesses={'padawan': constants.EDITABLE}
    )
    a = fields.CharField(
        accesses={'padawan': constants.EDITABLE})
    b = fields.CharField(
        accesses={'padawan': constants.EDITABLE})
    c = fields.CharField(
        accesses={'padawan': constants.EDITABLE})


class MultipleChoicesConditionsTestForm(FormidableForm):
    main_choices = fields.MultipleChoiceField(
        choices=(
            ('a', 'A'),
            ('b', 'B'),
            ('no_condition', 'No_condition')
        ),
        accesses={'padawan': constants.EDITABLE}
    )
    a = fields.CharField(accesses={'padawan': constants.EDITABLE})
    b = fields.CharField(accesses={'padawan': constants.EDITABLE})
    c = fields.CharField(accesses={'padawan': constants.EDITABLE})


class SimpleConditionTestCaseTestForm(FormidableForm):
    checkbox = fields.BooleanField(
        label='My checkbox',
        accesses={'padawan': constants.EDITABLE,
                  'jedi': constants.EDITABLE,
                  'human': constants.EDITABLE,
                  'robot': constants.REQUIRED}
    )
    foo = fields.CharField(
        label='Foo',
        accesses={'padawan': constants.EDITABLE,
                  'jedi': constants.REQUIRED,
                  'human': constants.REQUIRED,
                  'robot': constants.REQUIRED}
    )
    bar = fields.CharField(
        label='Bar',
        accesses={'padawan': constants.EDITABLE,
                  'jedi': constants.REQUIRED,
                  'human': constants.READONLY,
                  'robot': constants.REQUIRED}
    )
