def http_400_error(error_message):
    return {"status": "error", "message": error_message}, 400, {'Content-Type': 'application/json'}

