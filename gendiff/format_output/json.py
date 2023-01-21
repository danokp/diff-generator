import json as js


def json(diff_dict: dict) -> str:
    return js.dumps(diff_dict, sort_keys=True, indent=4)