#!/usr/bin/env python3

import os
import json
import click
import subprocess

VERSION = '0.0.1a'

def check_targets():
  try:
    p = subprocess.Popen([
      "curl", "-s", "-XGET", "http://prometheus.doamin.com:9090/api/v1/targets" ],
    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    out = json.loads(stdout.decode("utf-8"))
    return [
        v.get('instance') for i in out.get('data')['activeTargets']
        for k,v in i.items() if k == "labels" and v.get('job') == "node" and v.get('instance') != "localhost:9090"
        ]
  except Exception as e:
    print(e)

def check_class():
  try:
    p = subprocess.Popen([
      "curl", "-s", "--user", "admin:passwd123", "-H", "Content-Type:application/json", "-H", "Accept:application/json", "-k", "https://foreman.domain.com/api/v2/fact_values?per_page=9999\&search=name=is_node_exporter" ],
    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    out = json.loads(stdout.decode("utf-8"))
    return out.get('subtotal')
  except Exception as e:
    print(e)

def save_node(node, env, system):
    tmpl = [
        {
          "labels": {
            "job": "node",
            "group": "tst",
            "env": f"{env}",
            "system": f"{system}"

          },
          "targets": [
            f"{node}:9100"
          ]
        }
    ]
    with open(f'/etc/prometheus/conf.d/nodes/{node}.json', 'w', encoding='utf-8') as f:
        json.dump(tmpl, f, ensure_ascii=False, indent=4)
    os.chown(f'/etc/prometheus/conf.d/nodes/{node}.json', 1009, 1009)


def save_apache(node, env, system):
    tmpl = [
        {
          "labels": {
            "job": "apache",
            "group": "tst",
            "env": f"{env}",
            "system": f"{system}"

          },
          "targets": [
            f"{node}:9144"
          ]
        }
    ]
    with open(f'/etc/prometheus/conf.d/apache/{node}.json', 'w', encoding='utf-8') as f:
        json.dump(tmpl, f, ensure_ascii=False, indent=4)
    os.chown(f'/etc/prometheus/conf.d/apache/{node}.json', 1009, 1009)



@click.group()
@click.version_option(version=VERSION)
@click.pass_context
def main(ctx):
    '''
        Simple tool to configure Prometheus exporters
    '''
    if ctx.obj is None:
        ctx.obj = {}


@click.command('node')
@click.option('--srv', required=True, help='Type hostname')
@click.option('--env', required=True, help='Type environment')
@click.option('--system', required=True, help='Enter the assigned system')
@click.pass_context
def node(ctx, srv, env, system):
    '''
        Module for adding node exporter configuration
    '''
    save_node(srv, env, system)


@click.command('apache')
@click.option('--srv', required=True, help='Type hostname')
@click.option('--env', required=True, help='Type environment')
@click.option('--system', required=True, help='Enter the assigned system')
@click.pass_context
def apache(ctx, srv, env, system):
    '''
         Module for adding apache exporter configuration
    '''
    save_apache(srv, env, system)

@click.command('check')
@click.pass_context
def check(ctx):
    '''
        Module for verifying node exporter files with  puppet's class prometheus::node::exporter
    '''
    click.echo(f'Number of instances with jobs node on Prometheus - {len(check_targets())}')
    click.echo(f'Number of hosts with the Puppet prometheus::node::exporter - {check_class()}')

@click.command('sync')
@click.pass_context
def sync(ctx):
    '''
        Module for syncing configuration files between Prometheus <-> Puppet
    '''
    prom = len(check_targets())
    pupp = check_class()
    if prom == pupp:
      click.echo(f'Nothing to do, synchronization consistent... {list(set([prom, pupp]))}')
    else:
      click.echo(f'Synchronization inconsistent, something to do...')

main.add_command(sync)
main.add_command(check)
main.add_command(node)
main.add_command(apache)

if __name__ == '__main__':
    main()

