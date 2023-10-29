model (
    name dwh.dim_buildkite_agent,
    kind view
);

select
    agent_name
from dwh.stg_buildkite__agent
