# ssrcli

This is a SSR client with shell interface and using Docker to deploy

## Features

- SSR deployed by Docker, easy to install and use
- With Privoxy to provide http proxy
- SSR configuration management, with SSR share url support
- SSR subscription management to update SSR configurations

## Installation

### docker part

Put your SSR config.json into `/etc/ssr/`, then go to `docker/ssrcli` and use `docker-compose up -d` to start the SSR service

### python part

Copy the python package `ssrcli` to your favorite dir

## Usage

Use:

```bash
python3 -m ssrcli -h
```

to show help

## License

MIT
