# Install

Set up a virtualenv if you want

```bash
virtualenv ./venv -p python3
source venv/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

# Run

```bash
python3 server.py
```

## TODO

Each person will add one function which must have a url mapping. Look
at
[`hi`](https://github.com/binghamton-cs140/name-server/blob/master/server.py#L37)
in [server.py](server.py) for an example

The function can do anything you want it to do as long as it uses
session variables. You can add a decorator, add new session variables,
be creative!
