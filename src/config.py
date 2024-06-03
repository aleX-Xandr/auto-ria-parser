from dotenv import load_dotenv
from os import getenv


load_dotenv()

HOUR = int(getenv("STARTUP_HOUR"))
assert 0 <= HOUR <= 23, "STARTUP_HOUR must be between 0 and 23 inclusive"

MINUTE = int(getenv("STARTUP_MINUTE"))
assert 0 <= MINUTE <= 59, "STARTUP_MINUTE must be between 0 and 59 inclusive"

THREADAS_LIMIT = int(getenv("THREADAS_LIMIT"))
assert THREADAS_LIMIT % 2 == 0, "THREADAS_LIMIT must be a multiple of 2"

TARGET_URL = getenv("TARGET_URL")
assert TARGET_URL.startswith("https://auto.ria.com/"), "Only auto.ria.com links supported "

DATABASE_URL = getenv("DATABASE_URL")
STARTUP_PARAMS = {
    "hour":HOUR, 
    "minute":MINUTE
}