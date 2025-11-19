-- V1: Initial schema for HRIS integration system

-- =========================================
-- 1. Create ENUM for HRIS types (ALL CAPS)
-- =========================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'hris_type') THEN
        CREATE TYPE hris_type AS ENUM (
            'SAP_SUCCESSFACTORS',
            'WORKDAY',
            'ORACLE_HCM_CLOUD',
            'UKG',
            'BAMBOOHR',
            'ADP',
            'GUSTO',
            'PAYCOR',
            'PAYCOM'
        );
    END IF;
END
$$;

-- =========================================
-- 2. Create base provider table
-- =========================================
CREATE TABLE IF NOT EXISTS hris_provider (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type hris_type NOT NULL,
    creds JSONB NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Unique: only one active provider allowed
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_hris_provider
ON hris_provider ((is_active))
WHERE is_active = TRUE;


-- =========================================
-- 4. Create integration configuration table
-- =========================================
CREATE TABLE IF NOT EXISTS integration_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES hris_provider(id) ON DELETE CASCADE,

    config JSONB NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Only one active config per provider
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_config_per_provider
ON integration_config (provider_id)
WHERE is_active = TRUE;


-- =========================================
-- 6. Logs table
-- =========================================
CREATE TABLE IF NOT EXISTS integration_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES hris_provider(id) ON DELETE SET NULL,

    event_type TEXT NOT NULL,
    message TEXT,
    details JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================================
-- 7. Update timestamp trigger
-- =========================================
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Provider trigger
DROP TRIGGER IF EXISTS trg_update_timestamp_provider ON hris_provider;
CREATE TRIGGER trg_update_timestamp_provider
BEFORE UPDATE ON hris_provider
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Integration config trigger
DROP TRIGGER IF EXISTS trg_update_timestamp_config ON integration_config;
CREATE TRIGGER trg_update_timestamp_config
BEFORE UPDATE ON integration_config
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
