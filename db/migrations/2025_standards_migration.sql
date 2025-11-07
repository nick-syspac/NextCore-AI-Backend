-- Migration: Add support for ASQA Standards for RTOs 2025
-- Date: 2025-11-07
-- Description: Updates the asqa_standards table to support the new 2025 standards structure
--              including Outcome Standards (Quality Areas 1-4), Compliance Requirements, and Credential Policy

-- Add new columns to asqa_standards table
ALTER TABLE asqa_standards 
ADD COLUMN IF NOT EXISTS standard_category VARCHAR(20) DEFAULT 'legacy_2015',
ADD COLUMN IF NOT EXISTS quality_area INTEGER,
ADD COLUMN IF NOT EXISTS asqa_url VARCHAR(500);

-- Update the version field to allow both 2015 and 2025
ALTER TABLE asqa_standards 
ALTER COLUMN version SET DEFAULT '2025';

-- Drop the old unique constraint on standard_number
ALTER TABLE asqa_standards 
DROP CONSTRAINT IF EXISTS asqa_standards_standard_number_key;

-- Add new unique constraint allowing same standard_number for different versions
ALTER TABLE asqa_standards 
ADD CONSTRAINT asqa_standards_standard_number_version_key UNIQUE (standard_number, version);

-- Create new indexes for performance
CREATE INDEX IF NOT EXISTS asqa_standards_version_is_active_idx ON asqa_standards(version, is_active);
CREATE INDEX IF NOT EXISTS asqa_standards_category_idx ON asqa_standards(standard_category);
CREATE INDEX IF NOT EXISTS asqa_standards_quality_area_idx ON asqa_standards(quality_area);
CREATE INDEX IF NOT EXISTS asqa_standards_standard_number_idx ON asqa_standards(standard_number);

-- Update existing 2015 standards to have proper category
UPDATE asqa_standards 
SET standard_category = 'legacy_2015'
WHERE version = '2015';

-- Add comments to document the schema
COMMENT ON COLUMN asqa_standards.standard_category IS 'Classification: outcome, compliance, credential, or legacy_2015';
COMMENT ON COLUMN asqa_standards.quality_area IS 'Quality Area number (1-4) for 2025 Outcome Standards';
COMMENT ON COLUMN asqa_standards.asqa_url IS 'Link to official ASQA documentation';
COMMENT ON COLUMN asqa_standards.version IS 'Standards version: 2015 or 2025';
