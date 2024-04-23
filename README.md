# OC_Python_P12_2

## Introduction

This is a command-line CRM for Epic Events, an Event company.

## Setup

1. Clone the repo

    ```bash
    git clone https://github.com/0ddbird/OC_Python_P12_2.git
    ```

2. Install Just

    Just is like Make but better (more options and depth).

    On Arch Linux
    ```bash
    pacman -S just
    ```

    On Debian/Ubuntu: 
    ```bash
    git clone https://mpr.makedeb.org/just
    ```
    ```bash
    cd just
    ```
    ```bash
    makedeb -si
    ```

    ```bash
    port install just
    ```
    All other supported OS are listed here:
    from: https://github.com/casey/just

3. Create a virtual environment
    ```bash
    python -m venv venv
    ```

    then activate it, either with:

    ```bash
    source venv/bin/activate
    ```
    or with:
    ```bash
    just venv
    ```

4. Install the requirements

    ```bash
    pip install -r ./requirements/base.txt
    ```

5. Setup the DB

    ```bash
    just setup-db
    ```

6. Create the superuser

    ```bash
    just create-su
    ```

7. Install Rust
   
    On UNIX (Linux/MacOS):
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```
    On Windows see other installation methods:
    https://forge.rust-lang.org/infra/other-installation-methods.html

8. Build the JWT local storage
    ```bash
    just release
    ```

# Usage

Login as admin

By default, username and password are `admin`

```bash
just app login
```

You can also see available commands with

```bash
just app --help
```