import os
from twilio.rest import Client
from config import ContentID
from helpers import generate_booking_message
import logging
from session_manager import reset_session_data, set_last_send_attribute, set_session_value

# Initialize Twilio client
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']
client = Client(account_sid, auth_token)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Function to send a custom message based on the message type
def send_message(msg_type, sender, session_data, msg=None):
    if msg_type == "service":
        handle_service_message(sender, session_data)
    elif msg_type == "date":
        handle_date_message(sender, session_data)
    elif msg_type == "slot":
        handle_slot_message(sender, session_data)
    elif msg_type == "employee":
        handle_employee_message(sender, session_data)
    elif msg_type == "confirmation":
        handle_confirmation_message(sender, session_data)
    elif msg_type == "fallback":
        handle_fallback_message(sender, session_data)
    elif msg_type == "reset":
        handle_reset_message(sender, session_data)
    elif msg:
        handle_custom_message(msg, sender, session_data)
    else:
        print(f"Unknown message type: {msg_type}")

def handle_service_message(sender, session_data):
    send_content_message(sender, ContentID.CONTENT_SID_FIRST_MESSAGE)
    set_last_send_attribute(session_data, 'first')

def handle_date_message(sender, session_data):
    send_content_message(sender, ContentID.CONTENT_SID_DATES)
    set_last_send_attribute(session_data, 'service')
    
def handle_slot_message(sender, session_data):
    send_content_message(sender, ContentID.CONTENT_SID_SLOTS)
    set_last_send_attribute(session_data, 'date')

def handle_employee_message(sender, session_data):
    send_content_message(sender, ContentID.CONTENT_SID_EMPLOYEES)
    set_last_send_attribute(session_data, 'slot')

def handle_confirmation_message(sender, session_data):
    confirmation = generate_booking_message()
    send_text_message(confirmation, sender)
    set_last_send_attribute(session_data, 'employee')

def handle_fallback_message(sender, session_data):
    send_text_message("Hi! Welcome to *ServeEase*! 🎉 I'm your virtual assistant, here to help.\n\nSimply send 'Hi' to start booking services effortlessly!", sender)
    reset_session_data(session_data, 'fallback')

def handle_reset_message(sender, session_data):
    send_text_message("Sorry! Your session has been reset. Please start a new booking by sending 'Hi'.", sender)
    reset_session_data(session_data, 'reset')

def handle_custom_message(msg, sender, session_data):
    send_text_message(msg, sender)
    set_session_value(session_data, 'last_send_attribute', 'custom')

# Function to send a text message to a recipient
def send_text_message(msg, recipient):
    try:
        client.messages.create(
            body=msg,
            from_=twilio_phone_number,
            to=recipient
        )
        logging.info(f"Sent text message to {recipient}")
    except Exception as e:
        logging.error(f"Failed to send text message to {recipient}: {e}")

# Function to send a content message to a recipient
def send_content_message(recipient, content_sid):
    try:
        client.messages.create(
            from_=twilio_phone_number,
            to=recipient,
            content_sid=content_sid
        )
        logging.info(f"Sent content message to {recipient}")
    except Exception as e:
        logging.error(f"Failed to send content message to {recipient}: {e}")
