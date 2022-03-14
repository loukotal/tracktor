from datetime import datetime
import sqlite3
from typing import List, Union

import typer

from .database import TracktorRepository

conn = sqlite3.connect("./test.db") # TODO: Config value / sensible default
db = TracktorRepository(conn)
app = typer.Typer()


@app.command()
def start(project: Union[str, None] = None, tracker_id: Union[str, None] = None):
    """
    Starts a new time log & stops any currently running time logs.
    """
    db.stop_any_running()
    log = db.add_log(project=project, tracker_id=tracker_id, start_time=datetime.now())
    print(log.project)
    typer.echo(f"Tracking! {log}")

@app.command()
def stop():
    """
    Stops any currently running time logs.
    """
    db.stop_any_running()

@app.command()
def continue_log(tracker_id: str = None):
    """
    Creates a new time log. 
    When `tracker_id` is not provided, copies data from the latest one.
    """
    pass

@app.command()
def current():
    """
    Gets current time log with calculated duration.
    """
    curr = db.get_current()
    typer.echo(f"{curr}")

@app.command()
def today():
    stats = db.get_stats()
    typer.echo([f"{stat}" for stat in stats])

@app.command()
def raw(sql: List[str]):
    print(sql)
    res = db.raw(" ".join(sql))
    typer.echo(res)

@app.callback()
def init_db():
    db.init()

def main():
    app()
    db.graceful_close()

# if __name__ == "__main__":
#     app()
#     db.graceful_close()
# TODO:
# - [wip] add repo for creating time logs
# - [] prepare commands
# - [x] connect to sqlite
# - [] add setup command
# - [x] allow raw options - will run raw SQL to sqlite
# - [] setup opening issue in redmine / through API + links to post hours / do it automatically
# - [x] add start / stop / cancel / continue commands
# - [] handle empty time logs - split the empty log to different projects worked on during the day
# - group by day: select sum(duration), strftime('%Y-%m-%d', create_time) day from tracktor_logs group by day;
