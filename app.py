from flask import Flask, request
from twilio.rest import Client
import os
import random

app = Flask(__name__)

# Twilio credentials
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']
client = Client(account_sid, auth_token)

# Function to send a custom message to a recipient
def send_message(msg, recipient):
    client.messages.create(
        body=msg,
        from_=twilio_phone_number,
        to=recipient
    )

# Function to send the first message to a recipient
def send_first_message(recipient):
    client.messages.create(
        from_=twilio_phone_number,
        to=recipient,
        content_sid="HX8d2b12aa879b9a26fb3d29b04765bd8d"
    )

# Function to send available dates to a recipient
def send_dates(recipient):
    client.messages.create(
        from_=twilio_phone_number,
        to=recipient,
        content_sid="HX574d53a22805bf8a078608c994b857e1"
    )

# Function to send available slots to a recipient
def send_slots(recipient):
    client.messages.create(
        from_=twilio_phone_number,
        to=recipient,
        content_sid="HX9dec5bc934f9064ba054d764d82bb74b"
    )

# Function to send available employees to a recipient
def send_employees(recipient):
    client.messages.create(
        from_=twilio_phone_number,
        to=recipient,
        content_sid="HXd5a971eb45071b0997db05131e9bf8ad"
    )

# Function to process incoming text messages
def process_msg(msg):
    response = ""
    if msg == "Hi" or msg == "hi":
        response = "first"
    else:
        response = "Hi! Welcome to *ServeEase*! 🎉 I'm your virtual assistant, here to help.\n\nSimply send 'Hi' to start booking services effortlessly!"
    return response

# Function to process list messages
def process_list_msg(list_id):
    response = ""
    if list_id == "1" or list_id == "2" or list_id == "3" or list_id == "4":
        response = "date"
    elif list_id == "100" or list_id == "101" or list_id == "102" or list_id == "103":
        response = "done"
    return response

# Function to process button messages
def process_button_msg(button_payload):
    response = ""
    if button_payload == "7" or button_payload == "8" or button_payload == "9" or button_payload == "10":
        response = "slot"
    elif button_payload == "10" or button_payload == "11" or button_payload == "12":
        response = "employee"
    return response

# Function to generate a booking confirmation message
def generate_booking_message():
    # Generate a random 6-digit booking ID
    booking_id = random.randint(250000, 259999)
    # Construct the message
    message = f"""
    Fantastic! with a side of Awesome sauce. 😎🔥\n\nYour booking has been successfully confirmed with Booking ID: *{booking_id}*.\n\nOur executive will reach out to you within the next 3 business hours to confirm your booking details and address any questions or concerns you may have.\n\nWe will send you the available payment options shortly, allowing you to choose from a variety of convenient payment methods.\n\n*IMPORTANT: Kindly note that payment for the booking is required to be completed 24 hours prior to the scheduled work slot. Failure to make the payment within this time frame will result in the cancellation of your booking.*\n\nThank you for choosing *ServeEase*!! We look forward to serving you.
    """
    return message

# Helper function to sanitize input
def sanitize_input(input_str):
    if input_str is None:
        return None
    # Perform sanitization to prevent injection or malformed data
    return input_str.strip()

# Helper function to validate button payload
def validate_button_payload(payload):
    # Add logic to ensure payload meets expected format, e.g., JSON schema validation or regex
    return isinstance(payload, str) and len(payload) > 0


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
        f = request.form  # Access the incoming form data from the request
        msg = sanitize_input(f.get('Body'))  # Sanitize the message body to prevent injection or malformed data
        sender = f.get('From')  # Extract the sender's ID from the form data
        message_type = f.get('MessageType')  # Determine the type of incoming message

        # Ensure that the sender ID is present
        if sender is None or sender == "":
            print(f"Sender ID not found. Full request data: {f.to_dict()}")
            return "Error", 500

        # Handle interactive message types
        if message_type == "interactive":
            button_payload = f.get('ButtonPayload')  # Get button payload if present
            list_id = f.get('ListId')  # Get list ID if present
            
            if button_payload is not None:
                # Validate the button payload to ensure it's in the expected format
                if not validate_button_payload(button_payload):
                    print(f"Invalid button payload: {button_payload}")
                    return "Error", 400

                # Process the button message based on its payload
                response = process_button_msg(button_payload)
                if response == "slot":
                    send_slots(sender)  # Send slot-related response to the sender
                elif response == "employee":
                    send_employees(sender)  # Send employee-related response to the sender

            elif list_id is not None:
                # Process the list message based on its ID
                response = process_list_msg(list_id)
                if response == "date":
                    send_dates(sender)  # Send available dates to the sender
                elif response == "done":
                    confirmation = generate_booking_message()  # Generate a booking confirmation
                    send_message(confirmation, sender)  # Send the confirmation message to the sender
            else:
                # If no button payload or list ID is found, trigger the fallback
                print(f"Fallback triggered: sending first message to {sender}")
                send_first_message(sender)
        else:
            # Handle non-interactive messages
            if msg is not None and msg != "":
                response = process_msg(msg)  # Process the general text message
                if response == "first":
                    send_first_message(sender)  # Trigger the initial response for the sender
                else:
                    send_message(response, sender)  # Send the processed response to the sender
            else:
                # If the message body is empty or missing, trigger the fallback
                print(f"Fallback triggered: sending first message to {sender}")
                send_first_message(sender)
                
    except Exception as e:
        # Log the exception and include a stack trace for debugging purposes
        import traceback
        print(f"Error processing webhook: {e}\n{traceback.format_exc()}")
        return "Error", 500
    
    return "OK", 200  # Return success response if processing completes without errors


