-- Supabase PostgreSQL Schema

-- Organizations Table
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Licenses Table
CREATE TABLE licenses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    license_type VARCHAR(50) NOT NULL, -- e.g., 'Basic', 'Pro', 'Enterprise'
    query_usage INTEGER DEFAULT 0,
    usage_limit INTEGER NOT NULL,
    billing_status VARCHAR(50) NOT NULL, -- e.g., 'Active', 'Suspended'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'User', 'HR Consultant', 'Admin', 'Licensing Manager'
    organization_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Candidates Table
CREATE TABLE candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL, -- the HR consultant who added the candidate
    name VARCHAR(255) NOT NULL,
    resume_url VARCHAR(500),
    skills TEXT[],
    experience VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Search Queries Table
CREATE TABLE search_queries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    candidate_id UUID REFERENCES candidates(id) ON DELETE SET NULL,
    role VARCHAR(255) NOT NULL,
    skills TEXT[],
    experience VARCHAR(100),
    location VARCHAR(255),
    platform VARCHAR(100) NOT NULL,
    boolean_query TEXT NOT NULL,
    xray_query TEXT NOT NULL,
    search_links TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- AI Logs Table
CREATE TABLE ai_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL, -- e.g., 'generate_query', 'extract_skills'
    input_data JSONB,
    output_data JSONB,
    tokens_used INTEGER,
    model_name VARCHAR(100),
    status VARCHAR(50) NOT NULL, -- 'success', 'failure'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
