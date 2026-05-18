def get_command(data: str, allow_debug_commands: bool = False) -> list[dict]:
    commands = []
    tokens = data.strip().split()
    i = 0
    while i < len(tokens):
        token = tokens[i]
        lower = token.lower()
        # ==========================================
        # DEBUG / CHEAT COMMANDS
        # ==========================================
        if lower.startswith("m") and not allow_debug_commands:
            commands.append({
                "valid": False,
                "reason": "Debug commands disabled"
            })
            i += 1
            continue

        if lower.startswith("ms"):
            try:
                speed = int(token[2:])
                commands.append({
                    "valid": True,
                    "cmd": "MAKE_SPEED",
                    "value": speed
                })
            except ValueError:
                commands.append({"valid": False})
            i += 1
            continue

        if token.startswith("/"):
            content = token[1:]
            if content == "":
                commands.append({
                    "valid": True,
                    "cmd": "UNLOCK_SPEED"
                })
            else:
                try:
                    speed = int(content)
                    commands.append({
                        "valid": True,
                        "cmd": "SPEED",
                        "value": speed
                    })
                except ValueError:
                    commands.append({"valid": False})
            i += 1
            continue

        if token.startswith("↑") or token.startswith("↓"):
            cmd = "CLIMB" if token.startswith("↑") else "DESCEND"
            content = token[1:]
            try:
                if "," in content:
                    alt, roc = content.split(",")
                    commands.append({
                        "valid": True,
                        "cmd": cmd,
                        "value": int(alt),
                        "special": int(roc) * 100
                    })
                else:
                    commands.append({
                        "valid": True,
                        "cmd": cmd,
                        "value": int(content),
                        "special": 0
                    })
            except ValueError:
                commands.append({"valid": False})
            i += 1
            continue

        if token[0] in ["←", "→", "*"]:
            symbol = token[0]
            content = token[1:]
            expedite = False
            if content.endswith("*"):
                expedite = True
                content = content[:-1]
            try:
                heading = int(content)
                if symbol == "←":
                    cmd = "TURN_LEFT"
                elif symbol == "→":
                    cmd = "TURN_RIGHT"
                else:
                    cmd = "HEADING"
                commands.append({
                    "valid": True,
                    "cmd": cmd,
                    "value": heading,
                    "special": expedite
                })
            except ValueError:
                commands.append({"valid": False})
            i += 1
            continue

        if lower.startswith("mh"):
            try:
                heading = int(token[2:])
                commands.append({
                    "valid": True,
                    "cmd": "MAKE_HEADING",
                    "value": heading
                })
            except ValueError:
                commands.append({"valid": False})
            i += 1
            continue

        if lower.startswith("ml"):
            try:
                level = int(token[2:])
                commands.append({
                    "valid": True,
                    "cmd": "MAKE_LEVEL",
                    "value": level
                })
            except ValueError:
                commands.append({"valid": False})
            i += 1
            continue

        if lower.startswith("s"):
            try:
                ssr = int(token[1:])
                commands.append({
                    "valid": True,
                    "cmd": "SSR",
                    "value": ssr
                })
            except ValueError:
                commands.append({"valid": False})
            i += 1
            continue

        if lower == "d":

            # Need exactly ONE point after D
            if i + 1 >= len(tokens):
                commands.append({
                    "valid": False,
                    "reason": "DIRECT requires a point"
                })
                i += 1
                continue

            point = tokens[i + 1].upper()

            # If another non-command token exists after the point,
            # reject command
            if i + 2 < len(tokens):

                next_token = tokens[i + 2]

                is_new_command = (
                        next_token.startswith(("↑", "↓", "←", "→", "*", "/"))
                        or
                        next_token.lower() in ("d", "rte")
                        or
                        next_token.lower().startswith(("ms", "mh", "ml"))
                )

                if not is_new_command:
                    commands.append({
                        "valid": False,
                        "reason": "DIRECT accepts only one point"
                    })
                    i += 3
                    continue

            commands.append({
                "valid": True,
                "cmd": "DIRECT",
                "value": point
            })

            i += 2
            continue

        if lower == "rte":

            route_points = []

            j = i + 1

            while j < len(tokens):

                next_token = tokens[j]
                lower_next = next_token.lower()

                # Detect NEW command
                is_new_command = (
                        next_token.startswith(("↑", "↓", "←", "→", "*", "/"))
                        or
                        lower_next == "d"
                        or
                        lower_next == "rte"
                        or
                        lower_next.startswith(("ms", "mh", "ml"))
                )
                if is_new_command:
                    break

                route_points.append(next_token.upper())
                j += 1

            if len(route_points) >= 2:
                commands.append({
                    "valid": True,
                    "cmd": "ROUTE",
                    "value": route_points
                })
            else:
                commands.append({
                    "valid": False,
                    "reason": "ROUTE requires at least 2 points"
                })
            i = j
            continue

        commands.append({
            "valid": False
        })
        i += 1
    return commands