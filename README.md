\# 🚌 Bus Reservation System



This is a simple bus reservation website I built using Flask. The idea was to make the basic bus booking process easier — a user can log in, check the available buses, choose a seat, enter passenger details and go through the payment page.



I also added a separate admin side to manage the bus information and keep track of reservations.



\## ✨ What the project can do



\### 👤 Passenger Features



\* 🔐 User login

\* 🚌 View available buses

\* 🔎 Search and select a bus

\* 💺 Choose an available seat

\* 🎫 Book a bus ticket

\* 💳 Go through the payment page

\* ✅ Get a booking/payment confirmation

\* 📋 View passenger and booking details



\### 👨‍💼 Admin Features



\* 🔐 Admin login

\* 🚌 Add and manage bus information

\* 📋 View bus details

\* 👥 Manage passenger and booking information

\* 📊 Keep track of reservations



\### 🎨 User Interface



\* Simple and clean interface

\* Easy navigation

\* Separate passenger and admin pages

\* Interactive seat selection



\## 🛠️ Technologies Used



| Technology | Purpose                          |

| ---------- | -------------------------------- |

| 🐍 Python  | Backend programming              |

| 🌐 Flask   | Web application framework        |

| HTML5      | Website structure                |

| CSS3       | Styling and responsive design    |

| JavaScript | Client-side interactivity        |

| JSON       | Bus and application data storage |



\## 📁 Project Structure



```text

Bus-Reservation-System/

│

├── app.py

├── buses.json

├── requirements.txt

├── .gitignore

├── README.md

│

└── templates/

&#x20;   ├── admin.html

&#x20;   ├── index.html

&#x20;   ├── login.html

&#x20;   ├── passenger.html

&#x20;   ├── payment.html

&#x20;   ├── payment\_success.html

&#x20;   └── static/

&#x20;       └── style.css

```



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone https://github.com/Sanjana-MK24/Bus-Reservation-System.git

```



\### 2. Open the project folder



```bash

cd Bus-Reservation-System

```



\### 3. Create a virtual environment



```bash

python -m venv .venv

```



\### 4. Activate the virtual environment



\#### Windows — Git Bash



```bash

source .venv/Scripts/activate

```



\#### Windows — Command Prompt



```bash

.venv\\Scripts\\activate

```



\### 5. Install the required packages



```bash

pip install -r requirements.txt

```



\## ▶️ Run the Application



Start the Flask application:



```bash

python app.py

```



Then open your browser and visit:



```text

http://127.0.0.1:5000

```



\## 🔄 Application Workflow



```text

User

&#x20; ↓

Login

&#x20; ↓

Search Available Buses

&#x20; ↓

Select Bus

&#x20; ↓

Select Seat

&#x20; ↓

Enter Passenger Details

&#x20; ↓

Payment

&#x20; ↓

Booking Confirmation

```



\## 🔐 Security



The project uses a `.gitignore` file to prevent unnecessary files such as the Python virtual environment from being uploaded to GitHub.



For production deployment, sensitive information such as secret keys and credentials should be stored using environment variables.



\## 🚀 Future Enhancements



\* 🌐 Deploy the application online

\* 🗄️ Integrate MySQL/MongoDB for persistent data storage

\* 📧 Email booking confirmation

\* 📱 SMS/WhatsApp booking notifications

\* 💳 Integrate a real payment gateway

\* 🎫 Generate downloadable PDF tickets

\* 🗺️ Add live bus tracking

\* 🔍 Advanced bus and route search

\* 📊 Advanced admin analytics dashboard

\* 📱 Improve mobile responsiveness



\## 🎯 Why I built this



I built this project to practice developing a complete web application with Flask and to understand how a real booking flow works. It helped me work with routes, HTML templates, form data, sessions, JSON data and the connection between the frontend and backend.



\## 👩‍💻 Author



\*\*Sanjana M Kanaki\*\*



B.Tech — Computer Science \& Engineering (IoT)



\## ⭐ Support



If you find this project useful, consider giving the repository a ⭐ on GitHub!



\---



\*\*Made with ❤️ using Python Flask\*\*



