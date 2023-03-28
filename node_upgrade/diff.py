from rich.console import Console
from deepdiff import DeepDiff
import json

console = Console()

def find_diff(old, new):
    diff = DeepDiff(old, new)
    diff_dict = json.loads(diff.to_json())
    return diff_dict.get('values_changed', {})

def format_diff(diff):
    """ Returns the diff in a formatted string """
    output = ''

    for key, value in diff.items():
        if value:
            output += f'[bold]{key}[/]\n'
            if 'old_value' in value and 'new_value' in value:
                output += f'[red]  --- old[/]\n'
                output += f'[green]  +++ new[/]\n'
                output += f'[blue]  @@ -1 +1 @@[/]\n'
                output += f'[red]  -{value["old_value"]}[/]\n'
                output += f'[green]  +{value["new_value"]}[/]\n'
            else:
                output += f'  {value}\n'
    return output

def show_diff(old, new):
    diff = find_diff(old, new)
    console.print(format_diff(diff))

if __name__ == '__main__':
    old_data = {"foo": "bar", "baz": 1, "c": {"d": 1, "e": 2}}
    new_data = {"foo": "bax", "baz": 2, "c": {"d": 1, "e": 3}}
    show_diff(old_data, new_data)
