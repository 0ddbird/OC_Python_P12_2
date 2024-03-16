import typer
from rich import print
from rich.table import Table

from src.db_access import get_db_session
from src.events.models import Event

app = typer.Typer()


@app.command("list")
def list_events():
    conn = get_db_session()
    events = conn.query(Event).all()
    events_table = Table(title="Events")
    events_table.add_column("Id")
    events_table.add_column("Name")
    events_table.add_column("Start Date")
    events_table.add_column("End Date")
    events_table.add_column("Attendees")
    events_table.add_column("Location")
    events_table.add_column("Notes")
    events_table.add_column("Contract")
    events_table.add_column("Support Rep")
    events_table.add_column("Time Created")
    events_table.add_column("Time Updated")

    for event in events:
        events_table.add_row(
            str(event.id),
            event.name,
            str(event.start_date),
            str(event.end_date),
            str(event.attendees),
            event.location,
            event.notes,
            event.contract.id if event.contract else "",
            event.support_rep.name if event.support_rep else "",
            str(event.time_created),
            str(event.time_updated),
        )

    print(events_table)
