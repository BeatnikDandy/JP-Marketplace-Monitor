CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT UNIQUE NOT NULL,
    username TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    keyword TEXT NOT NULL,
    active INTEGER DEFAULT 1,
    max_price INTEGER,
    marketplace TEXT DEFAULT 'yahoo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
);

CREATE TABLE listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price INTEGER NOT NULL,
    currency TEXT DEFAULT 'JPY',
    url TEXT UNIQUE NOT NULL,
    marketplace TEXT NOT NULL,
    image_url TEXT,
    seller TEXT,
    auction_end TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE listing_search (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER,
    search_id INTEGER,

    FOREIGN KEY(listing_id)
    REFERENCES listings(id),

    FOREIGN KEY(search_id)
    REFERENCES searches(id)
);

CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    price INTEGER NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(listing_id)
    REFERENCES listings(id)
);


CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    listing_id INTEGER NOT NULL,
    notification_type TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id),

    FOREIGN KEY(listing_id)
    REFERENCES listings(id)
);

CREATE INDEX idx_listing_url
ON listings(url);


CREATE INDEX idx_listing_marketplace
ON listings(marketplace);


CREATE INDEX idx_search_keyword
ON searches(keyword);


CREATE INDEX idx_notification_listing
ON notifications(listing_id);
