from pages.radar.data.command_helper import get_command

tests = (
    "/250 /330",
    "/250",
    "ms 220",
    "/250 mh330",
    " /250 mh330   ",
)

for test in tests:
    val = get_command(test)
    print(val)