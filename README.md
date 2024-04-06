Address Book API
## Setup
1. Navigate to the project directory:

   bash
   cd address-book-api
   

2. Install dependencies:

   bash
   pip install -r requirements.txt
   

3. Run the FastAPI server:

   bash
   uvicorn main:app --reload
   

## Usage

Once the server is running, you can access the API documentation at `http://localhost:8000/docs` to interact with the endpoints using Swagger UI.

### Available Endpoints

- `POST /addresses/`: Create a new address.
- `PUT /addresses/{address_id}`: Update an existing address.
- `DELETE /addresses/{address_id}`: Delete an address.
- `GET /address/`: Get all addresses.
- `GET /addresses/within_distance/`: Get addresses within a given distance and location coordinates.

## Additional Notes

- Make sure to set up your database connection string in `SQLALCHEMY_DATABASE_URL` in `main.py` according to your database configuration.
- Modify the database models in the `models.py` file according to your requirements.
