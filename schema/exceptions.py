class NotFoundException(Exception):
    """The requested entity was not found from MLB's data"""
    pass

class UnexpectedResponseException(Exception):
    """MLB returned something unexpected"""
    pass