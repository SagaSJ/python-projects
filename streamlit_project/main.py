import streamlit as st
from tabulate import tabulate
import time
import datetime
import mysql.connector as mysql
import os
import bcrypt

# Database connection
try:
    con = mysql.connect(host="localhost", user="root", password="root", database="SJ_Seller")
    cor = con.cursor()
except mysql.Error as err:
    st.error(f"Error: {err}")

# Streamlit app layout
st.title("Welcome To SJ SELLER")
st.image(r"C:\Users\sagayaraj\OneDrive\Desktop\streamlit\assests\Image\best-seller-badge-logo-icon-golden-color-best-seller-label-icon-stamp-ribbon-design-illustration-vector.jpg")
option = st.sidebar.selectbox("SJ_Seller", ["Customer", "Employee"])

# Initialize session state to track login status
if "is_customer_logged_in" not in st.session_state:
    st.session_state.is_customer_logged_in = False

if "is_employee_logged_in" not in st.session_state:
    st.session_state.is_employee_logged_in = False

if option == "Customer":
    option1 = st.sidebar.radio("Customer", ["Register", "Login"])
elif option == "Employee":
    option1 = None

class Shopping:
    def load(self):
        p = st.progress(0)
        for i in range(1, 101):
            time.sleep(0.01)
            p.progress(i)

    def Customer_Register(self):
        st.title("CUSTOMER REGISTRATION")
        n = st.text_input("User Name")
        g = st.radio("Gender", ["Male", "Female"])
        e = st.text_input("Email ID")
        pn = st.text_input("Phone Number")
        p1 = st.text_input("Password", type="password")
        p2 = st.text_input("Confirm Password", type="password")
        check = st.checkbox("I agree")
        b = st.button("Submit", key="customer_register_submit")

        if b:
            if not check:
                st.error("You must agree to the terms and conditions")
                return

            if not pn.isdigit() or not (1000000000 <= int(pn) <= 9999999999):
                st.error("Please enter a valid phone number")
                return

            users_name = []
            qry = "SELECT user_name FROM Customers"
            cor.execute(qry)
            data = cor.fetchall()
            for i in data:
                users_name.append(i[0])

            if n in users_name:
                st.error("User name already exists")
            else:
                if p1 == p2:
                    hashed_password = bcrypt.hashpw(p1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    qry = "INSERT INTO Customers (user_name, gender, email, phone_number, password) VALUES (%s, %s, %s, %s, %s)"
                    val = (n, g, e, int(pn), hashed_password)
                    cor.execute(qry, val)
                    con.commit()
                    self.load()
                    st.success("Register Success")
                    st.balloons()
                else:
                    st.error("Passwords do not match")

    def Customer_login(self):
        st.title("CUSTOMER LOGIN")
        n = st.text_input("User Name", key="customer_login_user")
        p3 = st.text_input("Password", type="password", key="customer_login_password")
        b = st.button("Submit", key="customer_login_submit")

        if b:
            users_name = []
            qry = "SELECT user_name FROM Customers"
            cor.execute(qry)
            data = cor.fetchall()
            for i in data:
                users_name.append(i[0])

            if n not in users_name:
                st.error("Please create an account")
            else:
                qry = "SELECT password FROM Customers WHERE user_name=%s"
                val = (n,)
                cor.execute(qry, val)
                result = cor.fetchone()

                if result and not bcrypt.checkpw(p3.encode('utf-8'), result[0].encode('utf-8')):
                    st.error("Incorrect password. Please try again..!") 
                else:
                    self.load()
                    st.success("Login Success....!")
                    st.balloons()
                    st.session_state.is_customer_logged_in = True

        if st.session_state.is_customer_logged_in:
            option2 = st.radio("Option", ["View Product", "Order"], key="customer_login_option")
            if option2 == "View Product":
                self.view_products()
            elif option2 == "Order":
                self.order_product()

    def view_products(self):
        st.title("VIEW PRODUCTS")
        stocks = []
        qry = "SELECT * FROM Product"
        cor.execute(qry)
        result = cor.fetchall()
        for i in result:
            stocks.append(i)

        self.display_product_columns(stocks)

    def display_product_columns(self, stocks):
        cols = st.columns(2)
        for i in range(len(stocks)):
            with cols[i % 2]:
                if os.path.exists(stocks[i][1]):
                    st.image(stocks[i][1])
                else:
                    st.error(f"Image not found for {stocks[i][2]}")
                st.write(stocks[i][2])
                st.write(f"Quantity: {stocks[i][3]}")
                st.write(f"Price: {stocks[i][4]}")

    def order_product(self):
        st.title("ORDER PRODUCT")
        n = st.text_input("Product Name", key="order_product_name")
        q = st.number_input("Quantity", min_value=0, key="order_product_quantity")
        b = st.button("Submit", key="order_product_submit")

        if b:
            product_name = []
            qry = "SELECT product_name FROM Product"
            cor.execute(qry)
            data = cor.fetchall()
            for i in data:
                product_name.append(i[0])

            if n not in product_name:
                st.error('Product not found')
                return

            qry = "SELECT * FROM Product WHERE product_name=%s"
            val = (n,)
            cor.execute(qry, val)
            result = cor.fetchall()

            if result and result[0][3] < q:
                st.error(f"Only {result[0][3]} quantity is available")
            else:
                cr_qty = result[0][3] - q
                qry = "UPDATE Product SET qty=%s WHERE product_name=%s"
                val = (cr_qty, n)
                cor.execute(qry, val)
                con.commit()

                total = q * result[0][4]

                date = datetime.datetime.now()

                qry = "INSERT INTO Orders (product_name, order_date, quantity, price, total) VALUES (%s, %s, %s, %s, %s)"
                val = (n, date, q, result[0][4], total)
                cor.execute(qry, val)
                con.commit()

                st.success("Order Success .....!")
                st.balloons()

    def Employee_login(self):
        st.title("EMPLOYEE LOGIN")
        n = st.text_input("Employee ID", key="employee_login_id")
        p = st.text_input("Password", type="password", key="employee_login_password")
        b = st.button("Submit", key="employee_login_submit")

        if b:
            emp_id = []
            qry = "SELECT employee_id FROM Employees"
            cor.execute(qry)
            data = cor.fetchall()
            for i in data:
                emp_id.append(i[0])

            if n not in emp_id:
                st.error("Please create an account")
            else:
                qry = "SELECT password FROM Employees WHERE employee_id=%s"
                val = (n,)
                cor.execute(qry, val)
                result = cor.fetchone()

                if not bcrypt.checkpw(p.encode('utf-8'), result[0].encode('utf-8')):
                    st.error("Incorrect password. Please try again")
                else:
                    self.load()
                    st.success("Login Success...!")
                    st.balloons()
                    st.session_state.is_employee_logged_in = True

        if st.session_state.is_employee_logged_in:
            option2 = st.radio("Option", ["Add Product", "View Product", "Delete Product"], key="employee_option")
            if option2 == "Add Product":
                self.add_product()
            elif option2 == "View Product":
                self.view_products()
            elif option2 == "Delete Product":
                self.delete_product()

    def add_product(self):
        st.title("ADD PRODUCT")
        product_image = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
        product_name = st.text_input("Product Name")
        product_qty = st.number_input("Product Quantity", min_value=1)
        product_price = st.number_input("Product Price", min_value=1)
        submit = st.button("Submit", key="add_product_submit")

        if submit:
            product_image_path = os.path.join(r'C:\Users\sagayaraj\OneDrive\Desktop\streamlit\assests\Image', product_image.name)
            with open(product_image_path, 'wb') as f:
                f.write(product_image.getbuffer())

            qry = "INSERT INTO Product (product_img, product_name, qty, price) VALUES (%s, %s, %s, %s)"
            val = (product_image_path, product_name, product_qty, product_price)
            cor.execute(qry, val)
            con.commit()
            self.load()
            st.success("Product Added Successfully....!")
            st.balloons()

    def delete_product(self):
        st.title("DELETE PRODUCT")
        p = st.text_input("Product Name", key="delete_product_name")
        b = st.button("Submit", key="delete_product_submit")

        if b:
            product_name = []
            qry = "SELECT product_name FROM Product"
            cor.execute(qry)
            data = cor.fetchall()
            for i in data:
                product_name.append(i[0])

            if p not in product_name:
                st.error("Product does not exist")
            else:
                qry = "DELETE FROM Product WHERE product_name=%s"
                val = (p,)
                cor.execute(qry, val)
                con.commit()
                st.success("Product Deleted Successfully")
                st.balloons()

shop = Shopping()

if option == "Customer":
    if option1 == "Register":
        shop.Customer_Register()
    elif option1 == "Login":
        shop.Customer_login()

if option == "Employee":
    shop.Employee_login()
