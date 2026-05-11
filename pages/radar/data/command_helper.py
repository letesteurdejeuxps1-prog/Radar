def get_command(data: str) -> tuple[bool, str, int]:
    possibilities = ["↑", "↓", "←", "→", "*", "/", "ms", "mh", "ml"]
    command_header = False
    command_content = ""
    for possibility in possibilities:
        if data.startswith(possibility):
            command_header = str(possibility)
            command_content = data.replace(command_header, "")
            break
    if isinstance(command_header, str):
        try:
            command_content = int(command_content.strip(" "))
            return True, command_header, command_content
        except ValueError:
            pass

    return False, "", 0