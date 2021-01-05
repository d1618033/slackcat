Installation
=============

It's recommended to use `pipx` to install slackcat:

```
pipx install git+https://github.com/d1618033/slackcat.git
```

but you can also use pip:

```
pip install git+https://github.com/d1618033/slackcat.git
```

After the installation finishes, create a config file with your slack token in `~/.slackcat.toml`:

```
[credentials]
token = "..."
```

Usage
======


```
slackcat --channel <channel_id> [--from-date <from_date>]
```

This command will output all the messages from the previous 365 days in reverse order, 
so you sould probably pipe it into less or grep:

```
slackcat --channel <channel_id> | less
```

or:

```
slackcat --channel <channel_id> | grep <pattern> | wc -l
```

