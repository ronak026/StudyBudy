# StudyBud

StudyBud is a Django-based web application designed for collaborative learning and community discussions. Users can create rooms based on topics, join conversations, send messages, and connect with other learners.

## Features

- **User Authentication:** Register, login, logout, and manage your profile.
- **Rooms & Topics:** Create, update, and delete discussion rooms organized by topics.
- **Messaging:** Real-time threaded conversations within rooms.
- **Participants:** View and interact with other users in each room.
- **Profile Customization:** Upload avatars and edit your profile.
- **Responsive Design:** Modern UI with pastel/dark theme and glassmorphism effects.

## Getting Started

### Prerequisites

- Python 3.8+
- Django 4.x
- Pillow (for image uploads)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/studybud.git
   cd studybud
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```sh
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

6. **Access the app:**
   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Project Structure

```
studybud/
├── base/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── manage.py
└── requirements.txt
```

## Customization

- **Themes:** Edit `static/style/style.css` for custom colors and styles.
- **Avatars:** User profile images are stored in `media/avatars/`.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

---

**Made with Django & ❤️ by the StudyBud
