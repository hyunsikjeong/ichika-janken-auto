# ichika-janken-auto

## Requirements

- [Python3](https://www.python.org/)
- [requests](https://requests.readthedocs.io/en/master/)

## How to use

First, copy `logindata.example.json` to `logindata.json`.
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

Then run `run.py` to Jankenpo!
You can use this code with a scheduler like [cron](https://en.wikipedia.org/wiki/Cron) to do janken automatically everyday.