# Ginko Terminal

<p align="center">
  <img src="assets/ginkgo-icon.png" alt="Ginko Terminal — golden pixel-art ginkgo leaf" width="220">
</p>

<p align="center">
  A lightweight, history-aware terminal companion for macOS and Linux.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=flat-square" alt="Python 3">
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux-lightgrey?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT License">
</p>

---

## Hello, Ginko!

The terminal is one of the most powerful tools on your computer. But remembering every command you've ever typed is another story.

Ginko is a small, Python-powered interactive terminal that makes everyday command-line work a little easier. It remembers commands you've used, offers subtle inline suggestions, and helps you spend less time typing the same things over and over.

No complicated interface or unnecessary bells and whistles. Just a familiar terminal with a few thoughtful conveniences.

### What's Inside?

- **Smart Suggestions** — See subtle gray command completions as you type.
- **Command History** — Reuse commands from previous sessions without digging through your history.
- **Tab to Complete** — Press `Tab` or `Right Arrow` to accept an inline suggestion.
- **Optional Command Library** — Import command names from a Markdown reference to expand available suggestions.
- **System-Aware Suggestions** — Ginko checks whether the suggested command is available on your machine.
- **Root Session Support** — Use Ginko from an existing root shell, with a distinct prompt and separate history.
- **Lightweight by Design** — Built with Python and `prompt_toolkit`, without a heavyweight application framework.

Ginko keeps things simple, just as a terminal should.

---

## A Little Look Around

Ginko's suggestions appear directly beside your input in subtle gray text, ready when you need them and out of the way when you don't.

**Example 1**

<img width="260" height="42" alt="Ginko Terminal inline command suggestion example" src="https://github.com/user-attachments/assets/9915b64e-7ce3-4593-ac8f-1c5316e219df" />

**Example 2**

<img width="278" height="46" alt="Ginko Terminal command completion example" src="https://github.com/user-attachments/assets/66715a6a-4e5f-48cf-a5c9-99b520489fb7" />

Start typing, spot a suggestion, and press `Tab` or `Right Arrow` to complete it.

---

### Requirements

Before getting started, you'll need:

- Python 3
- `prompt_toolkit` 3.x
- macOS or Linux
- An interactive terminal

### 1. Install Dependencies

From the project directory, run:

```bash
python3 -m pip install -r requirements.txt
```

### 2. Launch Ginko

Start the interactive terminal:

```bash
python3 ginko_terminal.py
```

And you're in.

Ginko will begin offering suggestions as you type, based on your command history and any configured command catalog.

### 3. Optional macOS Setup

For macOS users, Ginko includes a setup wizard to make things a little more convenient.

```bash
python3 ginko_terminal.py --setup
```

The wizard can:

- Install a copy of Ginko at `~/ginko_terminal.py`.
- Import command names from a Markdown reference.
- Add a `ginko` function to your zsh configuration.
- Optionally start Ginko automatically in interactive zsh sessions.

Once configured, launch it using:

```bash
ginko
```

**Linux users:** Ginko works directly through Python. The setup wizard is currently available for macOS only.

---

## How Suggestions Work

Ginko uses two sources to offer inline completions:

**1. Your Command History**

Commands you've previously entered can become suggestions the next time you type.

**2. Your Command Catalog**

You can optionally provide a Markdown reference containing command names. Ginko uses these names to expand its completion options.

Before suggesting a command, Ginko checks whether the command is available in the current environment.

This helps keep suggestions relevant to the machine you're actually using.

**A quick note:** Ginko checks command availability, not whether an entire command or its arguments are valid or safe to execute.

---

## Running as Root

For advanced system administration, Ginko can run inside an existing root shell.

```bash
sudo -i
python3 /Users/your-user/ginko_terminal.py
```

Make sure the Python interpreter used in the root session has `prompt_toolkit` installed.

When running with root privileges:

- The prompt changes to `gzh#`.
- A root-session warning appears.
- Command history is stored separately from regular user history.
- Ginko reuses the invoking user's command catalog when available.

**A word of caution:** Every command executed in a root session runs with root privileges.

For everyday work, it's better to run Ginko as a regular user and use `sudo` for individual administrative commands.

A little caution goes a long way when you're one keystroke away from modifying your operating system.

---

## Running Tests

Want to check that everything is behaving?

Run the included unit tests:

```bash
python3 -m unittest discover -s tests -v
```

This runs the test suite using Python's built-in `unittest` framework.

---

## A Few Things Worth Knowing

Ginko works in the terminal interface, which means the commands you enter are executed through your system shell.

Keep these details in mind:

- Ginko does not sandbox commands or prevent destructive operations.
- Inline suggestions do not guarantee that commands are safe.
- Running Ginko as root gives entered commands root privileges.
- Available commands differ between macOS, Linux distributions, installed packages, and configured `PATH` directories.
- The optional command catalog stores command names rather than full command documentation.

As with any terminal, it's worth knowing what a command does before pressing Enter.

---

## Made for the Power-Users

Ginko is part of my collection of small, practical software projects exploring the fun side of computing, with the simple idea of building tools that solve everyday problems, while keeping them approachable and leaving a little room for experimentation along the way.

**Explore more:** [CtrlAltWiz](https://ctrlaltwiz.net)

---

## Credits

The golden ginkgo leaf artwork was created by [Dwiki Satya Dharma](https://www.vecteezy.com/members/dikwazousky) via Vecteezy.

Ginko Terminal is a CtrlAltWiz project.

## License

Ginko is open-source software distributed under the [MIT License](LICENSE).

---

<p align="center">
  <strong>Ginko Terminal</strong>
</p>

<p align="center">
  <em>Curiously crafted by CtrlAltWiz.</em>
</p>
