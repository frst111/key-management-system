# key-management-system

To launch the Key Management System project, follow these steps:
----------------------------------------------------------------

Clone the repository:
---------------------
git clone https://github.com/frst111/key-management-system.git

Set up the backend:
-------------------
cd key-management-system/backend
python -m venv venv

Activate the virtual environment:
--------------------------------
venv\Scripts\activate

Install dependencies:
---------------------
pip install -r requirements.txt

Run MongoDB.
-----------

Populate the database:
----------------------
python app/populate.py

Start the backend server:
------------------------
uvicorn app.main:app --reload


Set Up Frontend:
----------------
cd ../frontend
npm install
npm start


To use the application, open your browser and go to http://localhost:3000. Select a user type and click "Pick Up Key" to assign a key. To return a key, find it in the "All Keys" table and click "Return Key". View all keys in use, keys that have been returned, and all keys with their status.
P.S to make monthly inspection button and all keys will be returned.




