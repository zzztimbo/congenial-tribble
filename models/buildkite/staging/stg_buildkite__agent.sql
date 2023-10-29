model (
    name dwh.stg_buildkite__agent,
    kind view
);

select
    name as agent_name
from public.agent
