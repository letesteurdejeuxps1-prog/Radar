def get_command(data: str) -> list[tuple[bool, str, int, int]]:
    possibilities = ["↑", "↓", "←", "→", "*", "/", "ms", "mh", "ml", "s"]
    results = data.strip().split(" ")

    return_data = []
    for result in results:
        command_header = False
        command_content = ""
        for possibility in possibilities:
            if result.startswith(possibility):
                command_header = possibility
                command_content = result[len(possibility):]
                break
        if isinstance(command_header, str):
            if command_header in ["↑", "↓"] and "," in command_content:
                split_data = command_content.split(",")
                if len(split_data) == 2:
                    try:
                        altitude = int(split_data[0])
                        roc = int(split_data[1]) * 100
                        return_data.append((
                            True,
                            command_header,
                            altitude,
                            roc
                        ))
                    except ValueError:
                        return_data.append((False, "", None, 0))
                continue
            if command_header in ["←", "→", "*"] and command_content.endswith("*"):
                try:
                    heading = int(command_content[:-1])
                    return_data.append((
                        True,
                        command_header,
                        heading,
                        1
                    ))
                except ValueError:
                    return_data.append((False, "", None, 0))

            # ==========================================
            # NORMAL COMMANDS
            # ==========================================

            try:
                command_value = int(command_content.strip())
                return_data.append((
                    True,
                    command_header,
                    command_value,
                    0
                ))
            except ValueError:
                if command_header == "/" and command_content == "":
                    return_data.append((
                        True,
                        command_header,
                        None,
                        0
                    ))
                else:
                    return_data.append((False, "", None, 0))

    return return_data