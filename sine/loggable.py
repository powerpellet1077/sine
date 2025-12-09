from sine.logger import SineLogger

class Loggable:
    """intended for type hints and to make my code look fancy. adds basic logging functionality to any class super to this one."""
    def __init__(self, logger:SineLogger|None=None):
        self._logger = logger
        try:
            self.err=self._logger.error
            self.info=self._logger.info
            self.crit=self._logger.critical
            self.warn=self._logger.warning
            self.failure=self.__log_failure__
            self.success=self.__log_success__
        except:
            self.err=self.__null__
            self.info=self.__null__
            self.crit=self.__null__
            self.warn=self.__null__
            self.failure=self.__null__
            self.success=self.__null__

    def __log_failure__(self, message):
        self._logger.log("FAILURE", message)

    def __log_success__(self, message):
        self._logger.log("SUCCESS", message)

    def __null__(self, message):
        pass