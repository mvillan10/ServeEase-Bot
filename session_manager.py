import time
import logging
from typing import Dict, Tuple, Any

EXPIRATION_TIME = 3600  # 1 hour in seconds

def clear_expired_sessions(session: Dict[str, Any]) -> None:
    """
    Clear expired sessions from the session dictionary.
    """
    if session is None:
        logging.error("Session is None. Unable to clear expired sessions.")
        return

    current_time = time.time()
    for sender_id in list(session.keys()):
        if sender_id not in ('_flashes', '_permanent'):
            if current_time - session[sender_id]['start_time'] > EXPIRATION_TIME:
                session.pop(sender_id, None)

def initialize_session_data(session: Dict[str, Any], sender: str) -> Tuple[str, Dict[str, Any]]:
    """
    Initialize or update session data for the sender.
    """
    if session is None:
        logging.error("Session is None. Unable to initialize session data.")
        return "", {}

    session_key = f'chat:{sender}'
    session_data = session.get(session_key, {
        'service': None,
        'date': None,
        'slot': None,
        'employee': None,
        'orderid': None,
        'start_time': time.time(),
        'last_time': time.time(),
        'last_send_attribute': None,
        'invalidCount': 0
    })
    set_session_value(session_data, 'last_time', time.time())
    return session_key, session_data

def reset_session_data(session_data: Dict[str, Any], last_send_attribute: Any) -> None:
    """
    Reset the session data.
    """
    if session_data is None:
        logging.error("Session data is None. Unable to reset.")
        return

    session_data.update({
        'service': None,
        'date': None,
        'slot': None,
        'employee': None,
        'orderid': None,
        'start_time': time.time(),
        'last_time': time.time(),
        'last_send_attribute': last_send_attribute,
        'invalidCount': 0
    })
    logging.info(f"Session data reset with attribute: {last_send_attribute}")

def check_invalid_count(session_data: Dict[str, Any]) -> bool:
    """
    Check the invalid count and return a boolean.
    """
    if session_data is None:
        logging.error("Session data is None. Unable to check invalid count.")
        return False

    invalid_count = get_session_value(session_data, 'invalidCount')
    if invalid_count is not None and invalid_count < 3:
        set_session_value(session_data, 'invalidCount', invalid_count + 1)
        return True
    else:
        return False

def set_last_send_attribute(session_data: Dict[str, Any], attribute: Any, reset_invalid_count: bool = True) -> None:
    """
    Set the last send attribute in the session data and reset invalid count.
    """
    if session_data is None:
        logging.error("Session data is None. Unable to set last send attribute.")
        return

    if get_last_send_attribute(session_data) is not None:
        set_session_value(session_data, 'last_send_attribute', attribute)
        if reset_invalid_count and get_session_value(session_data, 'invalidCount') is not None:
            set_session_value(session_data, 'invalidCount', 0)

def get_last_send_attribute(session_data: Dict[str, Any]) -> Any:
    """
    Get the last send attribute from the session data.
    """
    if session_data is None:
        logging.error("Session data is None. Unable to get last send attribute.")
        return None

    return session_data.get('last_send_attribute', None)

def get_session_value(session_data: Dict[str, Any], key: str) -> Any:
    """
    Get the value of a key from the session data.
    """
    if session_data is None:
        logging.error("Session data is None. Unable to get session value.")
        return None

    return session_data.get(key, None)

def set_session_value(session_data: Dict[str, Any], key: str, value: Any) -> None:
    """
    Set the value of a key in the session data.
    """
    if session_data is None:
        logging.error("Session data is None. Unable to set session value.")
        return

    session_data[key] = value

def set_session_object(session: Dict[str, Any], session_key: str, session_data: Dict[str, Any]) -> None:
    """
    Set the session object with the updated session data.

    Parameters:
    session (dict): The session dictionary.
    session_key (str): The key for the session data.
    session_data (dict): The session data to be set.
    """
    if session is None or session_key is None or session_data is None:
        logging.error("Invalid session, session_key, or session_data. Unable to set session object.")
        return

    session[session_key] = session_data
