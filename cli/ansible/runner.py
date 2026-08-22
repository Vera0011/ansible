from __future__ import annotations

from pathlib import Path
from cli.core.context import Context
from ansible.cli.playbook import PlaybookCLI
from cli.core.models.audit.AnsibleResult import AnsibleResult


class AnsibleWrapper:
    """
    Wrapper around ansible-playbook binary
    """

    def __init__(self, context: Context):
        self.context = context

    def run(
        self,
        playbook: str,
        *,
        inventory: str,
        ssh_key: str,
        ssh_user: str,
        check: bool,
        diff: bool,
    ) -> AnsibleResult:
        """
        Executes a playbook given the specified parameters

        Parameters
        ----------
        playbook: str
            Path of the selected playbook
        inventory: str
            Path of the selected inventory
        ssh_key: str
            If an access key must be used
        ssh_user: str
            If an access user must be used
        check: bool
            If the parameter 'check' should be enabled or not
        diff: bool
            If the parameter 'diff' should be enabled or not

        Returns
        -------
        AnsibleResult
            The Ansible result as object
        """

        command = [
            "ansible-playbook",
            "-i",
            str(inventory),
            str(playbook),
            "-e",
            "ansible_python_interpreter=auto_silent",
        ]

        if check:
            command.append("--check")

        if diff:
            command.append("--diff")

        if ssh_key:
            command.extend(
                [
                    "--private-key",
                    str(Path(ssh_key).resolve()),
                ]
            )

        if ssh_user:
            command.extend(
                [
                    "--user",
                    ssh_user,
                ]
            )

        cli = PlaybookCLI(command)
        cli.parse()
        completed = cli.run()

        return AnsibleResult(
            returncode=completed or 0,
            stdout="",
            stderr="",
        )
