from typing import Dict, Any
from session_manager import set_session_value, get_last_send_attribute, check_invalid_count
from helpers import validate_input
from messaging import send_message

def process_msg(msg: str) -> str:
    """
    Process incoming text messages.
    """
    response = ""
    greetings = [
        "hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening",
        "help", "info", "information", "support", "assist"
    ]
    if msg.lower() in greetings:  # Check if the message is a greeting
        response = "first"
    else:
        response = "fallback"
    return response

def process_list_msg(list_id: str, session_data: Dict[str, Any]) -> str:
    """
    Process list messages.
    """
    response = ""
    # Validate the list ID to determine the type of response to send
    if not validate_input(list_id):
        print(f"Invalid list ID: {list_id}")
        return "Error"

    # Handle different cases based on the last sent attribute
    last_send_attribute = get_last_send_attribute(session_data)
    if last_send_attribute is not None and last_send_attribute == 'service':
        response = handle_service_list_id(list_id, session_data)
    elif last_send_attribute is not None and last_send_attribute == 'employee':
        response = handle_employee_list_id(list_id, session_data)
    else:
        print(f"Unknown list ID: {list_id}")
        response = "invalid"

    return response

def handle_service_list_id(list_id: str, session_data: Dict[str, Any]) -> str:
    """
    Handle service list ID.
    """
    if list_id in ('1', '2', '3', '4'):
        set_session_value(session_data, 'service', list_id)
        return "date"
    return "invalid"

def handle_employee_list_id(list_id: str, session_data: Dict[str, Any]) -> str:
    """
    Handle employee list ID.
    """
    if list_id in ('100', '101', '102', '103'):
        set_session_value(session_data, 'employee', list_id)
        return "confirmation"
    return "invalid"

def process_button_msg(button_payload: str, session_data: Dict[str, Any]) -> str:
    """
    Process button messages.
    """
    response = ""
    # Validate the button payload to ensure it's in the expected format
    if not validate_input(button_payload):
        print(f"Invalid button payload: {button_payload}")
        return "Error"

    # Handle different cases based on the last sent attribute
    last_send_attribute = get_last_send_attribute(session_data)
    if last_send_attribute is not None and last_send_attribute == 'date':
        response = handle_date_button_payload(button_payload, session_data)
    elif last_send_attribute is not None and last_send_attribute == 'slot':
        response = handle_slot_button_payload(button_payload, session_data)
    else:
        print(f"Unknown button payload: {button_payload}")
        response = "invalid"

    return response

def handle_date_button_payload(button_payload: str, session_data: Dict[str, Any]) -> str:
    """
    Handle date button payload.
    """
    if button_payload in ('7', '8', '9', '10'):
        set_session_value(session_data, 'date', button_payload)
        return "slot"
    return "invalid"

def handle_slot_button_payload(button_payload: str, session_data: Dict[str, Any]) -> str:
    """
    Handle slot button payload.
    """
    if button_payload in ('10', '11', '12'):
        set_session_value(session_data, 'slot', button_payload)
        return "employee"
    return "invalid"

def handle_invalid_response(sender: str, session_data: Dict[str, Any]) -> None:
    """
    Handle invalid responses.
    """
    if check_invalid_count(session_data):
        send_message("invalid", sender, session_data)
    else:
        send_message("reset", sender, session_data)