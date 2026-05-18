from pages.radar.data.command_helper import get_command

tests = (
    "@l250 /250",
    "rte",
    "↑250,50",
    "↓220",
    "↓",
    "←220",
    "→330",
    "→090",
    "→",
    "/250 /330",
    "/",
    "/250 ",
    "ms 220",
    "/250 mh330",
    " /250 mh330",
    "d andie",
    "d stege sta",
    "rte stege sta hrn paddi",
    "rte",
)

for test in tests:
    val = get_command(test)
    for v in val:
        print(v)
    print("_"*20)