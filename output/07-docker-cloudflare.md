# Docker and Cloudflare

Generated: 2026-06-30T21:41:58.616595


## Purpose

Defines container/runtime exposure and public HTTPS routing.

## Responsibilities

- Provide any required container runtime compatibility.
- Expose public Alfred endpoints through Cloudflare Tunnel.
- Map hostnames to correct local ports.

## Inputs

- Docker containers
- Cloudflare tunnel config
- Local services

## Outputs

- Public HTTPS endpoints
- Container runtime state

## Dependencies

- Docker
- cloudflared
- Cloudflare ingress configuration

## Failure Modes

- Cloudflare points to wrong local port.
- Container name exists historically but is not valid for current path.
- Service returns 502 because local target is not listening.

## Recovery Procedure

- Use ss -ltnp to confirm local listeners.
- Check /etc/cloudflared/config.yml.
- Restart cloudflared only after confirming local target.
- Inspect containers before assuming they are current production runtime.

## Source Evidence

### docker/containers.txt

Size: 368 bytes

```text
NAMES                              STATUS                   IMAGE                                        PORTS
hermes-agent-lp1i-hermes-agent-1   Exited (0) 6 weeks ago   ghcr.io/hostinger/hvps-hermes-agent:latest   
hermes-agent-mctr-hermes-agent-1   Up 17 hours              ghcr.io/hostinger/hvps-hermes-agent:latest   0.0.0.0:32768->4860/tcp, [::]:32768->4860/tcp

```

### docker/images.txt

Size: 294 bytes

```text
WARNING: This output is designed for human readability. For machine-readable output, please use --format.
IMAGE                                        ID             DISK USAGE   CONTENT SIZE   EXTRA
ghcr.io/hostinger/hvps-hermes-agent:latest   97e901c56cbd       9.84GB         3.04GB   U    

```

### cloudflare/config.yml

Size: 384 bytes

```text
tunnel: 297ae52c-a42f-4431-83d4-a3b49cc486f5
credentials-file: /root/.cloudflared/297ae52c-a42f-4431-83d4-a3b49cc486f5.json

ingress:
  - hostname: alfred.alfreddoheny.cloud
    service: http://localhost:4865

  - hostname: v2.alfreddoheny.cloud
    service: http://127.0.0.1:4880

  - hostname: api.alfreddoheny.cloud
    service: http://127.0.0.1:8788

  - service: http_status:404

```
