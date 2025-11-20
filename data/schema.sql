PRAGMA foreign_keys = ON;

-- -------------------------
-- Users Table
-- -------------------------
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------
-- Instagram Accounts
-- -------------------------
CREATE TABLE IF NOT EXISTS ig_accounts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  handle TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_ig_accounts_user_id ON ig_accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_ig_accounts_handle ON ig_accounts(handle);

-- -------------------------
-- KPI Logs
-- -------------------------
CREATE TABLE IF NOT EXISTS kpi_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ig_handle TEXT NOT NULL,
  followers INTEGER DEFAULT 0,
  likes INTEGER DEFAULT 0,
  reach INTEGER DEFAULT 0,
  impressions INTEGER DEFAULT 0,
  engagement_rate REAL DEFAULT 0,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_kpi_logs_handle ON kpi_logs(ig_handle);
CREATE INDEX IF NOT EXISTS idx_kpi_logs_timestamp ON kpi_logs(timestamp);

-- -------------------------
-- Reports Table
-- -------------------------
CREATE TABLE IF NOT EXISTS reports (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  ig_handle TEXT,
  pdf_path TEXT NOT NULL,
  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);
