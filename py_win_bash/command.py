from typing import Any, Dict, List, Optional


class Command:
    @staticmethod
    def parse(schema: Dict, input: List[str]) -> Dict:
        """
        Parses command input to separate elements
        :param schema: Dict of optional flags and kwargs {title: str, short: str}
        :param input: List of strings for the command
        :return: Dict of {args: [], flags: [], kwargs: {}}
        """
        match: Dict[str, List] = {
            "flags": schema["flags"] if "flags" in schema else [],
            "kwargs": schema["kwargs"] if "kwargs" in schema else [],
        }
        # TODO: consider how this is not currently checking the validity of flags and kwargs
        # NOTE: would it be worth making a CommandSchema class or something like that?

        result: Dict[str, Any] = {
            "args": [],
            "flags": [],
            "kwargs": {},
        }

        # Iterate Arguments
        arg_list = iter(input)

        def _find_nested_value(list: List, key: str, value: str) -> Optional[str]:
            """
            Finds a nested value in a list of dictionaries
            :param list: the list to search
            :param key: the key of the dictionary in each list element to check
            :param value: the value to match to the key in the dictionary
            :return: title of matched element or None
            """
            for entry in list:
                if entry[key] == value:
                    return entry["title"]
            return None

        def _find_in_schema(key: str, value: str) -> None:
            """
            Finds a related flag or kwarg based on command input value
            :param key: the key ("title" or "short") to check
            :param value: the value to match against
            :return: None
            """

            # Flag Argument
            find_flag = _find_nested_value(match["flags"], key, value)
            if find_flag:
                result["flags"].append(find_flag)

            # Keyword Argument
            find_kwarg = _find_nested_value(match["kwargs"], key, value)
            if find_kwarg:
                result["kwargs"][find_kwarg] = next(arg_list, None)
                # TODO: consider raising if next is None

            # Not Found
            else:
                pass
            # TODO: consider raising if nothing matched

        # Iterate Elements
        while True:

            # Next Entry
            entry = next(arg_list, None)

            # List End
            if entry is None:
                break

            # Parse Title
            if entry.startswith("--"):
                _find_in_schema("title", entry[2:])

            # Parse Short
            elif entry.startswith("-"):
                _find_in_schema("short", entry[1:])

            # Positional Argument
            else:
                result["args"].append(entry)

        return result
