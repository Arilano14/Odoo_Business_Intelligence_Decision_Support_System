from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DimDate(Base):
    __tablename__ = "dim_date"
    date_id = Column(Date, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    quarter = Column(Integer)

class DimCustomer(Base):
    __tablename__ = "dim_customer"
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    segment = Column(String)
    region = Column(String)

class DimSupplier(Base):
    __tablename__ = "dim_supplier"
    supplier_id = Column(Integer, primary_key=True)
    supplier_name = Column(String)

class DimProduct(Base):
    __tablename__ = "dim_product"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    category = Column(String)

class DimDepartment(Base):
    __tablename__ = "dim_department"
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String)

class FactSales(Base):
    __tablename__ = "fact_sales"
    sales_id = Column(Integer, primary_key=True)
    date_id = Column(Date, ForeignKey("dim_date.date_id"))
    customer_id = Column(Integer, ForeignKey("dim_customer.customer_id"))
    product_id = Column(Integer, ForeignKey("dim_product.product_id"))
    sales_amount = Column(Float)
    quantity = Column(Float)
    margin = Column(Float)

class FactInventory(Base):
    __tablename__ = "fact_inventory"
    inventory_id = Column(Integer, primary_key=True)
    date_id = Column(Date, ForeignKey("dim_date.date_id"))
    product_id = Column(Integer, ForeignKey("dim_product.product_id"))
    stock_level = Column(Float)
    stock_in = Column(Float)
    stock_out = Column(Float)

class FactPurchase(Base):
    __tablename__ = "fact_purchase"
    purchase_id = Column(Integer, primary_key=True)
    date_id = Column(Date, ForeignKey("dim_date.date_id"))
    supplier_id = Column(Integer, ForeignKey("dim_supplier.supplier_id"))
    product_id = Column(Integer, ForeignKey("dim_product.product_id"))
    purchase_amount = Column(Float)
    lead_time_days = Column(Integer)

class FactFinance(Base):
    __tablename__ = "fact_finance"
    finance_id = Column(Integer, primary_key=True)
    date_id = Column(Date, ForeignKey("dim_date.date_id"))
    revenue = Column(Float)
    expense = Column(Float)
    cash_in = Column(Float)
    cash_out = Column(Float)

class FactCRM(Base):
    __tablename__ = "fact_crm"
    crm_id = Column(Integer, primary_key=True)
    date_id = Column(Date, ForeignKey("dim_date.date_id"))
    lead_count = Column(Integer)
    conversion_rate = Column(Float)
    expected_revenue = Column(Float)
