import typer
from rich import print
from rich.table import Table

from epic_events.models import session
from epic_events.models.events import Event

app = typer.Typer()


@app.command("list")
def list_events():
    events = session.query(Event).all()
    events_table = Table(title="Events")
    columns = (
        "Id",
        "Name",
        "Start date",
        "End date",
        "Attendees",
        "Location",
        "Notes",
        "Contract",
        "Support Rep",
        "Time created",
        "Time updated",
    )
    for column in columns:
        events_table.add_column(column)

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


@app.command("create")
def create_event():
    name = typer.prompt("Name")
    start_date = typer.prompt("Start date")
    end_date = typer.prompt("End date")
    attendees = typer.prompt("Attendees")
    location = typer.prompt("Location")
    notes = typer.prompt("Notes")
    contract_id = typer.prompt("Contract ID")
    support_rep_id = typer.prompt("Support Rep ID")

    event = Event(
        name=name,
        start_date=start_date,
        end_date=end_date,
        attendees=attendees,
        location=location,
        notes=notes,
        contract_id=contract_id,
        support_rep_id=support_rep_id,
    )
    session.add(event)
    session.commit()
    typer.echo(f"Event {event.id} created")


@app.command("update")
def update_event():
    event_id = typer.prompt("Event ID")
    event = session.query(Event).get(event_id)

    if event is None:
        typer.echo(f"Event {event_id} not found")
        raise typer.Exit(code=1)

    name = typer.prompt("Name", default=event.name)
    start_date = typer.prompt("Start date", default=event.start_date)
    end_date = typer.prompt("End date", default=event.end_date)
    attendees = typer.prompt("Attendees", default=event.attendees)
    location = typer.prompt("Location", default=event.location)
    notes = typer.prompt("Notes", default=event.notes)
    contract_id = typer.prompt("Contract ID", default=event.contract_id)
    support_rep_id = typer.prompt("Support Rep ID", default=event.support_rep_id)

    event.name = name
    event.start_date = start_date
    event.end_date = end_date
    event.attendees = attendees
    event.location = location
    event.notes = notes
    event.contract_id = contract_id
    event.support_rep_id = support_rep_id

    session.commit()


@app.command("delete")
def delete_event(event_id: int):
    event = session.query(Event).get(event_id)

    if event is None:
        typer.echo(f"Event {event_id} not found")
        raise typer.Exit(code=1)

    session.delete(event)
    session.commit()
    typer.echo(f"Event {event_id} deleted")
