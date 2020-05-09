# ichika-janken-auto

## Requirements

- [Python3](https://www.python.org/)
- [requests](https://requests.readthedocs.io/en/master/)

## How to use

First, clone the repository. You can also download the repository via https://github.com/jhs7jhs/ichika-janken-auto/archive/master.zip.
```shell
git clone https://github.com/jhs7jhs/ichika-janken-auto.git
```

Copy `logindata.example.json` to `logindata.json`.
```shell
cp logindata.example.json logindata.json
```

Open `logindata.json` and write your ID and password.
```json
{
    "login_id": "example_id",
    "pass_word": "example_password"
}
```

Then run `run.py` to Janken!

You can use this code with a scheduler like [cron](https://en.wikipedia.org/wiki/Cron) or [Windows Task Scheduler](https://en.wikipedia.org/wiki/Windows_Task_Scheduler) to do janken automatically everyday.