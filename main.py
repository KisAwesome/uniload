#!/usr/bin/env python3
import argparse
import json
import os


def get_file(file):
    return os.path.join(os.path.dirname(__file__), file)


def get_value(mod, path):
    curr = mod
    for i in path:
        curr = getattr(curr, i)
    return curr


def load_types():
    with open(get_file("types.json"), "r") as f:
        _types = json.load(f)

    filetypes = {}
    languages = _types.copy()
    for lang, info in _types.items():
        info["name"] = lang
        for inf in info["file-types"]:
            filetypes[inf] = info
        for alias in info.get("aliases", []):
            languages[alias] = info

    return languages, filetypes


def form_type(type_):
    if type_.startswith("."):
        return type_.replace(".", "", 1)
    return "." + type_


def get_loader(args, parser):
    file_path = args.file
    types, filetypes = load_types()

    full_dict = types.copy()
    full_dict.update(filetypes)

    file_sp = os.path.splitext(os.path.basename(file_path))
    if args.type is not None:
        args.type = args.type.lower()
        type_dict = full_dict.get(args.type, full_dict.get(form_type(args.type)))
        if type_dict is None:
            return parser.error(f"Type {args.type} does not exist")

    else:
        file_type = file_sp[1]
        type_dict = filetypes.get(file_type, None)
        if type_dict is None:
            return parser.error(f"Type {file_type} does not exist")

    return type_dict


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Uniload", description="Loads all types of config files from terminal"
    )

    parser.add_argument("file")
    parser.add_argument(
        "--type", help="Manully choose the type of config file to treat input as"
    )

    return parser.parse_args(), parser


def main():
    args, parser = parse_args()
    if not os.path.exists(args.file):
        return parser.error(f"File {args.file} does not exist")
    loader = get_loader(args, parser)

    loading_func = loader["load"].split(".")

    module = loading_func.pop(0)

    if module == "file":
        function = lambda file: getattr(file, loading_func[0])()
    else:
        function = get_value(__import__(module), loading_func)
    with open(args.file, loader.get("read-mode", "r")) as f:
        try:
            file = function(f)
        except Exception as e:
            print(f'Error while loading {args.file} with loader {loader["name"]}')
            print(e)
        else:
            if not isinstance(file, (int, float, str)):
                try:
                    print(json.dumps(file, indent=4, sort_keys=True))
                except:
                    print(file)
            else:
                print(file)


if __name__ == "__main__":
    main() 
