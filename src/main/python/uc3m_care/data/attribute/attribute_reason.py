"""Class for the attribute Reason"""
from uc3m_care.data.attribute.attribute import Attribute

#pylint: disable=too-few-public-methods
class Reason(Attribute):
    """Class for the attribute Reason"""
    _validation_pattern = r"^(?=^.{2,100}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$"
    _validation_error_message = "the reason is not valid"