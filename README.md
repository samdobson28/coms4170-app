# Mexican Food in NYC - Learning Application

A Flask-based web application that helps users learn about Mexican food culture, language, and locations in New York City. The application includes interactive learning modules, a quiz, and a map of Mexican food locations.

## Features

- **Interactive Learning Modules**

  - Culture Guide: Learn about different Mexican foods
  - Language Guide: Essential Spanish phrases for dining
  - Map: Discover Mexican food locations in NYC

- **Interactive Quiz**

  - Multiple question types:
    - Image matching: Match food images to their names
    - Translation: Practice essential Spanish phrases
    - True/False: Test your knowledge of Mexican food facts
    - Multiple Choice: Choose the correct answer from options
    - Multiple Select: Select all correct answers
  - Progress tracking with visual indicators
  - Detailed results showing:
    - Overall score and percentage
    - Individual question results
    - Correct answers for missed questions
  - Support for skipping questions
  - Ability to review and retry the quiz

- **Personal Guidebook**
  - Save favorite foods, phrases, and locations
  - Access saved items anytime
  - Organize saved items by category

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, JavaScript, jQuery, Bootstrap
- **Database**: SQLite
- **Maps**: Leaflet.js
- **Data Storage**: JSON files

## Project Structure

```
.
├── app.py                  # Flask application and routes
├── static/
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   ├── images/            # Food and location images
│   └── data/              # JSON data files
│       ├── quiz.json      # Quiz questions and answers
│       ├── lessons.json   # Learning content
│       └── places.json    # Location data
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Home page
│   ├── culture.html       # Culture guide
│   ├── language.html      # Language guide
│   ├── map.html           # Map of locations
│   ├── quiz.html          # Quiz interface
│   └── guidebook.html     # Personal guidebook
└── user_progress.db       # SQLite database (created on first run)
```

## Setup and Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   The database will be automatically created when you first run the application.

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Data Structure

### Quiz Data (`static/data/quiz.json`)

Contains all quiz questions with their types, options, and correct answers:

```json
{
    "questions": [
        {
            "id": "q1",
            "type": "image_match",
            "question": "Match the labels to the correct images:",
            "images": ["chile-relleno", "conchas", ...],
            "correct_matches": {...}
        },
        ...
    ]
}
```

### Learning Content (`static/data/lessons.json`)

Contains structured data for the culture and language guides:

```json
{
    "foods": [...],
    "phrases": [...],
    "places": [...]
}
```

## Database Schema

### `quiz_answers` Table

- `id`: Primary key
- `question_id`: Question identifier
- `answer`: User's answer
- `is_correct`: Boolean indicating if answer was correct
- `timestamp`: When the answer was submitted

### `page_visits` Table

- `id`: Primary key
- `page`: Page visited
- `timestamp`: When the page was visited

### `saved_items` Table

- `id`: Primary key
- `item_type`: Type of saved item (food, phrase, or place)
- `item_id`: Identifier of the saved item
- `timestamp`: When the item was saved

### Quiz Results Structure

```json
{
    "score": 5,
    "total": 7,
    "results": [
        {
            "question_number": 1,
            "question": "Question text",
            "user_answer": "User's answer",
            "correct_answer": "Correct answer",
            "is_correct": true,
            "type": "question_type"
        },
        ...
    ]
}
```

## Development

### Adding New Content

1. **New Quiz Questions**

   - Add to `static/data/quiz.json`
   - Follow the existing question structure
   - Include all required fields for the question type

2. **New Learning Content**
   - Add to `static/data/lessons.json`
   - Maintain the existing structure
   - Include all required fields for the content type

### Adding New Features

1. **New Routes**

   - Add to `app.py`
   - Include database tracking if needed
   - Create corresponding template

2. **New Templates**
   - Extend from `base.html`
   - Include necessary blocks
   - Add required JavaScript

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
