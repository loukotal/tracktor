from datetime import datetime
from typing import Any, Dict, Union
import sqlite3


class TracktorLog:
    def __init__(
        self,
        project: str,
        tracker_id: str,
        start_time: str,
        end_time: str,
        duration: float,
    ) -> None:
        self.project = project
        self.tracker_id = tracker_id
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration

    @classmethod
    def from_sqlite(cls, row):
        return cls(
            row["project"],
            row["tracker_id"],
            row["start_time"],
            row["end_time"],
            row["duration"],
        )

    def __str__(self) -> str:
        return f"Log<proj={self.project}, tracker_id={self.tracker_id}, start_time={self.start_time}, end_time={self.end_time}, duration={self.duration}>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project": self.project,
            "tracker_id": self.tracker_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
        }


class TracktorLogStatistic:
    def __init__(
        self, project: str, tracker_id: str, date: str, worked_hours: float
    ) -> None:
        self.project = project
        self.date = date
        self.worked_hours = worked_hours

    @classmethod
    def from_sqlite(cls, row):
        return cls(row["project"], row["tracker_id"], row["date"], row["worked_hours"])

    def __str__(self) -> str:
        return f"Stat<proj={self.project}, date={self.date}, worked_hours={self.worked_hours}>"


class TracktorRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        self.log_table = "tracktor_logs"

    def init(self):
        with self.conn:
            self.conn.execute(
                f"""create table if not exists {self.log_table} (
                id integer primary key autoincrement,
                project text nullable,
                tracker_id text nullable,
                create_time timestamp default current_timestamp,
                start_time timestamp nullable,
                end_time timestamp nullable,
                duration generated always as (cast((julianday(coalesce(end_time, start_time)) - julianday(start_time)) * 24 as real))
            );"""
            )

    def add_log(
        self,
        project: Union[float, None] = None,
        tracker_id: str = None,
        start_time: Union[float, None] = None,
        end_time: Union[str, None] = None,
    ) -> None:
        with self.conn:
            self.conn.execute(
                f"insert into {self.log_table}(project, tracker_id, start_time, end_time) values (?, ?, ?, ?)",
                (project, tracker_id, start_time, end_time),
            )

        entry = self.conn.execute(
            f"select * from {self.log_table} order by create_time desc"
        ).fetchone()
        return TracktorLog.from_sqlite(entry)

    def stop_any_running(self):
        with self.conn:
            self.conn.execute(
                f"update {self.log_table} set end_time = ? where end_time is null",
                (datetime.now(),),
            )

    def get_stats(self):
        with self.conn:
            stats = self.conn.execute(
                "select strftime('%Y-%m-%d', create_time) date, project, tracker_id, sum(duration) as worked_hours from tracktor_logs group by project, tracker_id, date"
            )

        return list(map(TracktorLogStatistic.from_sqlite, stats))

    def get_current(self) -> Union[None, TracktorLog]:
        with self.conn:
            current = self.conn.execute(
                "select *, cast((julianday('now') - julianday(start_time)) * 24 as real) as calc_duration  from tracktor_logs where end_time is null order by start_time desc;"
            ).fetchone()

        if current is None:
            return
        log = TracktorLog.from_sqlite(current)
        log.duration = current["calc_duration"]
        return log

    def raw(self, sql: str):
        with self.conn:
            res = self.conn.execute(sql)
        return [tuple(item) for item in res]

    def graceful_close(self):
        self.conn.commit()
        self.conn.close()
