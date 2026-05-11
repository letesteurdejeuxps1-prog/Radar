def get_command(data: str) -> list[tuple[bool, str, int]]:
    possibilities = ["↑", "↓", "←", "→", "*", "/", "ms", "mh", "ml", "s"]
    results = data.strip(" ").split(" ")
    return_data = []
    for result in results:
        command_header = False
        command_content = ""
        for possibility in possibilities:
            if result.startswith(possibility):
                command_header = str(possibility)
                command_content = result.replace(command_header, "")
                break
        if isinstance(command_header, str):
            try:
                command_content = int(command_content.strip(" "))
                return_data.append((True, command_header, command_content))
            except ValueError:
                pass

    return return_data