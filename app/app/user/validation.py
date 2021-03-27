from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

create_users_schema = {
    'type': 'object',
    'properties': {
        'id': {
            'type': 'number',
        },
        'first_name': {
            'type': 'string',
        },
        'last_name': {
            'type': 'string',
        },
        'username': {
            'type': 'string',
        },
    },
    'required': ['id', 'first_name']
}


class CreateUsers(Inputs):
    json = [JsonSchema(schema=create_users_schema)]


def validate_create_users(request):
    inputs = CreateUsers(request)
    if inputs.validate():
        return None
    else:
        return inputs.errors
