_default:
    @just --list --unsorted

# start here: runs start_db, install, migrate, create_external_models, and plan
go: start_db install migrate create_external_models plan

# installs Python dependencies via Poetry
install:
    python -m venv .venv
    . .venv/bin/activate
    poetry install --sync

# updates the schema.yaml file with the latest schema from the database
create_external_models:
    rm -f schema.yaml
    poetry run sqlmesh create_external_models

# shows you the changes you will make to your dev environment
plan:
    poetry run sqlmesh plan

# start the db using docker
start_db:
    ./scripts/local/start_db.sh

# run migrations
migrate:
    poetry run yoyo apply --batch

# sqlmesh web ui
web_ui:
    poetry run sqlmesh ui

# comment out organization_id field
comment_out:
    sed -i 's/organization_id:/#organization_id:/' schema.yaml
