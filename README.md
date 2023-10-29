# congenial-tribble

## initial set up
```
just go
```

## comment out a field in schema.yaml
```
just comment_out
```

## run sqlmesh plan
```
just plan
```

## just commands
```
Available recipes:
    go                     # start here: runs install, create_external_models, and plan
    install                # installs Python dependencies via Poetry
    create_external_models # updates the schema.yaml file with the latest schema from the database
    plan                   # shows you the changes you will make to your dev environment
    start_db               # start the db using docker
    migrate                # run migrations
    web_ui                 # sqlmesh web ui
    comment_out            # comment out organization_id field
```
