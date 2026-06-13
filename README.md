# Expense Tracker

A flexible, database-agnostic expense tracking application designed for both local development and scalable cloud production.

## 🚀 Key Features

* **Dual-Mode Storage:** Seamlessly toggle between local `expenses.json` and MongoDB Atlas cloud storage.
* **Factory Pattern Architecture:** Database logic is abstracted, allowing you to switch storage engines without modifying core application code.
* **Environment Configuration:** Uses `.env` files for secure credential management.
* **Secure Connectivity:** Built-in SSL/TLS support to handle macOS certificate verification issues for MongoDB Atlas.

## 🛠 Prerequisites

* Python 3.x
* `pip` (Python package manager)
* A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account (for cloud storage mode)

## 📦 Quick Start

1. **Clone the repository:**
```bash
git clone <your-repository-url>
cd <project-folder>

```


2. **Install dependencies:** ```bash
pip install pymongo python-dotenv certifi
```

```

3. **Configure Environment Variables:** Create a `.env` file in the project root with your configuration.

## ⚙️ How It Works

The system uses `manager_factory.py` to determine which database handler to initialize at startup.

* **JSON Mode:** When `DATABASE_TYPE` is not set or is set to `json`, the app uses `DataManager`, which reads and writes to `expenses.json` in your local directory.
* **Mongo Mode:** When `DATABASE_TYPE=mongo` is set, the app switches to `MongoDataManager`. It automatically verifies the secure connection using `certifi` to ensure your data transmission is encrypted.

## 💡 Troubleshooting

* **SSL Certificate Errors:** If you see `[SSL: CERTIFICATE_VERIFY_FAILED]`, this is a common Python/macOS issue. The application is configured to automatically use the `certifi` bundle to bypass local system store limitations.
* **Connection Timeouts:** If the app cannot connect to MongoDB, ensure:
1. Your current IP address is added to the **Network Access** whitelist in your MongoDB Atlas dashboard.
2. Your `MONGO_URI` in the `.env` file contains your correct database username and password.

## 🤝 Development

To verify your connection independently of the main app, you can run:

```bash
python test_connection.py
```