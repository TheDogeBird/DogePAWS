from sanic.exceptions import InvalidUsage


def validate_request_payload(request, expected_keys):
    payload = request.json
    if not payload:
        raise InvalidUsage("Payload is missing")
    missing_keys = [key for key in expected_keys if key not in payload]
    if missing_keys:
        raise InvalidUsage(f"Payload is missing keys: {missing_keys}")
    return payload


def retrieve_payload(request):
    payload = request.app.config.SANIC_JWT_PAYLOAD_HANDLER(request)
    if not payload:
        raise InvalidUsage("Token is missing payload")
    return payload
