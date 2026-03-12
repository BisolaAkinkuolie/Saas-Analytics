USE saas_analytics;

## Create user tables
CREATE TABLE Users (
	user_id INT auto_increment PRIMARY KEY,
    email VARCHAR(265) NOT NULL UNIQUE,
    full_name VARCHAR(265),
    Company VARCHAR(265),
    Region VARCHAR(100),
    Plan_tier ENUM('free','starter','pro','enterprise'),
    signup_date DATE,
    is_active BOOLEAN DEFAULT TRUE
    );
    
## Create Subscriptions table
CREATE TABLE Subscriptions (
	subscription_id INT auto_increment PRIMARY KEY,
    user_id INT NOT NULL,
    Plan_tier ENUM ('free', 'starter','pro','enterprise'),
    mrr DECIMAL(10,2),
    start_date DATE,
    end_date DATE,
    churn_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    
## Create features table
CREATE TABLE features (
	feature_id INT auto_increment PRIMARY KEY,
    feature_name VARCHAR(265),
    feature_category VARCHAR(100),
    is_premium BOOLEAN DEFAULT FALSE
    );
    
## Create Sessions table
CREATE TABLE sessions(
	session_id INT auto_increment PRIMARY KEY,
    user_id INT NOT NULL,
    session_start datetime,
    session_end datetime,
    device_type ENUM('mobile', 'desktop','tablet'),
    FOREIGN KEY (user_id) REFERENCES Users (user_id)
    );
    
## CREATE Events Table
CREATE TABLE events(
	event_id INT auto_increment PRIMARY KEY,
    user_id int NOT NULL,
    session_id INT NOT NULL,
    feature_id INT NOT NULL,
    event_type VARCHAR(100),
    EVENT_TIMESTAMP DATETIME,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY(feature_id) REFERENCES features(feature_id)
    );