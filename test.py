from pages.radar.data.helper import convert_lat_and_long_to_radar

tests = (
    "57°52'24''N|15°56'03''E",
    "50°25'N",
    "50°25'00''N",
    "50°E",
    "50°25'33''N",
    "50°77'33''N",
    "57°52'24''N|15°56'03''E"
)

for test in tests:
    val = convert_lat_and_long_to_radar(test)
    print(val)