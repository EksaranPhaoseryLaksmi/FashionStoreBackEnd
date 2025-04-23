from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Terms(db.Model):
    tablename = "terms"

    terms_id = db.Column(db.Integer, primary_key=True)
    terms_description = db.Column(db.String(50), nullable=False)
    terms_due_days = db.Column(db.Integer, nullable=False)
    
class Invoices (db.Model):
    tablename = "invoices"

    invoice_id = db.Column(db.Integer, primary_key=True)
    # vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.vendor_id'), nullable=False)
    invoice_number = db.Column(db.Integer, nullable=False)
    invoice_date = db.Column(db.DateTime, nullable=False)
    invoice_total = db.Column(db.Float, nullable=False)
    payment_total = db.Column(db.Float, nullable=False, default=0.00)
    credit_total  = db.Column(db.Float, nullable=False, default=0.00)
    terms_id = db.Column(db.Integer, db.ForeignKey('terms.term_id'), nullable=False)
    invoice_due_date = db.Column(db.DateTime, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=None)
    
class departments (db.Model):
    tablename = "Departments"
    
    departments_number= db.Column(db.Integer, primary_key=True)
    departments_name = db.Column(db.VARCHAR(45),nullable = False)
    
class employees (db.Model):    
    tablename = "Employees"
    
    employee_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.VARCHAR(45),nullable = False)
    first_name = db.Column(db.VARCHAR(45),nullable = False) 
    department_number = db.Column(db.Integer,nullable = False)
    manager_id = db.Column(db.Integer,nullable = False)
    
class general_ledger_accounts (db.Model):
    tablename = "general_leger_accounts"
    
    account_number = db.Column(db.Integer, primary_key=True)
    account_description = db.Column(db.VARCHAR(50),nullable = False)
    
class invoice_archive (db.Model):
    tablename = "Invoice_archive"
    
    invoice_id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, nullable = False)
    invoice_number = db.Column(db.VARCHAR(50),nullable = False)
    invoice_date = db.Column(db.DATE,nullable = False)
    invoice_total = db.Column(db.DECIMAL(9,2),nullable = False)
    payment_total = db.Column(db.DECIMAL(9,2),nullable = False)
    credits_total = db.Column(db.DECIMAL(9,2),nullable = False)
    terms_id = db.Column(db.Integer, nullable = False)
    invoice_due_date = db.Column(db.DATE, nullable = False)
    payment_date = db.Column(db.DATE, nullable = False)
    
class invoice_line_iterms (db.Model):
    tablename = "Invoice_line_iterms"
    
    invoice_id = db.Column(db.Integer, primary_key=True)
    invoice_sequence = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.Integer, nullable = False)
    line_iterm_amount = db.Column(db.DECIMAL(9,2), nullable = False)
    line_iterm_description = db.Column(db.VARCHAR(100),nullable = False)

class projects (db.Model):
    tablename = "projects"
    
    project_number = db.Column(db.CHAR(10), nullable=True)
    employee_id = db.Column(db.Integer, primary_key=True)

class project_tracker (db.Model):
    tablename = "project_tracker"
    
    id=db.Column(db.Integer, primary_key=True)
    project_number = db.Column(db.CHAR(10), nullable=True)
    title = db.Column(db.VARCHAR(100),nullable=True)
    description=db.Column(db.VARCHAR(250),nullable=False)
    priority=db.Column(db.Integer,nullable=False)
    deadline=db.Column(db.DATE,nullable=False)
    status=db.Column(db.Integer,nullable=False)
    created_by=db.Column(db.Integer,nullable=False)

class brands (db.Model):
    tablename = "brands"
    
    BrandID=db.Column(db.Integer, primary_key=True)
    BrandName = db.Column(db.VARCHAR(100), nullable=True)
    BrandDescription = db.Column(db.VARCHAR(100),nullable=True)
    BrandWebsite=db.Column(db.VARCHAR(250),nullable=False)

class products (db.Model):
    tablename = "products"
    
    ProductID=db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.VARCHAR(100), nullable=True)
    Description = db.Column(db.VARCHAR(100),nullable=True)
    Size=db.Column(db.Integer,nullable=False)
    Price=db.Column(db.Integer,nullable=False)
    Color=db.Column(db.VARCHAR(100),nullable=False)
    ImageURL=db.Column(db.VARCHAR(100),nullable=True)
    
class orders (db.Model):
    tablename = "orders"
    
    OrderID=db.Column(db.Integer, primary_key=True)
    Customer_ID = db.Column(db.Integer, nullable=True)
    OrderDate = db.Column(db.DATE,nullable=True)
    TotalAmount=db.Column(db.Integer,nullable=False)
    ShoppingAddress = db.Column(db.VARCHAR(100),nullable=True)
    OrderStatus = db.Column(db.VARCHAR(100),nullable=True)
    ProductID = db.Column(db.Integer, nullable=True)
    Quantity = db.Column(db.Integer, nullable=True)
    Phone = db.Column(db.VARCHAR(100),nullable=True)
    Note = db.Column(db.VARCHAR(500),nullable=True)

class order_items (db.Model):
    
    tablename="order_items"
    
    OrderItemsID = db.Column(db.Integer, primary_key=True)
    Order_ID = db.Column(db.Integer, nullable=True)
    Product_ID = db.Column(db.Integer, nullable=True)
    Quantity = db.Column(db.Integer, nullable=True)
    ItemPrice = db.Column(db.Integer, nullable=True)

class vendor_contacts (db.Model):
    tablename = "Vendor_contacts"
    
    vendor_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.VARCHAR(50),nullable = False)
    first_name = db.Column(db.VARCHAR(50),nullable = False) 
    
class vendors (db.Model):
    tablename = "Vendors"
    
    vendor_id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.VARCHAR(50),primary_key=True)
    vendor_address1 = db.Column(db.VARCHAR(50),nullable = False)
    vendor_daddress2 = db.Column(db.VARCHAR(50),nullable = False)
    vendor_city = db.Column(db.VARCHAR(50),nullable = False)
    vendor_state = db.Column(db.CHAR(2),nullable = False)
    vendor_zip_code = db.Column(db.VARCHAR(20),nullable = False)
    vendor_phone = db.Column(db.VARCHAR(50),nullable = False)
    vendor_contact_last_name = db.Column(db.VARCHAR(50),nullable = False)
    vendor_contact_first_name = db.Column(db.VARCHAR(50),nullable = False)
    default_terms_id = db.Column(db.Integer, nullable = False)
    default_account_number = db.Column(db.Integer, nullable = False)
    
class Gender(db.Model):
    __tablename__ = 'gender'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Add a primary key
    name = db.Column(db.String(50), nullable=False)  # Example additional field
