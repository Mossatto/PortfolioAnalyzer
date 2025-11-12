CREATE SCHEMA IF NOT EXISTS analyzer_schema;
SET search_path TO analyzer_schema, public;

CREATE TYPE transaction_type_enum AS ENUM ('BUY', 'SELL', 'DIVIDEND', 'ADJUST');

CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE asset (
    asset_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    asset_type VARCHAR(20),
    sector VARCHAR(50),
    CONSTRAINT fk_user FOREIGN KEY (user_id)
        REFERENCES "user" (user_id)
        ON DELETE CASCADE
);

CREATE TABLE transaction (
    transaction_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type transaction_type_enum NOT NULL,
    quantity NUMERIC(10, 4) NOT NULL,
    unit_price NUMERIC(15, 6) NOT NULL,
    total_value NUMERIC(15, 6) NOT NULL,
    CONSTRAINT fk_asset FOREIGN KEY (asset_id)
        REFERENCES asset (asset_id)
        ON DELETE RESTRICT
);

CREATE TABLE quote (
    quote_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL,
    quote_date DATE NOT NULL,
    closing_price NUMERIC(15, 6) NOT NULL,
    UNIQUE (asset_id, quote_date),
    CONSTRAINT fk_asset_quote FOREIGN KEY (asset_id)
        REFERENCES asset (asset_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_transaction_date ON transaction (transaction_date);
CREATE INDEX idx_asset_ticker ON asset (ticker);

