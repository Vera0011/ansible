from __future__ import annotations

import sys, os

from dataclasses import dataclass
from pathlib import Path
from rich.console import Console

from app.core.exceptions import RepositoryError


@dataclass(frozen=True)
class Context:
    """
    Runtime context for a command

    Attributes
    ----------
    root: Path
        Main application path
    playbooks_dir: Path
        Path were are located playbooks
    roles_dir: Path
        Path were are located roles
    inventory_dir: Path
        Path were are located inventories
    reports_dir: Path
        Path were are located reports
    console: Console
        A Console instance (for logging)
    """

    root: Path
    playbooks_dir: Path
    roles_dir: Path
    inventory_dir: Path
    reports_dir: Path

    ansible_conf_path: Path
    console: Console

    @classmethod
    def discover(cls) -> Context:
        """
        Discovers the main repository path

        Returns
        -------
        Context
            The context with the correct main path
        """

        current = Path.cwd().resolve()

        for candidate in (current, *current.parents):
            if cls._get_paths(candidate)[0]:
                return cls.from_root(candidate)

        if getattr(sys, "frozen", False):
            bundled_root = Path(getattr(sys, "_MEIPASS", ""))

            if cls._get_paths(bundled_root)[0]:
                return cls.from_root(
                    bundled_root,
                    reports_dir=Path.cwd() / "reports",
                )

        raise RepositoryError(
            "Could not find the root repository.\n"
            "Run this command from the root repository."
        )

    @classmethod
    def from_root(cls, root: Path, reports_dir: Path | None = None) -> Context:
        """
        Creates the context based on a provided path

        Parameters
        ----------
        root: Path
            Main path provided
        reports_dir: Path | None
            Override for where reports are written (e.g. when root is a
            read-only bundled/temp directory and reports must go elsewhere)

        Returns
        -------
        Context
            The generated context
        """

        cls._configure_ansible_environment()
        paths = cls._get_paths(root)

        playbooks_dir, roles_dir, inventory_dir, ansible_conf_path = paths[1]

        return cls(
            root=root,
            console=Console(),
            playbooks_dir=playbooks_dir,
            roles_dir=roles_dir,
            inventory_dir=inventory_dir,
            ansible_conf_path=ansible_conf_path,
            reports_dir=reports_dir if reports_dir != None else cls.inventory_dir,
        )

    @classmethod
    def _get_paths(cls, root: Path) -> tuple[bool, list[str]]:
        """
        Checks if the selected path is the main path or not

        Parameters
        ----------
        root: Path
            The path to check

        Returns
        -------
        bool
            If the specified path is the main path or not
        """

        playbooks = root / "playbooks"
        roles = root / "playbooks" / "roles"
        inventory = root / "inventory"
        ansible = root / "ansible.cfg"

        if getattr(sys, "frozen", False):
            return (
                all(
                    (
                        playbooks.is_dir(),
                        roles.is_dir(),
                        inventory.is_dir(),
                        ansible.is_file(),
                    )
                ),
                [playbooks, roles, inventory, ansible],
            )

        else:
            roles = root / "roles"

            return (
                all(
                    (
                        playbooks.is_dir(),
                        roles.is_dir(),
                        inventory.is_dir(),
                        ansible.is_file(),
                    )
                ),
                [playbooks, roles, inventory, ansible],
            )

    @classmethod
    def _configure_ansible_environment(cls) -> None:
        """
        Configures correctly the binaries (ansible-playbook) - Makes them discoverable
        """

        if not getattr(sys, "frozen", False):
            return

        root = Path(sys._MEIPASS)
        ansible_bin = root / "ansible" / "bin"

        if not ansible_bin.is_dir():
            raise RuntimeError(f"Bundled Ansible binaries not found: {ansible_bin}")

        os.environ["PATH"] = str(ansible_bin) + os.pathsep + os.environ.get("PATH", "")

    @classmethod
    def _load_invenvory(cls) -> None:
        """ """

    @property
    def audit_playbook(self) -> Path:
        """
        Returns the audit playbook from this context

        Returns
        -------
        Path
            The built path
        """

        return self.playbooks_dir / "audit.yml"

    @property
    def check_playbook(self) -> Path:
        """
        Returns the audit playbook from this context

        Returns
        -------
        Path
            The built path
        """

        return self.playbooks_dir / "hardening.yml"

    @property
    def hardening_playbook(self) -> Path:
        """
        Returns the audit playbook from this context

        Returns
        -------
        Path
            The built path
        """

        return self.playbooks_dir / "hardening.yml"
