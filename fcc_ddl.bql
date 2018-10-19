SELECT * FROM
  (SELECT 
    201412 AS file_date,
    provider_id,
    hoco_num,
    hoco_final,
    state_abbr,
    block_code,
    SUBSTR(block_code, 0, 5) AS state_county_code,
    tech_code,
    consumer,
    max_ad_down,
    max_ad_up
  FROM `fccdsicapstone-218522.broadband.fcc_201412`
  UNION ALL
  SELECT 
    201506 AS file_date,
    provider_id,
    hoco_num,
    hoco_final,
    state_abbr,
    block_code,
    SUBSTR(block_code, 0, 5) AS state_county_code,
    tech_code,
    consumer,
    max_ad_down,
    max_ad_up
  FROM `fccdsicapstone-218522.broadband.fcc_201506`
  UNION ALL
  SELECT 
    201512 AS file_date,
    provider_id,
    hoco_num,
    hoco_final,
    state_abbr,
    block_code,
    SUBSTR(block_code, 0, 5) AS state_county_code,
    tech_code,
    consumer,
    max_ad_down,
    max_ad_up
  FROM `fccdsicapstone-218522.broadband.fcc_201512`
  UNION ALL
  SELECT 
    201606 AS file_date,
    provider_id,
    hoco_num,
    hoco_final,
    state_abbr,
    block_code,
    SUBSTR(block_code, 0, 5) AS state_county_code,
    tech_code,
    consumer,
    max_ad_down,
    max_ad_up
  FROM `fccdsicapstone-218522.broadband.fcc_201606`
  UNION ALL
  SELECT 
    201612 AS file_date,
    provider_id,
    hoco_num,
    hoco_final,
    state_abbr,
    block_code,
    SUBSTR(block_code, 0, 5) AS state_county_code,
    tech_code,
    consumer,
    max_ad_down,
    max_ad_up
  FROM `fccdsicapstone-218522.broadband.fcc_201612`
  UNION ALL
  SELECT 
    201706 AS file_date,
    provider_id,
    hoco_num,
    hoco_final,
    state_abbr,
    block_code,
    SUBSTR(block_code, 0, 5) AS state_county_code,
    tech_code,
    consumer,
    max_ad_down,
    max_ad_up
  FROM `fccdsicapstone-218522.broadband.fcc_201706`)
WHERE state_abbr NOT IN ('AK', 'HI', 'GU', 'MH', 'FM', 'MP', 'PW', 'PR' , 'VI' , 'AS')
AND consumer = 1
AND tech_code <> 60;
