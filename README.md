# For-her

A simple responsive Flask + uv website where your girlfriend can choose a date.

![website_view](screenshots/landing.png)

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- [**python 3.13**](https://www.python.org/downloads/)
- [**uv**](https://github.com/astral-sh/uv#installation)
- [**git**](https://git-scm.com/install/)

## Project structure

```text
for-her/
├── src/
│   ├── app.py                 # Flask app, routes, invite config
│   ├── log.py                 # logging setup
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── base.html          # page shell
│       └── main/
│           ├── _card.html     # shared card layout
│           ├── index.html     # date + activity form
│           └── confirmation.html
├── pyproject.toml             # project metadata and tools
├── uv.lock
├── .pre-commit-config.yaml
├── .gitignore
├── LICENSE
└── README.md
```

## How to run
1. Clone the repo.
```bash
git clone https://github.com/Ulad/for-her.git
```
2. Navigate to the source directory, all application code lives inside `src/`.
```bash
cd for-her/src
```
3. Run the Flask development server via `uv`. This guarantees your app uses the right environment.
```bash
uv run flask run
```
> [!TIP]
That's it! You can use:
> - `--debug` to enable auto-reload on code changes
> - `--port=5000` to change default port.
> - `--host=0.0.0.0` to make the server publicly available
