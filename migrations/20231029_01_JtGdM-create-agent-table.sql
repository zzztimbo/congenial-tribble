-- create agent table
-- depends:

create table agent (
    id bigint,
    connection_state text,
    created_at timestamp,
    hostname text,
    ip_address text,
    last_job_finished_at timestamp,
    name text,
    organization_id text,
    priority text,
    url text,
    user_agent text,
    version text,
    web_url text
);
