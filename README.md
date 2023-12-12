# job-exporters-from-puppet
Script for configure Prometheus jobs in accord with Puppet classes

## Depedencies
- `click`


## Installation

Just install the dependencies and copy the binary somewhere you want to e.g:

```
curl -Lso /opt/sync_exporters_from_puppet.py https://raw.githubusercontent.com/kadasz/job-exporters-from-puppet/main/sync_exporters_from_puppet.py
chmod +x /opt/sync_exporters_from_puppet.py
```

## Usage

```
$ ./sync_exporters_from_puppet.py
Usage: sync_exporters_from_puppet.py [OPTIONS] COMMAND [ARGS]...

  Simple tool to configure Prometheus exporters

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  apache  Add apache exporter configuration
  check   Verify node exporter files with puppet prometheus::node::exporter
  node    Add node exporter configuration
  sync    Sync configuration files between Prometheus <-> Puppet

```
