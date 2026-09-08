class EasySecError(Exception):
    """
    Base exception for expected errors
    """


class DependencyError(EasySecError):
    """
    A required external dependency is missing
    """


class AuditError(EasySecError):
    """
    An audit could not be executed
    """


class RepositoryError(EasySecError):
    """
    The root folder could not be found
    """
