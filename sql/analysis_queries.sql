-- Index on year for faster time-based queries
CREATE INDEX idx_year ON wcgbts_data(year);

-- Index on scientific_name for species-specific queries
CREATE INDEX idx_scientific_name ON wcgbts_data(scientific_name);

-- Index on catch_numbers to optimize filtering by catch size
CREATE INDEX idx_catch_numbers ON wcgbts_data(catch_numbers);

-- Retrieve all data
SELECT * FROM wcgbts_data

-- Filter by scientific name
SELECT * FROM wcgbts_data WHERE scientific_name = 'Dover sole'

-- Get average CPUE by species
SELECT scientific_name, AVG(cpue_wt_kg_per_m2) AS avg_cpue_kg_per_m2
FROM wcgbts_data
GROUP BY scientific_name
ORDER BY avg_cpue_kg_per_m2 DESC;

-- Get total catch weight per year
SELECT year, SUM(catch_wt_kg) AS total_catch
FROM wcgbts_data
GROUP BY year
ORDER BY year DESC;