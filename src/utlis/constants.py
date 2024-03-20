
description = """
        The ClassicModels database comprises several interconnected tables representing entities commonly found in a business scenario. Here's a description of each model:

                Offices: This table represents different offices of a company. It includes attributes such as office code, city, phone, address, state, country, postal code, and territory. Additionally, it utilizes a spatial data type (POINT) to store the office location.

                Employees: This table contains information about employees working in the company. Attributes include employee number, name, contact details, job title, and the office code where they work. It also maintains a hierarchical relationship through the reportsTo attribute, representing the employee to whom they report.

                Customers: This table stores data related to customers who purchase products from the company. Attributes include customer number, name, contact details, address, credit limit, and the employee responsible for sales to that customer. It also utilizes a spatial data type (POINT) to store customer location.

                ProductLines: This table defines different product lines offered by the company. It includes a product line description, both in plain text and HTML format, along with an image representing the product line.

                Products: This table lists individual products offered by the company. Attributes include product code, name, description, vendor details, pricing information, and stock quantity. Each product is associated with a product line from the ProductLines table.

                Orders: This table tracks orders placed by customers. It includes order number, dates (order, required, shipped), order status, customer number, and optional comments.

                OrderDetails: This table contains details of products within each order. It includes order number, product code, quantity ordered, price each, and order line number. It maintains relationships with both the Products and Orders tables.

                Payments: This table records payments made by customers. Attributes include payment details such as check number, payment date, amount, and the customer number associated with the payment.

                These models collectively represent the core entities and relationships within the business domain, facilitating the storage and management of information related to offices, employees, customers, products, orders, and payments. The schema adheres to relational database principles, utilizing primary and foreign keys to establish and maintain relationships between entities."
                
                Offices:

                officeCode: Unique identifier for each office.
                city: Name of the city where the office is located.
                phone: Contact phone number for the office.
                addressLine1: First line of the office address.
                addressLine2: Second line of the office address (optional).
                state: State or region where the office is located (optional).
                country: Country where the office is located.
                postalCode: Postal code for the office address.
                territory: Territory code for the office.
                officeLocation: Spatial data representing the geographic location of the office.
                Employees:

                employeeNumber: Unique identifier for each employee.
                lastName: Last name of the employee.
                firstName: First name of the employee.
                extension: Phone extension for the employee.
                email: Email address of the employee.
                reportsTo: Employee number of the manager to whom this employee reports (nullable).
                jobTitle: Job title or position of the employee.
                officeCode: Code of the office where the employee works, referencing the Offices table.
                Customers:

                customerNumber: Unique identifier for each customer.
                customerName: Name of the customer.
                contactLastName: Last name of the primary contact person.
                contactFirstName: First name of the primary contact person.
                phone: Contact phone number for the customer.
                addressLine1: First line of the customer's address.
                addressLine2: Second line of the customer's address (optional).
                city: City where the customer is located.
                state: State or region where the customer is located (optional).
                postalCode: Postal code for the customer's address (optional).
                country: Country where the customer is located.
                salesRepEmployeeNumber: Employee number of the sales representative for this customer (nullable).
                creditLimit: Credit limit for the customer.
                customerLocation: Spatial data representing the geographic location of the customer.
                ProductLines:

                productLine: Unique identifier for each product line.
                textDescription: Textual description of the product line.
                htmlDescription: HTML formatted description of the product line.
                image: Image representing the product line (stored as a binary large object).
                Products:

                productCode: Unique identifier for each product.
                productName: Name of the product.
                productScale: Scale of the product.
                productVendor: Vendor or manufacturer of the product.
                productDescription: Description of the product.
                quantityInStock: Quantity of the product in stock.
                buyPrice: Price at which the product is bought.
                MSRP: Manufacturer's suggested retail price.
                productLine: Product line to which the product belongs, referencing the ProductLines table.
                Orders:

                orderNumber: Unique identifier for each order.
                orderDate: Date when the order was placed.
                requiredDate: Date by which the order is required.
                shippedDate: Date when the order was shipped (nullable).
                status: Status of the order.
                comments: Additional comments related to the order (optional).
                customerNumber: Customer number associated with the order, referencing the Customers table.
                OrderDetails:

                orderNumber: Order number associated with the order detail.
                productCode: Product code associated with the order detail.
                quantityOrdered: Quantity of the product ordered.
                priceEach: Price of each unit of the product.
                orderLineNumber: Line number indicating the order of the detail within the order.
                Payments:

                checkNumber: Unique identifier for each payment.
                paymentDate: Date when the payment was made.
                amount: Amount of the payment.
                customerNumber: Customer number associated with the payment, referencing the Customers table.
                
                
                

"""