import argparse
import json
import os
import pwd
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from prompt_toolkit.application.current import get_app
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.filters import Condition
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

SHELL_BUILTINS = {
    ".", ":", "[", "break", "cd", "continue", "echo", "eval", "exec",
    "exit", "export", "getopts", "pwd", "read", "readonly", "return",
    "set", "shift", "test", "times", "trap", "umask", "unset",
}

class AvailableCommandSuggest(AutoSuggest):
    def __init__(self, history, command_names):
        self.history = history
        self.command_names = sorted(set(command_names))

    @staticmethod
    def command_is_available(command):
        return command in SHELL_BUILTINS or shutil.which(command) is not None

    def get_suggestion(self, buffer, document):
        prefix = document.text_before_cursor
        if not prefix:
            return None

        for entry in reversed(self.history.get_strings()):
            if not entry.startswith(prefix) or len(entry) == len(prefix):
                continue

            try:
                words = shlex.split(entry)
            except ValueError:
                continue

            if words and self.command_is_available(words[0]):
                return Suggestion(entry[len(prefix):])

        if " " not in prefix:
            for command in self.command_names:
                if (
                    command.startswith(prefix)
                    and len(command) > len(prefix)
                    and self.command_is_available(command)
                ):
                    return Suggestion(command[len(prefix):])

        return None

CONFIG_DIR = Path.home() / "Library" / "Application Support" / "ginko-terminal"
CATALOG_PATH = CONFIG_DIR / "commands.json"
DEFAULT_LIBRARY_PATH = Path.home() / "Downloads" / "VSCode_AI_Full_Paste_Ready.md"
DEFAULT_INSTALL_PATH = Path.home() / "ginko_terminal.py"
ZSHRC_PATH = Path.home() / ".zshrc"
ZSH_START_MARKER = "# >>> ginko-terminal setup >>>"
ZSH_END_MARKER = "# <<< ginko-terminal setup <<<"

def extract_command_names(library_text):
    names = set()
    for line in library_text.splitlines():
        match = re.match(r"^\s*\|\s*([^|]+)\|", line)
        if not match:
            continue
        for item in re.split(r"\s+/\s+", match.group(1)):
            command_match = re.search(r"`([^`]+)`", item)
            if not command_match:
                continue
            words = command_match.group(1).strip().split(maxsplit=1)
            if not words:
                continue
            command = words[0]
            if re.fullmatch(r"[A-Za-z0-9_.+-]+", command):
                names.add(command)
    return sorted(names)


def get_history_path(root_session=False):
    home = Path(pwd.getpwuid(0).pw_dir) if root_session else Path.home()
    return home / ".ginko_terminal_history"


