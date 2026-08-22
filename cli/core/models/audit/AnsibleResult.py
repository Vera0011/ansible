from dataclasses import dataclass


@dataclass
class AnsibleResult:
    """
    Class that returns an Ansible result

    Parameters
    ----------
    returncode: int
        Status code returned (integer) - 1 or 2
    stdout: str
        Standard output (code 1)
    stderr: str
        Standard error (code 2)
    """

    returncode: int
    stdout: str
    stderr: str

    @property
    def success(self) -> bool:
        return self.returncode == 0

    @property
    def error(self) -> str:
        return self.stderr

    @property
    def out(self) -> str:
        return self.stdout
