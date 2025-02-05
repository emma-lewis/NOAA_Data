DROP TABLE IF EXISTS wcgbts_data;

CREATE TABLE wcgbts_data (
    id SERIAL PRIMARY KEY,
    year INT,
    month INT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    bottom_depth_m DOUBLE PRECISION,
    scientific_name TEXT,
    catch_numbers BIGINT,
    catch_wt_kg DOUBLE PRECISION,
    cpue_wt_kg_per_m2 DOUBLE PRECISION
);