var spec = {
    "basePath": "/api",
    "definitions": {
        "Access": {
            "description": "Different contexts that helps to render a form",
            "properties": {
                "description": {
                    "description": "Help text of the access",
                    "type": "string"
                },
                "id": {
                    "description": "ID of the access",
                    "type": "string"
                },
                "label": {
                    "description": "Label of the access",
                    "type": "string"
                },
                "preview_as": {
                    "description": "How to display the preview, default is `FORM`. Values are `FORM`, `TABLE`",
                    "enum": [
                        "FORM",
                        "TABLE"
                    ],
                    "type": "string"
                }
            },
            "required": [
                "id",
                "label",
                "description"
            ],
            "type": "object"
        },
        "BuilderError": {
            "properties": {
                "fields": {
                    "description": "Errors on fields (key => field; value => list of messages)",
                    "type": "object"
                },
                "non_field_errors": {
                    "description": "Errors on anything except fields (validations...)",
                    "items": {
                        "type": "string"
                    },
                    "type": "array"
                }
            },
            "type": "object"
        },
        "BuilderForm": {
            "allOf": [
                {
                    "$ref": "#/definitions/Form"
                },
                {
                    "properties": {
                        "fields": {
                            "description": "List of fields ordered in the form",
                            "items": {
                                "$ref": "#/definitions/Field"
                            },
                            "type": "array"
                        }
                    }
                }
            ]
        },
        "Condition": {
            "description": "TODO",
            "properties": {
                "action": {
                    "enum": [
                        "display_iff"
                    ],
                    "type": "string"
                },
                "field_ids": {
                    "items": {
                        "type": "string"
                    },
                    "type": "array"
                },
                "name": {
                    "type": "string"
                },
                "tests": {
                    "items": {
                        "$ref": "#/definitions/ConditionTest"
                    },
                    "type": "array"
                }
            },
            "type": "object"
        },
        "ConditionTest": {
            "description": "Condition",
            "properties": {
                "field_id": {
                    "description": "Reference field for the comparison",
                    "type": "string"
                },
                "operator": {
                    "enum": [
                        "eq"
                    ],
                    "type": "string"
                },
                "values": {
                    "items": {
                        "type": "string"
                    },
                    "type": "array"
                }
            },
            "type": "object"
        },
        "Field": {
            "description": "Field in a form",
            "properties": {
                "accesses": {
                    "description": "List of accesses of the field with a level",
                    "items": {
                        "$ref": "#/definitions/FieldAccess"
                    },
                    "type": "array"
                },
                "defaults": {
                    "description": "Default values selected/inputed when the form is newly displayed",
                    "items": {
                        "type": "string"
                    },
                    "type": "array"
                },
                "description": {
                    "description": "Description of the field",
                    "type": "string"
                },
                "id": {
                    "description": "ID of the field",
                    "readOnly": true,
                    "type": "integer"
                },
                "items": {
                    "description": "Values available",
                    "items": {
                        "$ref": "#/definitions/Item"
                    },
                    "type": "array"
                },
                "label": {
                    "description": "Label of the field",
                    "type": "string"
                },
                "multiple": {
                    "description": "Is the field can have multiple values?",
                    "type": "boolean"
                },
                "placeholder": {
                    "description": "Placeholder of the field",
                    "type": "string"
                },
                "slug": {
                    "description": "Slug of the field (us as uniq identifier of the field on the form)",
                    "type": "string"
                },
                "type_id": {
                    "description": "Type of field (see Field types table)",
                    "type": "string"
                },
                "validations": {
                    "description": "List of validations of the field",
                    "items": {
                        "$ref": "#/definitions/FieldValidation"
                    },
                    "type": "array"
                }
            },
            "required": [
                "id",
                "slug",
                "label",
                "type_id",
                "description",
                "accesses"
            ],
            "type": "object"
        },
        "FieldAccess": {
            "description": "The access is the way to use the field in the context",
            "properties": {
                "access_id": {
                    "description": "Access reference",
                    "type": "string"
                },
                "level": {
                    "description": "Level of this access for the field",
                    "enum": [
                        "REQUIRED",
                        "EDITABLE",
                        "HIDDEN",
                        "READONLY"
                    ],
                    "type": "string"
                }
            },
            "required": [
                "access_id",
                "level"
            ],
            "type": "object"
        },
        "FieldValidation": {
            "description": "This validation can only be performed on a single field",
            "properties": {
                "message": {
                    "description": "Error message if the validation is not verified",
                    "type": "string"
                },
                "type": {
                    "description": "Type of validation (see Validation types table)",
                    "type": "string"
                },
                "value": {
                    "description": "Value of the validation",
                    "type": "string"
                }
            },
            "required": [
                "type",
                "value"
            ],
            "type": "object"
        },
        "Form": {
            "description": "The central piece of this project",
            "properties": {
                "conditions": {
                    "items": {
                        "$ref": "#/definitions/Condition"
                    },
                    "type": "array"
                },
                "description": {
                    "description": "Description of the form",
                    "type": "string"
                },
                "id": {
                    "description": "ID of the form",
                    "readOnly": true,
                    "type": "integer"
                },
                "label": {
                    "description": "Title of the form",
                    "type": "string"
                }
            },
            "required": [
                "id",
                "label",
                "description"
            ],
            "type": "object"
        },
        "InputError": {
            "description": "Object that contains field errors as key with a list of string in value",
            "properties": {
                "__all__": {
                    "description": "Errors on anything except form's fields",
                    "items": {
                        "type": "string"
                    },
                    "type": "array"
                }
            },
            "type": "object"
        },
        "InputField": {
            "allOf": [
                {
                    "$ref": "#/definitions/Field"
                }
            ],
            "properties": {
                "values": {
                    "description": "Values selected/inputed when the form is in edition mode",
                    "items": {
                        "type": "string"
                    },
                    "type": "array"
                }
            }
        },
        "InputForm": {
            "allOf": [
                {
                    "$ref": "#/definitions/Form"
                },
                {
                    "properties": {
                        "fields": {
                            "description": "List of fields ordered in the form",
                            "items": {
                                "$ref": "#/definitions/InputField"
                            },
                            "type": "array"
                        }
                    }
                }
            ]
        },
        "Item": {
            "description": "Describe an item in a list",
            "properties": {
                "description": {
                    "description": "Description of the item",
                    "type": "string"
                },
                "label": {
                    "description": "Label of the item",
                    "type": "string"
                },
                "value": {
                    "description": "Value which defined the item",
                    "type": "string"
                }
            },
            "required": [
                "label",
                "value"
            ],
            "type": "object"
        }
    },
    "host": "localhost:8000",
    "info": {
        "description": "django-formidable is a full django application which allows you to create,\nedit, delete and use forms.\n\n##### Field types\n\nList of known types available:\n\n| Type | Description | HTML Component |\n| ---- | ----------- | -------------- |\n| title | Title | h2 |\n| helpText | Helptext | p |\n| fieldset | Group of fields (iterable) | fieldset |\n| fieldsetTable | Group of fields display as table (iterable) | table |\n| separation | Separator line (design only) | hr |\n| checkbox | Checkbox alone | input type=checkbox |\n| checkboxes | Some checkboxes, all checkable | input type=checkbox, all have the same name |\n| dropdown | Dropdown with values | select |\n| radios | Some radios, only one is selected at once | input type=radio |\n| radiosButtons | Some radios display as toggle button | input type=radio |\n| text | Input for one line text | input type=text |\n| paragraph | Input for multiline text | textarea |\n| file | Field to select a local file to be uploaded | input type=file |\n| date | Input for a date (datepicker with it, lang know by application parameter, validation by momentjs) | input type=date |\n| email | Input for an email (validation by regexp) | input |\n| number | Input for a number | input |\n\n##### Validations types\n\nList of validations available by types:\n\n| Field | Validation type |\n| ----- | ----------- |\n| text | MINLENGTH, MAXLENGTH, REGEXP |\n| paragraph | MINLENGTH, MAXLENGTH, REGEXP |\n| date | GT, GTE, LT, LTE, EQ, NEQ, IS_AGE_ABOVE (>=), IS_AGE_UNDER (<), IS_DATE_IN_THE_PAST (< today), IS_DATE_IN_THE_FUTURE (< today) |\n| number | GT, GTE, LT, LTE, EQ, NEQ |\n",
        "title": "Formidable API",
        "version": "1.0.0"
    },
    "paths": {
        "/builder/accesses/": {
            "get": {
                "description": "List of accesses available.",
                "responses": {
                    "200": {
                        "description": "A list of accesses",
                        "schema": {
                            "items": {
                                "$ref": "#/definitions/Access"
                            },
                            "type": "array"
                        }
                    }
                },
                "summary": "Get accesses"
            }
        },
        "/builder/forms/": {
            "post": {
                "description": "Create Form Description",
                "parameters": [
                    {
                        "in": "body",
                        "name": "form",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/BuilderForm"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Newly created form",
                        "schema": {
                            "$ref": "#/definitions/BuilderForm"
                        }
                    },
                    "400": {
                        "description": "Unexpected error",
                        "schema": {
                            "$ref": "#/definitions/BuilderError"
                        }
                    }
                },
                "summary": "Create a new form"
            }
        },
        "/builder/forms/{id}/": {
            "get": {
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Form",
                        "schema": {
                            "$ref": "#/definitions/BuilderForm"
                        }
                    }
                },
                "summary": "Retrieve a Form"
            },
            "put": {
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "required": true,
                        "type": "integer"
                    },
                    {
                        "in": "body",
                        "name": "form",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/BuilderForm"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Form",
                        "schema": {
                            "$ref": "#/definitions/BuilderForm"
                        }
                    },
                    "400": {
                        "description": "Unexpected error",
                        "schema": {
                            "$ref": "#/definitions/BuilderError"
                        }
                    }
                },
                "summary": "Update a Form"
            }
        },
        "/forms/{id}/": {
            "get": {
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "A form",
                        "schema": {
                            "$ref": "#/definitions/BuilderForm"
                        }
                    }
                },
                "summary": "Get a contextualized form"
            }
        },
        "/forms/{id}/validate/": {
            "get": {
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Validation OK"
                    },
                    "400": {
                        "description": "Validation KO",
                        "schema": {
                            "$ref": "#/definitions/InputError"
                        }
                    }
                }, 
                "summary": "Validate a form (GET method). GET and POST are equivalent, but GET is deprecated."
            },
            "post": {
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "required": true,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Validation OK"
                    },
                    "400": {
                        "description": "Validation KO",
                        "schema": {
                            "$ref": "#/definitions/InputError"
                        }
                    }
                },
                "summary": "Validate a form (POST method). GET and POST are equivalent."
            }
        }
    },
    "produces": [
        "application/json"
    ],
    "schemes": [
        "http"
    ],
    "swagger": "2.0"
}
