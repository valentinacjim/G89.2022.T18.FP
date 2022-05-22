"""Subclass of JsonStore for managing the cancelation of appointments"""

from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class CancelAppoimentJsonStore():
    """Implements the singleton pattern"""
    #pylint: disable=invalid-name
    class CancelAppoimentJsonStore(JsonStore):
        """Subclass of JsonStore for managing the Appointments"""
        _FILE_PATH = JSON_FILES_PATH + "store_cancel.json"
        _ID_FIELD = "CancelAppointment__date_signature"
    instance = None

    def __new__ ( cls ):
        if not CancelAppoimentJsonStore.instance:
            CancelAppoimentJsonStore.instance = CancelAppoimentJsonStore.CancelAppoimentJsonStore()
        return CancelAppoimentJsonStore.instance

    def __getattr__ ( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__ ( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)