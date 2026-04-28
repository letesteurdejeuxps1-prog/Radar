from pages.radar.data.helper import convert_lat_long_to_nmbr

tests = (
    "50°25'N",
    "50°25'00''N",
    "50°E",
    "50°25'33''N",
    "50°77'33''N",
)

for test in tests:
    val = convert_lat_long_to_nmbr(test)
    print(val)