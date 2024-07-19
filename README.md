For Docker Based setup update the env file
```
POSTGRES_DB=schooldb
POSTGRES_USER=[user]
POSTGRES_PASSWORD=[pass]
DB_HOST=postgres_db_school #localhost, for local setup
DB_PORT=5432
USER_EMAIL=[YOUR_EMAIL]
USER_PASSWORD=[EMAIL_PASSWORD]
DEBUG=True
SECRET_KEY=[YOUR_SECRET_KEY]
POSTGRES_HOST_AUTH_METHOD=trust
```

For allowed host we have to create allowed_hosts.json file (if not present) parallel to Dockerfile and place allowed hosts in it before the build is made