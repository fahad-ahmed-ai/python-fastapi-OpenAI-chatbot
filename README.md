# Open AI Chatbot Backend

## Features

- Real-time chat functionality using WebSockets (Socket.IO)
- Persistent chat history stored in MongoDB
- Utilizes the OpenAI language model for generating responses
- Supports multiple chat sessions and users

## Prerequisites

- Python 3.7 or higher
- MongoDB database
- OpenAI API key

## Installation

1. Clone the repository:

```
git clone https://github.com/fahad-ahmed-ai/python-fastapi-OpenAI-chatbot.git
```

2. Navigate to the project directory:


3. Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Install the required dependencies:

```
pip install -r requirements.txt
```

5. Set up the environment variables:

Create a `.env` file in the project root directory and add the following variables:

```
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
MONGO_URL=your_mongodb_connection_string
DATABASE_NAME=your_mongodb_database_name
```

Replace the placeholders with your actual API keys and MongoDB connection details.

## Running the Application

1. Start the FastAPI server:

```
uvicorn main:application --reload
```

The server will start running at `http://localhost:8000`.

2. Access the application in your web browser:

```
http://localhost:8000
```

You should see the "server is up and running" message.

3. Use the WebSocket connection to interact with the chatbot:

The WebSocket endpoint is located at `http://localhost:8000/socket.io/`.

## API Endpoints

- `GET /`: Returns a success response indicating that the server is running.
- `GET /chat/chat_history`: Retrieves the chat history for a specific session.

## Project Structure

- `main.py`: The main entry point of the application, where the FastAPI app is defined and the routes are included.
- `app/chat/models.py`: Defines the MongoDB model for storing chat history.
- `app/chat/routes.py`: Defines the API routes for the chat functionality.
- `app/chat/views.py`: Implements the logic for generating responses and handling chat history.
- `app/utilities/config.py`: Loads the environment variables and defines the configuration settings.
- `app/utilities/responses.py`: Provides utility functions for generating success and error responses.
- `app/utilities/socketio_instance.py`: Initializes the Socket.IO instance.

## Deployment

To deploy the application, you can use a hosting platform like Heroku, AWS, or DigitalOcean. Make sure to set the environment variables on the deployment platform as well.

## Contributors

- [Sheikh Fahad Ahmed](https://github.com/fahad-ahmed-ai)
