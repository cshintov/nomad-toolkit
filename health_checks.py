import json
import fire
import requests

from rich import print
from rich import inspect
from rich.console import Console
from rich.table import Table

CONSUL="http://127.0.0.1:8500"

def create_table():

    table = Table(title="Health check status")

    table.add_column("ServiceName", style="magenta")
    table.add_column("Node", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", justify="right", style="blue", no_wrap=True)
    table.add_column("Status", justify="right", style="green", no_wrap=True)
    table.add_column("Output", justify="right", style="white")

    return table

table = create_table()

colors = {
    'critical': 'red',
    'warning': 'yellow',
    'passing': 'green'
}

def main(job="solana-devnet-rpc"):

    for region in ['eu-de1', 'us-west1']:
        service=f"{job}-{region}"
        URL=f"{CONSUL}/v1/health/checks/{service}"
        # inspect(locals())

        resp = requests.get(URL)
        checks = resp.json()


        for check in checks:
            color = colors[check['Status']]
            table.add_row(
                check["ServiceName"], 
                check["Node"], 
                check["Name"], 
                f"[{color}]{check['Status']}",
                check["Output"]
            )

    console = Console()
    console.print(table)

if __name__ == '__main__':
  fire.Fire(main)
