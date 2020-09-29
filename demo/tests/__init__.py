
form_data = {
    "label": "test create",
    "description": "my first formidable by api",
    "fields": [
        {
            "label": "hello",
            "slug": "textslug",
            "type_id": "text",
            "placeholder": None,
            "description": None,
            "default": None,
            "accesses": [
                {"access_id": "padawan", "level": "REQUIRED"},
                {"access_id": "jedi", "level": "EDITABLE"},
                {"access_id": "jedi-master", "level": "READONLY"},
                {"access_id": "human", "level": "HIDDEN"},
            ]
        },
    ]
}

form_data_readonly = {
    "label": "test readonly",
    "description": "readonly fields with defaults",
    "fields": [
        {
            "label": "readonly text",
            "slug": "readonly_text",
            "type_id": "text",
            "defaults": ["Hello World!"],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"}
            ]
        },
        {
            "label": "readonly paragraph",
            "slug": "readonly_paragraph",
            "type_id": "paragraph",
            "defaults": ["Hello World!"],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"}
            ]
        },
        {
            "label": "readonly date",
            "slug": "readonly_date",
            "type_id": "date",
            "defaults": ["2020-09-29"],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"}
            ]
        },
        {
            "label": "readonly number",
            "slug": "readonly_number",
            "type_id": "number",
            "defaults": [10],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"}
            ]
        },
        {
            "label": "readonly email",
            "slug": "readonly_email",
            "type_id": "email",
            "defaults": ["jon.europe@example.com"],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"}
            ]
        },
        {
            "label": "readonly dropdwon",
            "slug": "readonly_dropdown",
            "type_id": "dropdown",
            "defaults": ["val1"],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"},
            ],
            "items": [
                {'value': 'val1', 'label': 'Value 1'},
                {'value': 'val2', 'label': 'Value 2'},
                {'value': 'val3', 'label': 'Value 3'},
            ],
            "multiple": False
        },
        {
            "label": "readonly multiple dropdwon",
            "slug": "readonly_multiple_dropdown",
            "type_id": "dropdown",
            "defaults": ["val2", "val3"],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"},
            ],
            "items": [
                {'value': 'val1', 'label': 'Value 1'},
                {'value': 'val2', 'label': 'Value 2'},
                {'value': 'val3', 'label': 'Value 3'},
            ],
            "multiple": True
        },
        {
            "label": "readonly checkbox",
            "slug": "readonly_checkbox",
            "type_id": "checkbox",
            "defaults": ["val1"],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"},
            ],
            "items": [
                {'value': 'val1', 'label': 'Value 1'},
                {'value': 'val2', 'label': 'Value 2'},
                {'value': 'val3', 'label': 'Value 3'},
            ]
        },
        {
            "label": "readonly checkboxes",
            "slug": "readonly_checkboxes",
            "type_id": "checkboxes",
            "defaults": ["val2", "val3"],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"},
            ],
            "items": [
                {'value': 'val1', 'label': 'Value 1'},
                {'value': 'val2', 'label': 'Value 2'},
                {'value': 'val3', 'label': 'Value 3'},
            ]
        },
        {
            "label": "readonly radios",
            "slug": "readonly_radios",
            "type_id": "radios",
            "defaults": ["val1"],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"},
            ],
            "items": [
                {'value': 'val1', 'label': 'Value 1'},
                {'value': 'val2', 'label': 'Value 2'},
                {'value': 'val3', 'label': 'Value 3'},
            ]
        },
        {
            "label": "readonly radios buttons",
            "slug": "readonly_radios_buttons",
            "type_id": "radios_buttons",
            "defaults": ["val1"],
            "accesses": [
                {"access_id": "padawan", "level": "READONLY"},
            ],
            "items": [
                {'value': 'val1', 'label': 'Value 1'},
                {'value': 'val2', 'label': 'Value 2'},
                {'value': 'val3', 'label': 'Value 3'},
            ]
        }

    ],
}

form_data_items = {
    "label": "test create",
    "description": "my first formidable by api",
    "fields": [{
        "label": "my_dropdwon",
        "slug": "dropdown_slug",
        "type_id": "dropdown",
        "placeholder": None,
        "description": "Lesfrites c'est bon",
        "default": None,
        "accesses": [
            {"access_id": "padawan", "level": "REQUIRED"},
            {"access_id": "jedi", "level": "EDITABLE"},
            {"access_id": "jedi-master", "level": "READONLY"},
            {"access_id": "human", "level": "HIDDEN"},
        ],
        "items": [
            {'value': 'tuto', 'label': 'toto'},
            {'value': 'plop', 'label': 'coin'},
        ],
        "multiple": False
    }]
}
