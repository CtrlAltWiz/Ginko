import json
import pwd
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ginko_terminal


class EmptyHistory:
    def get_strings(self):
        return []


class GinkoTerminalTests(unittest.TestCase):
    def test_extract_command_names_splits_alternatives_not_paths(self):
        library = "\n".join(
            [
                "| `gzip` / `gunzip` | Compression | example | note |",
                "| `readlink -f` | Resolve link | example | note |",
                "| `ls -l /dev/disk/by-id` | List devices | example | note |",
            ]
        )

        self.assertEqual(
            ["gunzip", "gzip", "ls", "readlink"],
            ginko_terminal.extract_command_names(library),
        )

    def test_catalog_suggests_only_available_commands(self):
        suggest = ginko_terminal.AvailableCommandSuggest(
            EmptyHistory(), ["cat", "not-installed-ginko-test-command"]
        )
        with patch.object(
            suggest,
            "command_is_available",
            side_effect=lambda command: command == "cat",
        ):
            suggestion = suggest.get_suggestion(
                None, SimpleNamespace(text_before_cursor="ca")
            )
            unavailable = suggest.get_suggestion(
                None, SimpleNamespace(text_before_cursor="not-")
            )

        self.assertEqual("t", suggestion.text)
        self.assertIsNone(unavailable)

    def test_root_history_uses_root_home(self):
        expected = Path(pwd.getpwuid(0).pw_dir) / ".ginko_terminal_history"
        self.assertEqual(expected, ginko_terminal.get_history_path(root_session=True))

    def test_root_session_falls_back_to_script_owners_catalog(self):
        script_owner = pwd.getpwuid(
            Path(ginko_terminal.__file__).stat().st_uid
        ).pw_name
        with tempfile.TemporaryDirectory() as directory:
            user_home = Path(directory)
            catalog = (
                user_home
                / "Library"
                / "Application Support"
                / "ginko-terminal"
                / "commands.json"
            )
            catalog.parent.mkdir(parents=True)
            catalog.write_text(json.dumps(["ls", "diskutil"]))

            with (
                patch.object(ginko_terminal, "CATALOG_PATH", user_home / "missing.json"),
                patch.dict(ginko_terminal.os.environ, {"SUDO_USER": ""}),
                patch.object(
                    ginko_terminal.pwd,
                    "getpwnam",
                    return_value=SimpleNamespace(pw_dir=str(user_home)),
                ),
            ):
                names = ginko_terminal.load_command_names(root_session=True)

        self.assertEqual(["ls", "diskutil"], names)


if __name__ == "__main__":
    unittest.main()
