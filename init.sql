-- 部員テーブル
CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    number INTEGER,
    position VARCHAR(10)
);

-- 予定テーブル
CREATE TABLE IF NOT EXISTS schedules (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    time TIME NOT NULL,
    location VARCHAR(100),
    type VARCHAR(20) -- 'Practice', 'Match'
);

-- 出欠テーブル
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    member_id INTEGER REFERENCES members(id),
    schedule_id INTEGER REFERENCES schedules(id),
    status VARCHAR(20) DEFAULT 'Pending', -- 'Present', 'Absent'
    UNIQUE(member_id, schedule_id)
);

-- 初期データ（テスト用）
INSERT INTO members (name, number, position) VALUES 
('Inoue', 10, 'FIXO'),
('Tanaka', 7, 'ALA');

INSERT INTO schedules (date, time, location, type) VALUES 
('2025-02-01', '18:00', 'University Gym', 'Practice');