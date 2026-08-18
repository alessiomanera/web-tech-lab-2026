-- schema.sql
-- Database schema for the Museum Ticketing & AI Cultural Guide application.
-- Uses raw SQLite with FOREIGN KEY constraints.
-- Run via database.init_db() to initialize the database.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    preferences TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS museums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    city TEXT NOT NULL DEFAULT 'Italy',
    image_url TEXT
);

CREATE TABLE IF NOT EXISTS exhibitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    museum_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    FOREIGN KEY (museum_id) REFERENCES museums (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    museum_id INTEGER,
    title TEXT NOT NULL,
    tagline TEXT NOT NULL,
    city TEXT NOT NULL,
    theme TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 120,
    base_price REAL NOT NULL DEFAULT 25.0,
    badge TEXT,
    included_items_json TEXT NOT NULL DEFAULT '[]',
    available_addons_json TEXT NOT NULL DEFAULT '[]',
    description TEXT NOT NULL,
    highlights TEXT,
    image_url TEXT,
    is_featured INTEGER DEFAULT 0,
    FOREIGN KEY (museum_id) REFERENCES museums (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_code TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    experience_id INTEGER NOT NULL,
    visit_date TEXT NOT NULL,
    time_slot TEXT NOT NULL,
    guests_count INTEGER NOT NULL DEFAULT 1,
    selected_addons_json TEXT NOT NULL DEFAULT '[]',
    total_price REAL NOT NULL DEFAULT 0.0,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Confirmed',
    feedback_rating INTEGER,
    feedback_text TEXT,
    feedback_date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (experience_id) REFERENCES experiences (id) ON DELETE CASCADE
);
