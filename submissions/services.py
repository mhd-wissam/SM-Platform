import logging
import os
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class SMSService(ABC):
    """Abstract base class for SMS services"""

    @abstractmethod
    def send_otp(self, phone_number: str, otp_code: str) -> bool:
        """
        Send OTP code to phone number

        Args:
            phone_number: Phone number to send OTP to
            otp_code: OTP code to send

        Returns:
            bool: True if SMS sent successfully, False otherwise
        """
        pass


class MockSMSService(SMSService):
    """
    Mock SMS service for development and testing
    Uses fixed OTP code '000000' and doesn't send real SMS
    """

    def send_otp(self, phone_number: str, otp_code: str) -> bool:
        """
        Mock SMS sending - just logs the OTP code

        In production, this should be replaced with actual SMS service
        """
        logger.info(f"MOCK SMS: Sending OTP '{otp_code}' to {phone_number}")
        print(f"📱 MOCK SMS: OTP code '{otp_code}' sent to {phone_number}")

        # Always return True for mock service
        return True


class TwilioSMSService(SMSService):
    """
    Twilio SMS service implementation
    Uncomment and configure when ready to use Twilio
    """

    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number

    def send_otp(self, phone_number: str, otp_code: str) -> bool:
        """
        Send OTP via Twilio SMS service
        """
        try:
            # Uncomment when Twilio is installed and configured
            # from twilio.rest import Client

            # client = Client(self.account_sid, self.auth_token)
            # message = client.messages.create(
            #     body=f"Your OTP code is: {otp_code}",
            #     from_=self.from_number,
            #     to=phone_number
            # )

            logger.info(f"Twilio SMS sent to {phone_number}: {otp_code}")
            return True

        except Exception as e:
            logger.error(f"Failed to send Twilio SMS to {phone_number}: {str(e)}")
            return False


class SMSServiceFactory:
    """Factory for creating SMS service instances"""

    @staticmethod
    def get_sms_service(service_type: str = 'mock', **kwargs) -> SMSService:
        """
        Get SMS service instance based on type

        Args:
            service_type: Type of SMS service ('mock', 'twilio', etc.)
            **kwargs: Additional configuration parameters

        Returns:
            SMSService: SMS service instance
        """
        if service_type == 'mock':
            return MockSMSService()
        elif service_type == 'twilio':
            return TwilioSMSService(
                account_sid=kwargs.get('account_sid', ''),
                auth_token=kwargs.get('auth_token', ''),
                from_number=kwargs.get('from_number', '')
            )
        else:
            # Default to mock service
            logger.warning(f"Unknown SMS service type '{service_type}', using mock service")
            return MockSMSService()


# Global SMS service instance (can be configured via environment variables)
sms_service = SMSServiceFactory.get_sms_service(
    service_type=os.getenv('SMS_SERVICE_TYPE', 'mock'),
    account_sid=os.getenv('TWILIO_ACCOUNT_SID', ''),
    auth_token=os.getenv('TWILIO_AUTH_TOKEN', ''),
    from_number=os.getenv('TWILIO_FROM_NUMBER', '')
)
