SELECT 
    v.res_id,
    v.res_type,
    v.res_version,
    v.res_text_vc::json->>'id' as patient_id,
    v.res_text_vc::json->>'birthDate' as birth_date,
    v.res_text_vc::json->>'gender' as gender,
    --jsonb_array_elements_text(v.res_text_vc::json->'name'->0->'given') as given_name,
    v.res_text_vc::json->'name'->0->>'family' as family_name,
    v.res_text_vc::json->'address'->0->>'city' as city,
    v.res_text_vc::json->'address'->0->>'country' as country,
    v.res_text_vc::json->'telecom'->0->>'value' as contact,
    v.res_updated as last_updated
FROM public.hfj_res_ver v
WHERE v.res_type = 'Patient'
ORDER BY v.res_updated DESC
LIMIT 100;