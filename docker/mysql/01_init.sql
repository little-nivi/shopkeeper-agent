
CREATE DATABASE IF NOT EXISTS meta CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE DATABASE IF NOT EXISTS dw CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE meta;

CREATE TABLE IF NOT EXISTS table_info (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    role VARCHAR(16) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS column_info (
    id VARCHAR(128) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    type VARCHAR(64) NOT NULL,
    role VARCHAR(16) NOT NULL,
    examples TEXT,
    description TEXT,
    alias TEXT,
    table_id VARCHAR(64) NOT NULL,
    FOREIGN KEY (table_id) REFERENCES table_info(id)
);

CREATE TABLE IF NOT EXISTS metric_info (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    relevant_columns TEXT,
    alias TEXT
);

CREATE TABLE IF NOT EXISTS column_metric (
    column_id VARCHAR(128) NOT NULL,
    metric_id VARCHAR(64) NOT NULL,
    PRIMARY KEY (column_id, metric_id),
    FOREIGN KEY (column_id) REFERENCES column_info(id),
    FOREIGN KEY (metric_id) REFERENCES metric_info(id)
);

USE dw;

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id VARCHAR(64) PRIMARY KEY,
    customer_name VARCHAR(128),
    gender VARCHAR(16),
    member_level VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id INT PRIMARY KEY,
    day INT,
    month INT,
    quarter VARCHAR(8),
    year INT
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id VARCHAR(64) PRIMARY KEY,
    product_name VARCHAR(128),
    brand VARCHAR(64),
    category VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS dim_region (
    region_id VARCHAR(64) PRIMARY KEY,
    region_name VARCHAR(64),
    province VARCHAR(64),
    country VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS fact_order (
    order_id VARCHAR(64) PRIMARY KEY,
    customer_id VARCHAR(64),
    product_id VARCHAR(64),
    region_id VARCHAR(64),
    date_id INT,
    order_amount DECIMAL(10,2),
    order_quantity INT,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

INSERT INTO dim_date (date_id, day, month, quarter, year) VALUES
(20240101, 1, 1, 'Q1', 2024),
(20240102, 2, 1, 'Q1', 2024),
(20240401, 1, 4, 'Q2', 2024),
(20240701, 1, 7, 'Q3', 2024),
(20241001, 1, 10, 'Q4', 2024);

INSERT INTO dim_region (region_id, region_name, province, country) VALUES
('R001', '华北', '北京', '中国'),
('R002', '华北', '天津', '中国'),
('R003', '华东', '上海', '中国'),
('R004', '华东', '江苏', '中国'),
('R005', '华南', '广东', '中国');

INSERT INTO dim_product (product_id, product_name, brand, category) VALUES
('P001', '手机', '品牌A', '电子产品'),
('P002', '电脑', '品牌A', '电子产品'),
('P003', '耳机', '品牌B', '电子产品'),
('P004', '衣服', '品牌C', '服装'),
('P005', '鞋子', '品牌C', '服装');

INSERT INTO dim_customer (customer_id, customer_name, gender, member_level) VALUES
('C001', '张三', '男', 'VIP'),
('C002', '李四', '女', '普通'),
('C003', '王五', '男', 'VIP'),
('C004', '赵六', '女', '普通'),
('C005', '钱七', '男', '普通');

INSERT INTO fact_order (order_id, customer_id, product_id, region_id, date_id, order_amount, order_quantity) VALUES
('O001', 'C001', 'P001', 'R001', 20240101, 5999.00, 1),
('O002', 'C002', 'P003', 'R003', 20240102, 299.00, 2),
('O003', 'C003', 'P002', 'R001', 20240401, 8999.00, 1),
('O004', 'C004', 'P004', 'R005', 20240701, 199.00, 3),
('O005', 'C005', 'P005', 'R004', 20241001, 299.00, 2),
('O006', 'C001', 'P003', 'R002', 20240101, 299.00, 1),
('O007', 'C002', 'P001', 'R003', 20240401, 5999.00, 1),
('O008', 'C003', 'P004', 'R001', 20240701, 199.00, 2),
('O009', 'C004', 'P002', 'R005', 20241001, 8999.00, 1),
('O010', 'C005', 'P001', 'R004', 20240102, 5999.00, 1);
