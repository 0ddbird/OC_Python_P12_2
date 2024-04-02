# Just documentation: https://just.systems/man/en/

src:= "epic_events"
RS_APP:= "bubble"


default:
	@just --list

@pypath:
	echo "export PYTHONPATH=$PYTHONPATH:$(pwd)"
	export PYTHONPATH=$PYTHONPATH:$(pwd)

@venv:
	source .venv/bin/activate

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

# ================== BUBBLE COMMANDS ====================

@release:
	cd {{RS_APP}} && cargo build --release && cp target/release/{{RS_APP}} ~/bin/{{RS_APP}}


# ================ FORMATTING COMMANDS ==================
@format:
	ruff check --fix {{src}}
	isort {{src}}
	ruff format {{src}}
	python3 -m black {{src}}
	cd {{RS_APP}} && cargo fmt
