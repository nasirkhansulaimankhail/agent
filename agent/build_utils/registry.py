from agent.exceptions import AgentException


def raise_for_push_error(event: dict):
    detail = event.get("errorDetail")
    if not event.get("error") and not detail:
        return

    message = event.get("error")
    if not message and isinstance(detail, dict):
        message = detail.get("message")
    message = message or "Unknown registry error"
    raise AgentException({"traceback": f"Docker image push failed: {message}"})
