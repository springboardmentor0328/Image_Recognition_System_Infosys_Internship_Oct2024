-- Create the table
CREATE TABLE user_images (
    id NUMBER PRIMARY KEY,
    username VARCHAR2(255) NOT NULL,
    image_data BLOB,
    image_name VARCHAR2(255),
    timestamp NUMBER
);
