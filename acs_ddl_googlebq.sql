-- Integers should be type INT64, see other data types: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
-- Default Nullable. Adding NOT NULL makes the field required.

CREATE TABLE broadband.acs_hispanic(
       id STRING NOT NULL,
       block_group_code STRING,
       geography STRING,
       estimate_total INT64,
       margin_of_error_total INT64,
       estimate_total__not_hispanic_or_latino INT64,
       margin_of_error_total__not_hispanic_or_latino INT64,
       estimate_total__hispanic_or_latino INT64,
       margin_of_error_total__hispanic_or_latino INT64
)
