import binascii
from binascii import a2b_hex
import json
import string
from checksumio.algorithms.crc import PredefinedCRCAlgorithClassifier
from pyramid.response import Response
from pyramid.view import view_config
import re

HEX_RE = re.compile(r"^[0-9a-fA-F]*$")
STR_RE = re.compile(r"%(\w|\s)*$")
PAYLOAD_FORMAT_GUESS = "guess"
PAYLOAD_FORMAT_HEX = "hex"
PAYLOAD_FORMAT_STRING = "string"
PAYLOAD_FORMAT_PYREPR = "repr"


def _parse_as_hex(value):
    """Try to parse the value as a hex payload, raise ValueError if unable"""
    # First, remove any whitespace
    value = value.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")

    # Strip leading 0x or 0X
    if not (value.startswith('0x') or value.startswith('0X')):
        value = value[2:]

    if len(value) % 2 != 00:
        raise ValueError("Payload size not evenly divisible by two")

    if HEX_RE.match(value) is None:
        raise ValueError("Payload contains non-hexadecimal characters")

    try:
        return binascii.a2b_hex(value)
    except TypeError:
        raise ValueError("Not a valid input sequence")


def _parse_as_string(value):
    if not all(c in string.printable for c in value):
        raise ValueError("Payloads contains non-printable characters, try using hex")
    return value


def _attempt_parse_payload(payload, payload_format):
    if payload_format == PAYLOAD_FORMAT_HEX:
        return _parse_as_hex(payload)
    elif payload_format == PAYLOAD_FORMAT_STRING:
        return _parse_as_string(payload)
    elif payload_format == PAYLOAD_FORMAT_GUESS:
        try:
            return _parse_as_hex(payload)
        except ValueError:
            pass
        try:
            return _parse_as_string(payload)
        except ValueError:
            pass
        raise ValueError("String provided does not follow hex or string formats")


def _attempt_parse_checksum(value):
    if value.startswith("0x") or value.startswith("0X"):
        return int(value[2:], 16)
    else:
        return int(value, 10)


@view_config(route_name='validate_payload', renderer='json')
def validate_payload(request):
    try:
        _attempt_parse_payload(request.params["payload"], request.params.get("payload_format", "guess"))
    except ValueError, e:
        return json.dumps({"error": "Invalid payload, must be hex or string"})
    else:
        return json.dumps({"success": "success"})


@view_config(route_name='validate_checksum', renderer='json')
def validate_checksum(request):
    try:
        _attempt_parse_checksum(request.params["checksum"])
    except ValueError, e:
        return {"error": "Invalid checksum must be hex (0x...) or base 10 integer"}
    else:
        return {"success": "success"}


@view_config(route_name='index', renderer='index.jinja2')
def index(request):
    return {}


@view_config(route_name="revcheck", renderer='json')
def revcheck(request):
    payload = request.params["payload"]
    checksum = request.params["checksum"]
    payload_format = request.params.get("payload_format", "guess")

    # Attempt parsing payload
    parsed_payload = _attempt_parse_payload(payload, payload_format)
    parsed_checksum = _attempt_parse_checksum(checksum)

    # Attempt parsing provided checksum
    predefined_classifier = PredefinedCRCAlgorithClassifier()
    match = predefined_classifier.find_match(parsed_payload, parsed_checksum)
    if match is None:
        return {
            "result": "no_algorithm_found",
            "message": "Data was valid but not matching checksum algorithm was found"
        }
    else:
        return {
            "result": "success",
            "algoriths": [
                {"type": "predefined",
                 "key": match}
            ]
        }

