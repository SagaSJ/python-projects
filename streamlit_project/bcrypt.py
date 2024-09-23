import bcrypt
import mysql.connector as mysql
from mysql.connector.errors import IntegrityError, Error

def hash_password(password):
    """
    Hashes the provided password using bcrypt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def insert_data():
    """
    Connects to the SJ_Seller MySQL database and inserts employees, customers,
    products, and orders data with hashed passwords for employees and customers.
    """
    con = None
    try:
        # Connect to the MySQL database
        con = mysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="SJ_Seller"
        )

        if con.is_connected():
            print("Connected to MySQL database")

            cor = con.cursor()

            # Employees data
            employees = [
                ('123', 'password123'),
                ('234', 'password234')
            ]

            # Customers data
            customers = [
                ('Alex', 'Male', 'Alexander@gmail.com', 1234567890, 'AlexanderTheGreat'),
                ('Cynthia', 'Female', 'Cynthia@gmail.com', 2345678901, 'CynthiaThePrimcess'),
                ('Henry_Williams', 'Male', 'HenryWilliamson@gmail.com', 3456789012, 'HenryWilliamsonsKing'),
                ('Candice', 'Female', 'LilyCandice@gmail.com', 4567890123, 'GlitteringQueen')
            ]

            # Products data
            products = [
                ('prod001', 'C:\\Users\\sagayaraj\\OneDrive\\Pictures\\pythonproject\\Headphone.jpg', 'Headphones', 50, 400.00),
                ('prod002', 'C:\\Users\\sagayaraj\\OneDrive\\Pictures\\pythonproject\\Dumbells.jpg', 'Dumbells', 30, 600.00),
                ('prod003', 'C:\\Users\\sagayaraj\\OneDrive\\Pictures\\pythonproject\\Alziba Skin Care Products.jpg', 'Alziba_Skin_Care', 1000, 1000.00),
                ('prod004', 'C:\\Users\\sagayaraj\\OneDrive\\Pictures\\pythonproject\\HarryPotterBooks.jpg', 'Harrypotter_Books', 60, 750.00),
                ('prod005', 'C:\\Users\\sagayaraj\\OneDrive\\Pictures\\pythonproject\\Playstation.jpg', 'PlayStation_PS4', 25, 3500.00),
                ('prod006', 'C:\\Users\\sagayaraj\\OneDrive\\Pictures\\pythonproject\\Mens Clothing Full Set.jpg', 'MENS_CLOTHES', 150, 500.00)
            ]

            # Orders data
            orders = [
                ('Headphones', '2023-06-28 12:00:00', 2, 400.00, 800.00),
                ('MENS_CLOTHES', '2023-06-28 12:00:00', 1, 500.00, 500.00)
            ]

            # Hash and insert employees with ON DUPLICATE KEY UPDATE
            for employee_id, password in employees:
                hashed_password = hash_password(password)
                try:
                    print(f"Inserting employee {employee_id}")
                    cor.execute("""
                        INSERT INTO Employees (employee_id, password) 
                        VALUES (%s, %s) 
                        ON DUPLICATE KEY UPDATE password=VALUES(password)
                    """, (employee_id, hashed_password))
                    print(f"Inserted employee {employee_id}")
                except IntegrityError as err:
                    print(f"Error inserting employee {employee_id}: {err}")

            # Hash and insert customers with ON DUPLICATE KEY UPDATE
            for user_name, gender, email, phone_number, password in customers:
                hashed_password = hash_password(password)
                try:
                    print(f"Inserting customer {user_name}")
                    cor.execute("""
                        INSERT INTO Customers (user_name, gender, email, phone_number, password) 
                        VALUES (%s, %s, %s, %s, %s) 
                        ON DUPLICATE KEY UPDATE gender=VALUES(gender), email=VALUES(email), phone_number=VALUES(phone_number), password=VALUES(password)
                    """, (user_name, gender, email, phone_number, hashed_password))
                    print(f"Inserted customer {user_name}")
                except IntegrityError as err:
                    print(f"Error inserting customer {user_name}: {err}")

            # Insert products with ON DUPLICATE KEY UPDATE
            for product in products:
                try:
                    print(f"Inserting product {product[0]}")
                    cor.execute("""
                        INSERT INTO Product (product_id, photo_url, product_name, qty, price) 
                        VALUES (%s, %s, %s, %s, %s) 
                        ON DUPLICATE KEY UPDATE photo_url=VALUES(photo_url), product_name=VALUES(product_name), qty=VALUES(qty), price=VALUES(price)
                    """, product)
                    print(f"Inserted product {product[0]}")
                except IntegrityError as err:
                    print(f"Error inserting product {product[0]}: {err}")

            # Insert orders (if duplicates are not expected)
            for order in orders:
                try:
                    print(f"Inserting order for product {order[0]}")
                    cor.execute("INSERT INTO Orders (product_name, order_date, quantity, price, total) VALUES (%s, %s, %s, %s, %s)", order)
                    print(f"Inserted order for product {order[0]}")
                except IntegrityError as err:
                    print(f"Error inserting order for product {order[0]}: {err}")

            # Commit the changes
            con.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # Close the MySQL connection
        if con is not None and con.is_connected():
            cor.close()
            con.close()
            print("MySQL connection is closed")

# Call the function to insert data
insert_data()
