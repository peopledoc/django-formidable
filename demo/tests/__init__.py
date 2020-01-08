
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
