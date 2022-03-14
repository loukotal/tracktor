
<div align="center">
  
![](https://raw.githubusercontent.com/loukotal/tracktor/master/assets/static/img/logo.svg)

# Time Tracktor
A CLI time tracker.

</div>

## Disclaimer :exclamation:
This is as alpha as it gets. Use with caution.


## TODOs & Ideas:
- [] Better README
- [wip] add methods for creating & manipulating time logs
- [x] connect to sqlite
- [] add setup command
- [x] allow raw options - will run raw SQL to sqlite
- [] make raw SQL not having to escape single quotes
- [] setup opening issue in issue tracker (e.g. redmine) / through API + links to post hours / do it automatically
- [x] add start / stop / cancel / continue commands
- [] handle empty time logs - split the empty log to different projects worked on during the day
- group by day: select sum(duration), strftime('%Y-%m-%d', create_time) day from tracktor_logs group by day;

## License
MIT
