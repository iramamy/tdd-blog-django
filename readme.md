# 📝 Django Blog with TDD 🚀

This project is a **simple blog application** built using **Django**. It follows the principles of **Test-Driven Development (TDD)**, ensuring robust functionality through automated tests. Users can **register**, **update their profile**, and perform standard **blog post operations** such as creating, updating, and deleting posts.

---

## 🌟 Features

### 🔐 **User Management**

- User **Signup & Signin**
- **Profile Update**: Users can update their personal information.

### 🖊️ **Blog Post Operations**

- **Create, Update, and Delete** Blog Posts

### 🛡️ **Authentication**

- Only **authenticated users** can manage posts.

---

## ⚙️ Technologies Used

- **Backend:** Django
- **Testing:** Django’s `TestCase`
- **Database:** SQLite (default)

---

## 🧪 Tests

This application follows a **TDD approach**, ensuring that every feature is thoroughly tested before implementation.

### ✅ **Key Tests:**

1. **User Creation and Authentication:**

   - Tests for **signup** and **login** functionalities.

2. **User Profile Update:**

   - Verifies that **profile updates** are working correctly.

3. **Blog Post CRUD:**
   - Tests for **Create, Update, and Delete** operations, ensuring proper **user permissions**.

---

## 🛠️ Setups

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/iramamy/tdd-blog-django.git
   cd tdd-blog-django
   ```

2. **Create a virtual environment:**

```bash
python -m venv env
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

To run all the tests, use the following command:

4. **Run tests:**

```bash
python manage.py test
```

## Contributing

Pull requests are welcome. For major changes, please open an issue to discuss what you would like to change.
