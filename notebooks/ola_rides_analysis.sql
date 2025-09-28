CREATE DATABASE IF NOT EXISTS ola_ride_analysis;
USE ola_ride_analysis;

CREATE TABLE IF NOT EXISTS ola_rides (
    Date DATE,
    Time TIME,
    Booking_ID VARCHAR(50) PRIMARY KEY,
    Customer_ID VARCHAR(50),
    Ride_Status VARCHAR(30),
    Booking_Status VARCHAR(30),
    Vehicle_Type VARCHAR(50),
    Ride_Distance DECIMAL(10,2) NULL,
    Booking_Value INT,
    Payment_Method VARCHAR(30),
    Driver_Ratings DECIMAL(3,2) NULL,
    Customer_Rating DECIMAL(3,2) NULL,
    Customer_Cancelled TINYINT,
    Driver_Cancelled TINYINT,
    Cancellation_Reason VARCHAR(100),
    Incomplete_Rides_Flag TINYINT,
    Incomplete_Rides_Reason VARCHAR(100),
    Date_Time DATETIME,
    Hour INT,
    Day INT,
    Is_Weekend TINYINT,
    Month VARCHAR(10)
);

SELECT * FROM ola_rides;

-- 1. Retrieve all successful bookings:

SELECT COUNT(*) AS Successful_Bookings
FROM ola_rides
WHERE Booking_Status = 'Success';

-- 2. Find the average ride distance for each vehicle type:

SELECT Vehicle_Type, ROUND(AVG(Ride_Distance),2) AS Avg_Ride_Distance
FROM ola_rides
GROUP BY Vehicle_Type;

-- 3. Get the total number of cancelled rides by customers:

SELECT SUM(Customer_Cancelled) AS Total_Customer_Cancellations
FROM ola_rides;

-- 4. List the top 5 customers who booked the highest number of rides:

SELECT Customer_ID, COUNT(*) AS Total_Rides
FROM ola_rides
GROUP BY Customer_ID
ORDER BY Total_Rides DESC
LIMIT 5;

-- 5. Get the number of rides cancelled by drivers due to personal and car-related issues:

SELECT COUNT(*) AS Cancelled_rides
FROM ola_rides
WHERE Driver_Cancelled = 1 AND Cancellation_Reason = 'Personal & Car related issue';

-- 6. Find the maximum and minimum driver ratings for Prime Sedan bookings:

SELECT MIN(Driver_Ratings) AS min_rating, 
	   MAX(Driver_Ratings) AS max_rating
FROM ola_rides
WHERE Vehicle_Type = "Prime Sedan" AND Driver_Ratings != 0;

-- 7. Retrieve all rides where payment was made using UPI:

SELECT *
FROM ola_rides
WHERE Payment_Method = "UPI";

-- 8. Find the average customer rating per vehicle type:

SELECT Vehicle_Type, ROUND(AVG(Customer_Rating),2) AS Avg_Customer_Rating
FROM ola_rides
GROUP BY Vehicle_Type
ORDER BY avg_customer_rating DESC;

-- 9. Calculate the total booking value of rides completed successfully:

SELECT SUM(Booking_Value) AS Total_Booking_Value
FROM ola_rides
WHERE Ride_Status = "Completed";

-- 10. List all incomplete rides along with the reason

SELECT Booking_ID, Customer_ID, Booking_Status, Ride_Status, Incomplete_Rides_Reason
FROM ola_rides
WHERE Incomplete_Rides_Flag = 1;


