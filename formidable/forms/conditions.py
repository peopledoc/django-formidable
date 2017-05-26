# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six


class ConditionsRegister(dict):

    def gen_from_schema(self, fields, conditions_schema):
        for condition in conditions_schema:
            # name, fields_ids, action, tests
            klass = self[condition['action']]

            # cast values to field's type
            def convert_values(field_id, values):
                field = fields[field_id]
                return [field.to_python(value) for value in values]

            tests = [ConditionTest(test['field_id'],
                                   test['operator'],
                                   convert_values(test['field_id'],
                                                  test['values']))
                     for test in condition['tests']]
            yield klass(
                condition['fields_ids'],
                condition['name'],
                tests
            )

    def build(self, fields, conditions_schema):
        # TODO XXX deepcopy ?
        return list(self.gen_from_schema(fields, conditions_schema))


conditions_register = ConditionsRegister()


class ConditionsMetaClass(type):

    def __new__(mcls, name, base, attrs):
        klass = super(ConditionsMetaClass, mcls).__new__(
            mcls, name, base, attrs
        )
        if 'action' in attrs:
            conditions_register[klass.action] = klass
        return klass


class ConditionTest(object):

    mapper = {
        'eq': lambda field, values: field == values[0],
    }

    def __init__(self, field_id, operator, values):
        self.field_id = field_id
        self.operator = operator
        # do we need to cast values according to ref field type ?
        # form.fields[field_id].to_python(value) ...
        self.values = values

    def __call__(self, cleaned_data):
        meth = self.mapper[self.operator]

        try:
            ref_value = cleaned_data[self.field_id]
            return meth(ref_value, self.values)
        except:
            # KeyError if self.field_id not in cleaned_data
            # TODO XXX add log ?
            return False


class Condition(six.with_metaclass(ConditionsMetaClass)):

    def __init__(self, fields_ids, name, tests):
        self.name = name
        self.tests = tests
        self.fields_ids = fields_ids


class DisplayIffCondition(Condition):
    action = 'display_iff'

    def __call__(self, form, cleaned_data):
        # Check if the condition is True
        is_displayed = True
        for test in self.tests:
            is_displayed = test(cleaned_data)
            if not is_displayed:
                break

        # if not, we need to remove the fields from `cleaned_data` and
        # `form.errors`
        if not is_displayed:
            for field_id in self.fields_ids:
                cleaned_data.pop(field_id, None)
                form.errors.pop(field_id, None)
        return cleaned_data

    def __repr__(self):
        return "<{classname} {name}>".format(
            classname=self.__class__.__name__,
            name=self.name)
