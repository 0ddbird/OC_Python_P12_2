# Just documentation: https://just.systems/man/en/

src:= "src"
MANDALA_PATH:= "mandala"


default:
	@just --list

@pypath:
	echo "export PYTHONPATH=$PYTHONPATH:$(pwd)"
	export PYTHONPATH=$PYTHONPATH:$(pwd)

# ================ EPIC EVENTS COMMANDS ==================

# Set up the database
@setup-db:
	python scripts/setup_db.py

# Create superuser
@create-su:
	python scripts/create_su.py

# Run the server
@app *additional_args:
	python -m {{src}} {{additional_args}}

# ================== MANDALA COMMANDS ====================

# Run mandala
@mandala:
	python -m {{src}} runmandala

# Build mandala binary and move it into the epic_events directory
@mandala-build:
	cd {{MANDALA_PATH}} && cargo build --release && cp target/release/mandala ../epic_events/mandala


# ================ FORMATTING COMMANDS ==================
@format:
	ruff check --fix {{src}}
	isort {{src}}
	ruff format {{src}}
	python3 -m black {{src}}
