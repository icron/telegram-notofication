from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

create_keywords_schema = {
    'type': 'object',
    'properties': {
        'channel_id': {
            'type': 'number',
        },
        'user_id': {
            'type': 'number',
        },
        'keywords': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        }
    },
    'required': ['channel_id', 'user_id', 'keywords']
}

update_keywords_schema = {
    'type': 'object',
    'properties': {
        'uuid': {
            'type': 'string',
        },
        'channel_id': {
            'type': 'number',
        },
        'user_id': {
            'type': 'number',
        },
        'keywords': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        }
    },
    'required': ['uuid', 'channel_id', 'user_id', 'keywords']
}

delete_keywords_schema = {
    'type': 'object',
    'properties': {
        'uuid': {
            'type': 'string',
        }
    },
    'required': ['uuid']
}


class CreateKeywords(Inputs):
    json = [JsonSchema(schema=create_keywords_schema)]


class UpdateKeywords(Inputs):
    json = [JsonSchema(schema=update_keywords_schema)]


class DeleteKeywords(Inputs):
    json = [JsonSchema(schema=delete_keywords_schema)]


def validate_create_keywords(request):
    inputs = CreateKeywords(request)
    if inputs.validate():
        return None
    else:
        return inputs.errors


def validate_update_keywords(request):
    inputs = UpdateKeywords(request)
    if inputs.validate():
        return None
    else:
        return inputs.errors


def validate_delete_keywords(request):
    inputs = DeleteKeywords(request)
    if inputs.validate():
        return None
    else:
        return inputs.errors
