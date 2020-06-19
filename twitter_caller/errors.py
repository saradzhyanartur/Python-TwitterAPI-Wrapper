from typing import Optional, Union


class Error(Exception):
    """Base class for errors"""
    pass
 

class ClientPermissionError(Error):
    """Raised when the client is unable to Authenticate.
    
    Attributes:
        message -- the custom part of message the error displays
        reference -- the link to the appropraite resource
    """

    def __init__(self, message: str, reference: Optional[Union[str, None]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.reference = reference

    def __str__(self) -> str:
        return (
            f"[MESSAGE] -- {self.message}. "
            f"[REFERENCE] -- {self.reference} "
        )


class StatusCodeError(Error):
    """Raised when the the response from the API does not return 200.
    
    Attributes:
        message -- the custom part of message the error displays
        status_code -- the response code
        reference -- the link to the appropraite resource
    """

    def __init__(self, status_code: str, 
                    reference: Optional[str] = 'https://developer.twitter.com/en/docs',
                    message: Optional[str] = "Twitter's API did not return 200. Please double check the passed in arguments.") -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.reference = reference

    def __str__(self) -> str:
        return (
            f"""[MESSAGE] -- {self.message}. """
            f"[STATUS CODE] -- {self.status_code} "
            f"[REFERENCE] -- {self.reference} "
        )

