# Ginko Terminal

Ginko is a small Python command prompt with gray inline suggestions from command history and an optional command catalog. Suggestions are shown only for commands available on the current machine. Press Tab or Right Arrow to accept one.

## Requirements

- Python 3
- `prompt_toolkit` 3.x
- macOS or Linux with an interactive terminal

Install the dependency:

```sh
python3 -m pip install -r requirements.txt
```

## Run

Start the prompt directly:

```sh
python3 ginko_terminal.py
```

On macOS, the optional setup wizard can import command names from a Markdown reference and add a `ginko` function to zsh:

```sh
python3 ginko_terminal.py --setup
```

The wizard defaults to installing a copy at `~/ginko_terminal.py`. It can optionally start Ginko in interactive zsh sessions. Linux users can run the program directly; the setup wizard is macOS-only.

## Root Sessions

To run Ginko from an existing root shell, start it with a Python interpreter that has `prompt_toolkit` installed:

```sh
sudo -i
python3 /Users/your-user/ginko_terminal.py
```

The prompt changes to `gzh#` and Ginko prints a root-session warning. Every command entered in that session runs with root privileges. Root history is stored separately from the regular user's history. When available, Ginko reuses the invoking user's command catalog.

Prefer running Ginko as a regular user and using `sudo` only for individual commands that require it.

## Tests

Run the unit tests with:

```sh
python3 -m unittest discover -s tests -v
```

## Safety Notes

- Ginko executes entered commands through the system shell. Suggestions only check whether a command name is available; they do not validate arguments or guarantee a command is safe.
- In a root session, commands have root privileges and can modify or damage the system.
- The command catalog contains names only. Availability varies by operating system, installed packages, shell, and `PATH`.

## License

Ginko is distributed under the MIT License. See [LICENSE](LICENSE).