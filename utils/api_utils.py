import logging

from marshmallow import ValidationError

format_str = "%(asctime)s: %(message)s"
logging.basicConfig(format=format_str, level=logging.INFO,
                    datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)


def validate_data(data, schema):
    try:
        schema.validate(data=data)
    except ValidationError as err:
        logging.info(f'Errors found in payload: {err}')
        return {"message": "Invalid payload. Error: {}".format(err.messages)}, 400
