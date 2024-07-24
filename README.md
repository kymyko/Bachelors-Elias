# Elias Mental Health App

In today’s fast-paced and ever-changing world, mental disorders, also referred to as mental health conditions, represent a significant challenge. These conditions impact individuals of all ages, across diverse social environments and demographics. From anxiety and depression to more severe disorders like bipolar and borderline, mental health conditions have debilitating effects on those affected. The societal stigma surrounding mental health often amplifies the suffering, weakening the ability of individuals to seek help and find peace.

Given these pressing issues, there is a critical need for innovative solutions that provide support, guidance, and empathy to those navigating mental health challenges. The integration of advanced technologies such as artificial intelligence offers an opportunity to revolutionize mental health care, providing tailored and personalized assistance to those in need.

This research endeavors to address this pressing need by developing an online platform equipped with an AI counselor, aimed at fostering psychological support and resilience among individuals facing mental health difficulties.

## Used Technologies

The development of the Elias Mental Health App utilizes a range of technologies to ensure a seamless user experience and robust backend operations. Each component of the app leverages specific technologies suited to its requirements:

### Backend Development

The backend is implemented using Python, specifically with the Flask framework. Flask provides a lightweight and flexible framework for building web applications, making it ideal for this project. The backend handles user authentication, AI chatbot interactions, database operations, and appointment scheduling. The primary database used is PostgreSQL, known for its reliability and performance in handling complex queries and large datasets.

- **Python**: The core programming language used for backend logic and AI functionalities.
- **Flask**: The web framework used to build the server-side application.
- **PostgreSQL**: The relational database management system used to store user, article, and psychologist data.
- **SQLAlchemy**: An ORM (Object-Relational Mapping) tool used for database interactions in a Pythonic way.
- **Flask-Migrate**: Handles database migrations, ensuring the schema evolves as the application grows.

### Frontend Development

The frontend is developed using HTML, CSS, and JavaScript, providing a responsive and user-friendly interface. The design ensures accessibility and ease of use across different devices.

- **HTML**: The markup language used to structure the web pages.
- **CSS**: Used for styling the web pages to create a visually appealing layout.
- **JavaScript**: Adds interactivity to the web pages, particularly for dynamic content updates and form validations.
- **Jinja2**: The templating engine for rendering HTML with dynamic data from the Flask backend.

### AI Chatbot

The AI chatbot is a critical component of the app, providing initial mental health assessments and engaging users in conversations based on a predefined dataset.

- **Natural Language Processing (NLP)**: Utilized to understand and respond to user inputs in a conversational manner.
- **Machine Learning Models**: Developed to predict potential mental health conditions based on user responses.
- **JSON Dataset**: A dataset containing patient profiles and symptoms used to train the AI models.
