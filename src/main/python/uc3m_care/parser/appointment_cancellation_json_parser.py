"""Subclass of JsonParer for parsing inputs"""
from uc3m_care.parser.json_parser import JsonParser

class AppointmentCancellationJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs"""

    BAD_DATE_SIGNATURE_LABEL_ERROR = "Bad label date signature"
    BAD_CANCELLATION_TYPE_LABEL_ERROR = "Bad label cancelation type"
    BAD_REASON_LABEL_ERROR = "Bad label reason"
    DATE_SIGNATURE_KEY = "date_signature"
    CANCELLATION_TYPE_KEY = "cancelation_type"
    REASON_KEY = "reason"

    _JSON_KEYS = [DATE_SIGNATURE_KEY, CANCELLATION_TYPE_KEY, REASON_KEY]
    _ERROR_MESSAGES = [BAD_DATE_SIGNATURE_LABEL_ERROR,
                       BAD_CANCELLATION_TYPE_LABEL_ERROR,
                       BAD_REASON_LABEL_ERROR]
