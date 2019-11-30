# ssrcli

[![Build Status](https://travis-ci.org/myl7/ssrcli.svg?branch=master)](https://travis-ci.org/myl7/ssrcli)
[![codecov.io Code Coverage](https://codecov.io/gh/myl7/ssrcli/branch/master/graph/badge.svg)](https://codecov.io/gh/myl7/ssrcli)
[![Known Vulnerabilities](https://snyk.io/test/github/myl7/ssrcli/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/myl7/ssrcli?targetFile=requirements.txt)
[![Maintainability](https://api.codeclimate.com/v1/badges/b3c6db1a25f3fd84d654/maintainability)](https://codeclimate.com/github/myl7/ssrcli/maintainability)

SSR management client on Linux with command line interface

## Features

- Command line interface, which is friendly for headless environment
- All-in-one management for SSR application, configuration and subscription
- pacman-style commands, which is short and easy for use
- Support subscription update, configuration share URL and more useful function

## Prerequisites

- `Python` >= 3.6
- `git` for SSR installation
- `lsof` to check local port

## Get Started

First install this package from PyPI:

```shell
pip3 install ssrcli
```

Then use ssrcli to install SSR:

```shell
ssrcli --install
```

Following [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html),
SSR will be downloaded to `~/.local/share/shadowsocksr`

Then add your SSR configuration using ssrcli and use it. For example, if you have a SSR subscription url, do:

```shell
# Add a subscription
ssrcli -Saj '{"name": "<the name>", "url": "<the url>"}'
# Update all subscription
ssrcli -Sua
# List all got configuration
ssrcli -Cla
# Choose one. With its id, use the configuration
ssrcli -Csc '<the id>'
# Start SSR
ssrcli -O
# Or restart SSR, which would ensure SSR is on
ssrcli -R
```

For more information, refer to the below content of this readme or `ssrcli -h`

## Config

We recommend not to use a custom ssrcli config file for the default config is enough and good

ssrcli will go through XDG_CONFIG_DIRS to search for `ssrcli/ssrcli-config.json` to load.
Following XDG Standard, you should put your config file as `~/.config/ssrcli/ssrcli-config.json`.
This is a JSON file which can optionally contains the below options. Both upper case and lower case is OK.

|         Name          |          Default Value           |                  Description                  |
|-----------------------|----------------------------------|-----------------------------------------------|
| DB_PATH               | ~/.local/share/ssrcli/db.sqlite3 | Path to the database file containing all data |
| SSR_APP_PATH          | ~/.local/share/shadowsocksr      | Path to the folder containing SSR             |
| SSR_CONF_PATH         | ~/.config/ssrcli/ssr-config.json | Path to the SSR config file                   |
| SSR_LOCAL_PORT        | 1080                             | Local port used by SSR                        |
| SSR_CONF_EXTRA_FIELDS | See below                        | Extra JSON content added to SSR config file   |
| UPDATE_TIMEOUT        | 10                               | Timeout when updating (Unit: s)               |
| UPDATE_RETRY          | 5                                | Retry times when update failed                |

The default value of SSR_CONF_EXTRA_FIELDS is:

```json
{
  "local_address": "127.0.0.1",
  "local_port": "$SSR_LOCAL_PORT",
  "timeout": 300
}
```

In this JSON \$SSR_LOCAL_PORT will be replaced by the same-name config argument SSR_LOCAL_PORT

## Usage

Show help and version:

More options could be found here

```shell
ssrcli -h
ssrcli -V
```

Below we shorten configuration as conf and subscription as sub

Install/remove SSR with `--install` and `--remove`

Start/stop/restart SSR with `-O`(on), `-F`(off) and `-R`(restart)

Test SSR integrity with `--test`

Manage conf with `-C` and sub with `-S`

Both conf and sub support `-l`(list), `-n`(add), `-d`(delete)

Conf additionally support `-s`(use), sub additionally support `-u`(update)

You can pass multi `-c <id>` to choose multi objects to be processed

You can pass `-j <json>` to provide information. The option value should be a valid JSON with all required fields.

You can add `-a` to perform action on all objects, and usually without `-a`, the default objects of a action is all
objects except for `-d`(delete). Without given objects `-d`(delete) will raise a exception.

As for update, when updating a sub, all old conf belonging to the sub will be removed

You can pass `-r`(current) to ssrcli when using `-l`(list) to show currently used SSR conf

For more information, type `ssrcli -h` to read. The below is some examples:

```shell
# Show help
ssrcli -h
# Add a conf from JSON
ssrcli -Caj '{
  "server": "::1",
  "server_port": 30000,
  "protocol": "origin",
  "method": "none",
  "obfs": "plain",
  "password": "test",
  "obfs_param": "",
  "protocol_param": "",
  "remarks": "test",
  "group": "test"
  }'
# Add a sub from JSON
ssrcli -Caj '{"name": "test", "url": "https://test.test"}'
# List all conf with currently used conf
ssrcli -Clar
# Update all sub with proxy
ssrcli -Suap '{"socks5": "127.0.0.1:1080"}'
```

## Test

First install the test requirements in `requirements.txt`

Then Move to `tests` folder and start the tests with `test.sh` script:

```shell
cd tests  # IMPORTANT, as many tests would rely on the relative path
./test.sh
```

In tests, port 1080, 8001, 8002 will be used. Make sure them bindable or change the ports in `test.sh` and `shared.py`.

Internet is required to download SSR.
Or you can use another pytest command in `test.sh` with downloading SSR to `tests/shadowsocksr` previously.

For the use of Popen, after a failed test port 1080 may be bind by left SSR. Just kill it.

## License

MIT
