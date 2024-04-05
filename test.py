select
timestamp_trunc(timestamp,hour) timestamp,
subid,
raw.org,
case when raw.supply_org in (select id FROM `streamrail.dscf.Org`
WHERE HasSsp = true and SspSettings.SaasFee is null group by 1)
then 'MM' else 'RISE' end as SaasType,
domain,
ifnull(state,'') state,
adtype,
pub.name publisher,
supply_org,
browser,
os,
country,
device_type,
extract(hour from timestamp) hour,
placement_id,
round(SAFE_CAST(param2 as NUMERIC),1) IncomingFloor_grp,
advertiserid,
user_sync_settings,
bl0_report,
max(case when raw.org = '614089bf9bbbfe000189911f' then 1 when raw.org = '5d1a6421ecad4c0001c39467' then 0 end) is_mm,
sum(case when action='bid' then 1 else 0 end) + sum(case when action ='nbd' then safe_cast(r3 as int64) else 0 end) + sum(case when category ='prebid-error' and errorcode !='1' then 1 else 0 end) req,
sum(case when action='bid' then 1 else 0 end) bids,
sum(case when action='win' then 1 else 0 end) wins,
sum(case when action='ai' then 1 else 0 end) impressions,
cast(sum(case when action = 'bn' and errorcode = '1' then (1 / NULLIF((cast (recordID as FLOAT64)),0)) else 0 end) as INT64) as bl_demand_blocks,
cast(sum(case when action = 'bn' and errorcode = '2' then (1 / NULLIF((cast (recordID as FLOAT64)),0)) else 0 end) as INT64) as QPSBlocked,
(sum(case when action='ai' then safe_cast(adsourcerate as float64) else 0 end)/1000) rev,
(sum((cast(adsourcerate as float64)-cast(raw.cost as float64))*case when action='ai' then 1 else 0 end)/1000) profit,
(sum(cast(raw.cost as float64)*case when action='ai' then 1 else 0 end)/1000) cost,
sum(case when action='am' then 1 else 0 end) opp,
concat (dheight,'_',dwidth) dheight_dwidth,
env,
bundleid,
case when pv='us-east-1' then 'USA East'
when pv='us-west-2' then 'USA West'
else pv end as dc_region
from
(
select timestamp, subid, org, domain, state, adtype, supply_org, browser, os, country, device_type, placement_id,param2 , user_sync_settings, bl0_report, action, category, errorcode,
recordID, adsourcerate, cost, dheight, dwidth, env, bundleid, pv, position, bas as advertiserid, rank, dc_region, split(module_version,"~")[OFFSET(0)] module_version, r3,
concat(sid,'_',original_sid,'_',player_ad_unit) as session, 'seller' as table


from `streamrail.views.RAW_all_sellers_last_3_hours`
where date(timestamp) = current_date()
and timestamp_trunc(timestamp, minute) >= timestamp_add(current_timestamp, interval -2 hour)
and lower(subid) in ('hb', 's2s', 'mrkt', 'tam', 'uam', 'pbs')
and (action in ('bid', 'am', 'ai', 'win', 'nbd') or category ='prebid-error')
