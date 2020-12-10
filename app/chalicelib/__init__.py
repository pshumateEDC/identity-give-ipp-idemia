REG_SCHEMA = {
    "type": "object",
    "properties": {
        "uuid": {"type": "string"},
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "emailAddress": {"type": "string"},
    },
    "required": ["uuid", "firstName", "lastName", "emailAddress"],
    "additionalProperties": False,
}

STATUS_SCHEMA = {
    "type": "object",
    "properties": {"ippstatus": {"type": "string"}},
    "required": ["ippstatus"],
    "additionalProperties": False,
}
