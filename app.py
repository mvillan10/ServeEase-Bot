from flask import Flask, request, session
from flask_session import Session
import logging
from config import Config
from helpers import sanitize_input
from messaging import send_message
from session_manager import initialize_session_data, clear_expired_sessions, set_session_object, get_last_send_attribute
from message_processor import process_msg, process_list_msg, process_button_msg, handle_invalid_response

# Initialize the Flask app with the configuration from config.py
app = Flask(__name__)
app.config.from_object(Config)
Session(app)

# Initialize logging
logging.basicConfig(level=logging.INFO)


# Route to check if the server is running
@app.route('/')
def index():
    return {
        'Result': 'The route is working'
    }


# Webhook route to handle incoming messages
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        clear_expired_sessions(session)  # Clear expired sessions to prevent memory leaks

        f = request.form  # Access the incoming form data from the request
        msg = sanitize_input(f.get('Body'))  # Sanitize the message body to prevent injection or malformed data
        sender = f.get('From')  # Extract the sender's ID from the form data
        message_type = f.get('MessageType')  # Determine the type of incoming message

        # Ensure that the sender ID is present
        if sender is None or sender == "":
            logging.error(f"Sender ID not found. Full request data: {f.to_dict()}")
            return "Error", 500

        # Initialize or update session data for the sender
        session_key, session_data = initialize_session_data(session, sender)

        # Handle interactive message types
        last_send_attribute = get_last_send_attribute(session_data)
        if last_send_attribute is not None and message_type == "interactive":
            button_payload = f.get('ButtonPayload')  # Get button payload if present
            list_id = f.get('ListId')  # Get list ID if present
            
            if last_send_attribute in ('date','slot') and button_payload is not None:
                # Process the button message based on its payload
                msg_type = process_button_msg(button_payload, session_data)
                send_message(msg_type, sender, session_data)  # Send the processed response to the sender

            elif last_send_attribute in ('service', 'employee') and list_id is not None:
                # Process the list message based on its ID
                msg_type = process_list_msg(list_id, session_data)
                send_message(msg_type, sender, session_data)  # Send the processed response to the sender
                
            else:
                # If no button payload or list ID is found, trigger the invalid response
                logging.warning(f"Invalid action. Sending invalid message alert to {sender}")
                handle_invalid_response(sender, session_data)
        else:
            # Handle non-interactive messages
            if msg is not None and msg != "" and last_send_attribute is not None:
                if msg.lower() == "reset":
                    send_message("reset", sender, session_data)  # Trigger the reset response for the sender
                elif last_send_attribute in ('first','service', 'date', 'slot'):
                    handle_invalid_response(sender, session_data)
                elif last_send_attribute in ('reset', 'fallback'):
                    msg_type = process_msg(msg)  # Process the general text message
                    send_message(msg_type, sender, session_data)  # Send the processed response to the sender
            else:
                # If the message body is empty or missing, trigger the invalid response
                logging.warning(f"Invalid message. Sending invalid message alert to {sender}")
                handle_invalid_response(sender, session_data)
                
    except Exception as e:
        # Log the exception and include a stack trace for debugging purposes
        logging.error(f"Error processing webhook: {e}", exc_info=True)
        return "Error", 500
    
    set_session_object(session, session_key, session_data)
    return "OK", 200  # Return success response if processing completes without errors


