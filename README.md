# ssrcli

SSR client with shell interface and using Docker to deploy

## Features

- SSR deployed by Docker, easy to install and use
- With Privoxy to provide http proxy
- SSR configuration management, with ssr url support
- SSR subscription management to update SSR configurations

## Installation

### docker

Put your SSR config.json into `/etc/ssr/`, then go to `docker/ssrcli` and use `docker-compose up -d` to start the SSR service

### python

Copy python package `python/ssrcli` to somewhere you like

## Usage

Use:

```bash
python3 -m ssrcli -h
```

to show help

## License

MIT
