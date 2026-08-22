from __future__ import annotations
import sys, os
from dataclasses import dataclass
from pathlib import Path
from rich.console import Console

from cli.core.exceptions import RepositoryError


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
    ansible_conf: Path
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
            if cls._is_repository(candidate):
                return cls.from_root(candidate)

        if getattr(sys, "frozen", False):
            bundled_root = Path(getattr(sys, "_MEIPASS", ""))
            if cls._is_repository(bundled_root):
                return cls.from_root(
                    bundled_root,
                    reports_dir=Path.cwd() / "reports",
                )

        raise RepositoryError(
            "Could not find the root repository.\n"
            "Run this command from the root repository."
        )

    @classmethod
    def from_root(cls, root: Path, *, reports_dir: Path | None = None) -> Context:
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

        root = root.resolve()

        if not cls._is_repository(root):
            raise RepositoryError(
                f"{root} is not the root repository.\n"
                "Run this command from the root repository."
            )

        cls.configure_ansible_environment()

        return cls(
            root=root,
            console=Console(),
            playbooks_dir=root / "playbooks",
            roles_dir=(
                root / "playbooks" / "roles"
                if getattr(sys, "frozen", False)
                else root / "roles"
            ),
            inventory_dir=root / "inventory",
            ansible_conf=root / "ansible.cfg",
            reports_dir=reports_dir or (root / "reports"),
        )

    @classmethod
    def _is_repository(cls, root: Path) -> bool:
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

        if getattr(sys, "frozen", False):
            return all(
                (
                    (root / "playbooks").is_dir(),
                    (root / "playbooks" / "roles").is_dir(),
                    (root / "inventory").is_dir(),
                    (root / "ansible.cfg").is_file(),
                )
            )
        else:
            return all(
                (
                    (root / "playbooks").is_dir(),
                    (root / "roles").is_dir(),
                    (root / "inventory").is_dir(),
                    (root / "ansible.cfg").is_file(),
                )
            )

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

    @classmethod
    def configure_ansible_environment(cls) -> None:
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
