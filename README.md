# supply-chain-management-system-python
🏭 Supply Chain Management System (Python + MySQL)

📌 Overview

This project is a database-driven Supply Chain Management System developed using Python (Tkinter) and MySQL.
It provides an interactive GUI to manage suppliers and products while ensuring structured data handling and real-time updates.



 🎯 Objective

* Design a system to manage supplier and product information efficiently
* Implement database operations for real-time data management
* Provide a user-friendly interface for interacting with backend data

🛠️ Technologies Used

* Python (Tkinter for GUI)
* MySQL (Relational Database)
* SQL (CRUD operations & relationships)



⚙️ Features

* Add, update, and delete supplier records
* Manage product inventory and stock levels
* Relational database design with foreign key constraints
* Interactive GUI for real-time data interaction
* Data validation and user-friendly input handling



🧠 System Design

* **Suppliers Table**: Stores supplier details (Name, Contact, Rating)
* **Products Table**: Stores product details with supplier linkage
* **Relationship**: One-to-many relationship between Suppliers and Products


🔍 Key Highlights

* Implemented full CRUD functionality for database operations
* Ensured data consistency using relational constraints
* Built modular Python functions for database interaction
* Designed structured UI for efficient data entry and visualization



📂 Project Structure

* `main.py` → Application source code
* `requirements.txt` → Python dependencies
* `application-preview.jpeg` → Application screenshots



 🚀 How to Run

1. Install dependencies:

```id="n6gqg0"
pip install -r requirements.txt
```

2. Ensure MySQL server is running

3. Update database credentials in code

4. Run the application:

```id="jyzbpl"
python main.py
```



⚠️ Note

* Update MySQL credentials before running
* Database and tables are automatically created on execution


📈 Future Improvements

* Add low-stock alert system
* Implement search and filtering features
* Enhance UI/UX for better usability
* Add authentication for admin access

---
