# Dynamic Channels Discord bot

This bot manages dynamic groups of voice channels in a Discord server.

On channels named in the format of `Name Number` the bot will automatically
create and delete channels as members join and leave them.

![](https://media.giphy.com/media/1Qjyn0ZXkjq3N9Zf2T/giphy.gif)

## Requirements

The script requires the 1.0 or newer version of the `discord.py` module.

```
python3 -m pip install -U discord.py
```

## Permissions

The bot needs only the **Manage Channels** permission. On private channels, it
must also have the **Connect** permission explicitly granted.

## Usage

Run the bot's script with the `python3` command specifying the bot's API key as
an environment variable.

```bash
API_KEY=SECRET python3 bot.py
```

## Installing as a service

The bot should normally run as a service. As an example, this can be configured
as a `systemd` service.

Create the service at ```/lib/systemd/system/dynamic_channels.service```.

```
[Unit]
Description=Dynamic Channels Discord bot

[Service]
Type=simple
Environment="API_KEY=SECRET"
ExecStart=/usr/bin/python3 /opt/dynamic_channels/bot.py

[Install]
WantedBy=multi-user.target
```

Then, start the service and configure it to run on startup.

```
sudo systemctl enable dynamic_channels
sudo systemctl start dynamic_channels
```

## Contributing

1. Create a named feature branch (i.e. `add-feature`)
2. Write your change
3. Submit a Pull Request

## License and Authors

Author: Matt Graham (<gadgetmg@gmail.com>)

Copyright (c) 2019 Matt Graham, Licensed under the Apache License 2.0
