# ichika-janken-auto

## Requirements

- [Python3](https://www.python.org/)
- [requests](https://requests.readthedocs.io/en/master/)

## How to use

First, clone the repository.
You can also download the repository via https://github.com/jhs7jhs/ichika-janken-auto/archive/master.zip.
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

## How to set a schedule

You can use this code to do janken automatically everyday, with a scheduler like:

- [cron](https://en.wikipedia.org/wiki/Cron)
- [Windows Task Scheduler](https://en.wikipedia.org/wiki/Windows_Task_Scheduler)

### cron

Don't forget to use `cd` command before running the code.
The code uses local path: `captcha.json` and `logindata.json`, so you must run the code in the path which those files are in.
```
1 10,15,20 * * * cd /your/path/to/ichika-janken-auto && ./run.py
```

### Windows Task Scheduler

You can write `.bat` script file to run the code, and add a schedule to run the script.
Don't forget to use `cd` command before running the code, like using cron described above.