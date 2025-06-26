class DBTables:
    SESSIONS        = "sessions"
    USERS           = "users"
    APPLICATIONS    = "applications"
    AUTH_CODES      = "auth_codes"


class  DBConfig:
    SCHEMA_NAME = "auth"
    BASE_ARGS   = { "schema": SCHEMA_NAME }