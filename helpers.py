import random
from session_manager import set_session_value

# Helper function to sanitize input
def sanitize_input(input_str):
    """
    Sanitize the input to prevent injection or malformed data.
    """
    if input_str is None:
        return None
    return input_str.strip()

# Helper function to validate button payload
def validate_input(payload):
    """
    Validate the input payload to ensure it is a non-empty string.
    """
    return isinstance(payload, str) and len(payload) > 0


# Function to generate a booking confirmation message
def generate_booking_message(session_data):
    # Generate a random 6-digit booking ID
    booking_id = random.randint(250000, 259999)
    set_session_value(session_data, 'orderid', booking_id)
    # Construct the message
    message = f"""
    Fantastic! with a side of Awesome sauce. 😎🔥\n\nYour booking has been successfully confirmed with Booking ID: *{booking_id}*.\n\nOur executive will reach out to you within the next 3 business hours to confirm your booking details and address any questions or concerns you may have.\n\nWe will send you the available payment options shortly, allowing you to choose from a variety of convenient payment methods.\n\n*IMPORTANT: Kindly note that payment for the booking is required to be completed 24 hours prior to the scheduled work slot. Failure to make the payment within this time frame will result in the cancellation of your booking.*\n\nThank you for choosing *ServeEase*!! We look forward to serving you.
    """
    return message