def load_command_names(root_session=False):
    catalog_paths = [CATALOG_PATH]
    if root_session:
        usernames = [os.environ.get("SUDO_USER")]
        try:
            usernames.append(pwd.getpwuid(Path(__file__).stat().st_uid).pw_name)
        except KeyError:
            pass

        for username in usernames:
            if not username or username == "root":
                continue
            try:
                user_home = Path(pwd.getpwnam(username).pw_dir)
            except KeyError:
                continue
            candidate = user_home / "Library" / "Application Support" / "ginko-terminal" / "commands.json"
            if candidate not in catalog_paths:
                catalog_paths.append(candidate)

    for catalog_path in catalog_paths:
        try:
            names = json.loads(catalog_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(names, list):
            return [name for name in names if isinstance(name, str)]
    return []


def install_zsh_function(auto_start=False, script_path=None):
    script_path = shlex.quote(script_path or str(Path(__file__).resolve()))
    python_path = shlex.quote(sys.executable)
    block = (
        f"{ZSH_START_MARKER}\n"
        f"ginko() {{\n  {python_path} {script_path} \"$@\"\n"
        f"}}\n{ZSH_END_MARKER}"
    )
    if auto_start:
        block = block.replace(
            ZSH_END_MARKER,
            "if [[ -o interactive ]]; then\n  ginko\nfi\n" + ZSH_END_MARKER,
        )
    existing = ZSHRC_PATH.read_text() if ZSHRC_PATH.exists() else ""
    pattern = re.compile(
        rf"(?ms)^{re.escape(ZSH_START_MARKER)}\n.*?"
        rf"^{re.escape(ZSH_END_MARKER)}\n?"
    )
    if pattern.search(existing):
        updated = pattern.sub(block + "\n", existing)
    else:
        updated = existing.rstrip() + ("\n\n" if existing.strip() else "")
        updated += block + "\n"

    backup_path = ZSHRC_PATH.with_name(".zshrc.ginko-backup")
    if ZSHRC_PATH.exists() and not backup_path.exists():
        shutil.copy2(ZSHRC_PATH, backup_path)
    ZSHRC_PATH.write_text(updated)
    print(f"Added the ginko function to {ZSHRC_PATH}.")
    if backup_path.exists():
        print(f"Backup: {backup_path}")
    print("Run `source ~/.zshrc`, then start Ginko with `ginko`.")


def setup_wizard():
    if sys.platform != "darwin":
        raise SystemExit("The setup wizard currently supports macOS with zsh.")

    print("Ginko Terminal setup")
    print("Startup behavior is optional; exiting Ginko returns you to zsh.")
    install_input = input(
        f"Install program path [{DEFAULT_INSTALL_PATH}]: "
    ).strip()
    install_path = Path(
        os.path.expanduser(install_input) if install_input else DEFAULT_INSTALL_PATH
    )
    if install_input and (install_input.endswith(os.sep) or install_path.is_dir()):
        install_path /= Path(__file__).name
    install_path = install_path.resolve()
    source_path = Path(__file__).resolve()
    if install_path != source_path:
        if install_path.exists() and install_path.read_bytes() != source_path.read_bytes():
            replace = input(
                f"{install_path} exists. Replace it? [y/N]: "
            ).strip().lower()
            if replace not in {"y", "yes"}:
                install_path = source_path
                print(f"Using the current program at {source_path}.")
        if install_path != source_path:
            install_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, install_path)
            print(f"Installed Ginko at {install_path}.")

    library_input = input(
        f"Command library path [{DEFAULT_LIBRARY_PATH}]: "
    ).strip()
    library_path = Path(
        os.path.expanduser(library_input) if library_input else DEFAULT_LIBRARY_PATH
    )

    if library_path.is_file():
        names = extract_command_names(library_path.read_text())
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CATALOG_PATH.write_text(json.dumps(names, indent=2) + "\n")
        available_count = sum(
            AvailableCommandSuggest.command_is_available(name) for name in names
        )
        print(
            f"Imported {len(names)} command names; "
            f"{available_count} are available on this Mac."
        )
    else:
        print(f"No library found at {library_path}; setup will continue without it.")

    answer = input("Add the `ginko` command to ~/.zshrc? [Y/n]: ").strip().lower()
    if answer in {"", "y", "yes"}:
        auto_start = input(
            "Start Ginko in each interactive zsh session? [y/N]: "
        ).strip().lower() in {"y", "yes"}
        install_zsh_function(
            auto_start=auto_start,
            script_path=str(install_path),
        )
        if auto_start:
            print("Ginko will start whenever an interactive zsh session opens.")
    else:
        print("Skipped the zsh configuration change.")


def run_prompt():
    root_session = os.geteuid() == 0
    history = FileHistory(str(get_history_path(root_session)))
    command_names = load_command_names(root_session)
    if root_session:
        print("ROOT SESSION: commands run with root privileges.")

    suggest = AvailableCommandSuggest(history, command_names)
    style = Style.from_dict({"autosuggestion": "fg:#777777"})
    key_bindings = KeyBindings()

    @Condition
    def suggestion_available():
        buffer = get_app().current_buffer
        return (
            buffer.suggestion is not None
            and bool(buffer.suggestion.text)
            and buffer.document.is_cursor_at_the_end
        )

    @key_bindings.add("tab", filter=suggestion_available)
    def accept_suggestion(event):
        suggestion = event.current_buffer.suggestion
        if suggestion:
            event.current_buffer.insert_text(suggestion.text)

    session = PromptSession(
        history=history,
        auto_suggest=suggest,
        style=style,
        key_bindings=key_bindings,
    )

    while True:
        try:
            prompt = "gzh# " if root_session else "gzh> "
            command = session.prompt(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not command:
            continue
        if command in {"exit", "quit"}:
            break

        parts = shlex.split(command)
        if parts[0] == "cd" and len(parts) <= 2:
            os.chdir(os.path.expanduser(parts[1] if len(parts) == 2 else "~"))
            continue

        subprocess.run(command, shell=True)


def main():
    parser = argparse.ArgumentParser(description="Command preview prompt for macOS/Linux")
    parser.add_argument("--setup", action="store_true", help="run the setup wizard")
    args = parser.parse_args()
    if args.setup:
        setup_wizard()
    else:
        run_prompt()


if __name__ == "__main__":
    main()
