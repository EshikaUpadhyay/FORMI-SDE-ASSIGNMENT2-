# 🏨 Moustache Property Finder Backend API

A Django REST API built for Moustache Escapes to help their tele-calling team quickly identify properties within a 50km radius of a customer-specified location, even with spelling errors in the input.

---

## 🚀 Project Setup

### 🔧 Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### 📦 Installation Steps
```bash
# 1. Clone the repository
$ git clone <repo_url>
$ cd property_finder

# 2. Create a virtual environment
$ python -m venv env
$ source env/bin/activate  # On Windows: env\Scripts\activate

# 3. Install required dependencies
$ pip install -r requirements.txt

# 4. Run migrations (even if not used, needed for Django setup)
$ python manage.py migrate

# 5. Run the development server
$ python manage.py runserver
```

### 🧪 Test the API
Use Postman or curl:
```bash
curl -X POST http://localhost:8000/nearest-property/ \
  -H "Content-Type: application/json" \
  -d '{"query": "Sissu"}'
```

---

## 💡 Problem Statement
Tele-callers often talk to customers who mention the cities or areas they are interested in. These locations can:
- Be typed incorrectly due to fast typing (e.g., "Delih" instead of "Delhi")
- Vary in specificity (city, town, or area names)

The goal was to:
- Take such an input
- Detect the correct intended location (even if misspelled)
- Find all available Moustache properties within a 50 km radius of that place

---

## 🧠 Approach & Justification

### 1. **Django + Django REST Framework**
- Chosen for its ease of use, scalability, and developer-friendly ecosystem.
- Provides clear structure and fast development cycles.

### 2. **RapidFuzz for Fuzzy Matching**
- To deal with fast-typed or slightly misspelled inputs.
- Lightweight and faster than fuzzywuzzy.
- Ensures user input is corrected to the closest city or area using a known dataset.

### 3. **Indian Cities Dataset (CSV)**
- Used for validating and correcting user input.
- Ensures inputs like "Jaipurr" are corrected to "Jaipur".
- Provides fallback coordinates when geocoding fails.

### 4. **OpenStreetMap (Nominatim API)**
- Used to fetch lat/lon of user-inputted locations.
- Used only when the input cannot be resolved using the dataset.

### 5. **Geopy**
- Used to calculate geodesic distance (accurate over the Earth’s surface).
- Helps in checking if a property is within the 50 km radius.

### 6. **pandas**
- For efficient CSV parsing and lookups.
- Ensures that the city dataset can be loaded and searched quickly.

---

## 📁 File Structure
```
property_finder/
├── locator/
│   ├── static/
│   │   ├── property_data.json          # List of Moustache properties with coordinates
│   │   └── indian_cities.csv          # Dataset for known Indian cities/areas
│   ├── views.py                       # API logic
│   ├── utils.py                       # Core fuzzy search + distance logic
│   ├── urls.py                        # App routing
│   └── ...
├── property_finder/
│   └── urls.py                        # Project routing
├── manage.py
└── requirements.txt
```

--- 

## 🙌 Credits
Built with ❤️ by Eshika for Formi's backend evaluation assignment.

