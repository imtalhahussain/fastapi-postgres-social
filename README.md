# fastapi-postgres-social
A FastAPI + PostgreSQL backend for managing social media posts
It supports creating, reading, updating, and deleting posts.  
This project demonstrates clean architecture with SQLAlchemy models and Pydantic schemas.
--
## Features
- User authentication with JWT
- CRUD operations for posts
- PostgreSQL database integration
- Pydantic schemas for validation
- Automatic API docs with Swagger UI
--
## Project Structure
app/
 ├── main.py          # Entry point
 ├── models.py        # SQLAlchemy models
 ├── schemas.py       # Pydantic schemas
 ├── database.py      # DB connection
 └── routers/         # API routes

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/imtalhahussain/fastapi-postgres-social
   cd FASTAPI
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Install dependencies:
bash
pip install -r requirements.txt

### 6. **Running the App**
```markdown
## Running the App
Start the server:
```bash
uvicorn app.main:app --reload

---

### 7. **API Endpoints**
Document key endpoints.
```markdown
## API Endpoints
- `POST /posts/` → Create a post
- `GET /posts/` → Get all posts
- `GET /posts/{id}` → Get a single post
- `PUT /posts/{id}` → Update a post
- `DELETE /posts/{id}` → Delete a post

## Contributing
Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to change.
## License
This project is licensed under the MIT License.
