"""Class for the attribute Reason"""
from uc3m_care.data.attribute.attribute import Attribute

#pylint: disable=too-few-public-methods
class Reason(Attribute):
    """Class for the attribute Reason"""
    _validation_pattern = r"[ a-z A-Z 0-9 , . ]{2,100}"
    _validation_error_message = "the reason is not valid"