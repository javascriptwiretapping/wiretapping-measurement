--- We run this BigQuery script to finalize the build the correct data structure before starting analysis.

-- removed_event_listeners

create or replace table your_dataset_id_final.removed_event_listeners as
SELECT
    site_id,
    site,
    event_type,
    init_invoke as init_id,
    init_id as init_invoke,
    event_time,
    event,
    function,
    useCapture,
    init_stack,
    stack,--ok 
    stack_json,
    third_parties,
    current_page_etld,
    is_third_party_event,
    third_party,
    time,
    measurement
FROM
    `your_dataset_id.removed_event_listeners`
where
    event = "RemoveEventListener"
union
all
SELECT
    site_id,
    site,
    function as event_type,
    init_id,
    init_invoke,
    event_type as event_time,
    stack as event,
    init_stack as function,
    stack_json as useCapture,
    timestamp as init_stack,
    value as stack,
    is_set as stack_json,
    third_parties,    
    '' as current_page_etld,
    null is_third_party_event,
    third_party,
    time,
    measurement
FROM
    `your_dataset_id.callstacks`
where
    stack = "RemoveEventListener"

union ALL
SELECT
  site_id,
  site,
  event_type,
  init_id,
  init_invoke,
  event_time,
  event,
  FUNCTION,
  useCapture, 
  '' init_stack,
  stack,
  stack_json,
  third_parties, 
  current_page_etld,
  is_third_party_event,
  third_party,
  time,
  measurement
FROM
  your_dataset_id.event_listeners
   where event like "%RemoveEventListener%" ;


--- EVENT LISTENERS 


CREATE OR REPLACE TABLE
  your_dataset_id_final.event_listeners AS
SELECT
  *
FROM
  your_dataset_id.event_listeners
WHERE
  event='AddEventListener'

  union ALL
  SELECT
  site_id,
  site,
  event_type,
  init_invoke init_id,
  init_id init_invoke,
  event_time,
  event,
  FUNCTION,
  useCapture,
  init_stack args,
  stack,
  stack_json,
  third_parties,
  measurement,
  '' init_stack,
  current_page_etld,
  is_third_party_event,
  null as stack_hosts,
  null stack_trigger,
  time,
  third_party
FROM
  `your_dataset_id.removed_event_listeners`
WHERE
  event ="AddEventListener"

  union ALL

  SELECT
  site_id,
  site,
  FUNCTION event_type,
  init_id,
  init_invoke,
  event_type event_time,
  stack event,
  init_stack function,
  stack_json useCapture,
  timestamp args,
  value stack,
  is_set stack_json,
  third_parties,
  measurement,
  null init_stack,
  null current_page_etld,
  NULL is_third_party_event,
  NULL AS stack_hosts,
  NULL stack_trigger,
  time,
  third_party
FROM
  your_dataset_id.callstacks
WHERE
  stack='AddEventListener';










----------------

create or replace table your_dataset_id_final.callstacks
AS
SELECT
  *
FROM
  `your_dataset_id.callstacks`
WHERE
  ( stack !='AddEventListener'
    or stack !='RemoveEventListener' ) 
  union all

SELECT
  site_id,
  site,
  event_type FUNCTION,
  init_id,
  init_invoke,
  event_time event_type,
  event stack,
  FUNCTION init_stack,
  useCapture stack_json,
  args timestamp,
  stack value,
  third_parties,
  measurement,
  CAST(NULL AS STRING)  request_url,
  NULL time,
  CAST(NULL AS int64) third_party,
  stack_json is_set,
FROM
  your_dataset_id.event_listeners 

union ALL

SELECT
  site_id,
  site,
  event_type function,
  init_invoke init_id,
  init_id init_invoke,
  event_time event_type,
  event stack,
  function init_stack,
  useCapture stack_json,
  init_stack timestamp,
  stack value,
  third_parties,
  measurement,
  CAST(NULL AS STRING)  request_url,
  NULL time,
  CAST(NULL AS int64)  third_party,
  stack_json is_set
FROM
  your_dataset_id.removed_event_listeners
WHERE
  event LIKE "%Error%"  ;