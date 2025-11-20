CREATE TABLE employee (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    provider_id UUID NOT NULL REFERENCES hris_provider(id) ON DELETE CASCADE,

    employee_id VARCHAR(50) NOT NULL, -- BambooHR employee ID
    first_name TEXT,
    last_name TEXT,
    preferred_name TEXT,
    display_name TEXT,
    job_title TEXT,
    location TEXT,
    supervisor TEXT,
    department TEXT,
    division TEXT,
    work_email TEXT,
    work_phone TEXT,
    work_phone_extension TEXT,
    photo_url TEXT,

    -- Track record changes
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE(provider_id, employee_id)  -- ensure one record per provider per employee
);
