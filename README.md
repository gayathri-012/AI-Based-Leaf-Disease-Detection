# 🌿 AgriScan AI - AI Based Leaf Disease Detection

## 📌 Project Overview

AgriScan AI is an intelligent web-based plant leaf disease detection platform that uses Artificial Intelligence, Computer Vision, and Large Language Models (LLMs) to identify plant diseases from leaf images.

The system allows users to upload leaf images, analyze plant health, detect diseases, determine severity levels, and receive treatment and prevention recommendations. It also includes an AI-powered agricultural chatbot that assists users with disease-related questions and farming guidance.

---

## 🚀 Key Features

### 🔍 AI Disease Detection
- Upload plant leaf images
- Automatic leaf validation
- Disease identification
- Confidence score generation
- Disease severity analysis
- Treatment recommendations
- Prevention suggestions

### 🤖 AI Agricultural Assistant
- Interactive AI chatbot
- Disease-related guidance
- Farming recommendations
- Plant care assistance
- Prevention advice

### 🔐 Authentication System
- User Registration
- Secure Login
- Password Encryption using Bcrypt
- MySQL Database Integration

### 🎨 Modern User Interface
- Responsive design
- Interactive dashboard
- Animated UI components
- Mobile-friendly layout

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS

### Database
- MySQL

### AI & Machine Learning
- OpenRouter API
- GPT-4o Mini
- Computer Vision
- Image Analysis

### Security
- Flask-Bcrypt
- Password Hashing

---

## 📂 Project Structure

```
AI-Based-Leaf-Disease-Detection/
│
├── index.html
├── ai_engine.html
├── aichat.html
├── auth.html
├── app.py
├── auth_app.py
├── README.md
└── assets/
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/gayathri-012/AI-Based-Leaf-Disease-Detection.git
```

### 2. Install Dependencies

```bash
pip install flask
pip install flask-cors
pip install openai
pip install flask-mysqldb
pip install flask-bcrypt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=YOUR_API_KEY
```

### 4. Configure MySQL Database

Create database:

```sql
CREATE DATABASE ai_users;
```

Create users table:

```sql
CREATE TABLE users(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(100),
email VARCHAR(100) UNIQUE,
password VARCHAR(255)
);
```

### 5. Run Authentication Server

```bash
python auth_app.py
```

### 6. Run AI Detection Server

```bash
python app.py
```

---

## 🌱 How It Works

1. User registers and logs in.
2. User uploads a plant leaf image.
3. AI analyzes the image.
4. Disease information is generated.
5. Confidence and severity levels are displayed.
6. Prevention and treatment recommendations are provided.
7. Users can interact with the AI chatbot for additional assistance.

---

## 🎯 Project Objectives

- Early detection of plant diseases
- Reduce crop losses
- Support farmers with AI-powered recommendations
- Improve agricultural productivity
- Provide an easy-to-use disease diagnosis platform

---

## 👩‍💻 Author

**Gayathri**
MCA Graduate

### Skills
- Python
- Flask
- MySQL
- Artificial Intelligence
- Machine Learning
- Web Development
- Computer Vision

---

## 📜 License

This project is developed for educational and research purposes.
