SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'Business_Intelegent_Project_v2';
DROP DATABASE IF EXISTS "Business_Intelegent_Project_v2";
CREATE DATABASE "Business_Intelegent_Project_v2" WITH TEMPLATE "Business_Intelegent_Project";
