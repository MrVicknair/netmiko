import json
import rich
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from rich.syntax import Syntax

CUSTOM_THEME = Theme(
    {
        "device_name": "bold magenta",
        "border": "cyan",
        "output": "green",
    }
)


def output_raw(results):
    border_color = CUSTOM_THEME.styles.get("border").color.name

    if len(results) == 1:
        for device_name, output in results.items():
            print(output)
    else:
        for device_name, output in results.items():
            banner = "-" * len(device_name)
            rich.print(f"[bold {border_color}]{device_name}[/]")
            rich.print(f"[{border_color}]{banner}[/]")
            print(output)
            print()


def output_text(results):
    console = Console(theme=CUSTOM_THEME)
    for device_name, output in results.items():
        panel = Panel(
            output,
            title=device_name,
            expand=False,
            border_style="border",
            title_align="left",
            padding=(1, 1),
        )
        console.print()
        console.print(panel)
        console.print()


def output_json(results, raw=False):
    console = Console(theme=CUSTOM_THEME)

    for device_name, output in results.items():
        try:
            json_data = json.loads(output)
            formatted_json = json.dumps(json_data, indent=2)
            banner = "-" * len(device_name)
            if raw:
                print()
                print(device_name)
                print(banner)
                print(formatted_json)
                print()
            else:
                syntax = Syntax(formatted_json, "json", theme="one-dark")

                console.print()
                print(device_name)
                print(banner)
                console.print(syntax)
                console.print()

        except json.decoder.JSONDecodeError as e:
            msg = f"""

Error processing output for device: {device_name}

In order to use display the output in JSON (--json arg), you must provide the output in JSON
format (i.e. device supports '| json' or parse with TextFSM)

"""
            new_exception = json.decoder.JSONDecodeError(msg, e.doc, e.pos)
            # Raise the new exception, chaining it to the original one
            raise new_exception from e


def output_yaml(results):
    pass


def output_dispatcher(out_format, results):

    # Sort the results dictionary by device_name
    results = dict(sorted(results.items()))

    output_functions = {
        "text": output_text,
        "json": output_json,
        "yaml": output_yaml,
        "raw": output_raw,
        "json_raw": output_json,
    }
    kwargs = {}
    if out_format == "json_raw":
        func = output_functions.get(out_format, output_text)
        kwargs["raw"] = True
    else:
        func = output_functions.get(out_format, output_text)
    return func(results, **kwargs)