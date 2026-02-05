# Learn & Earn AI - Setup and Run Guide

## 🎯 Project Overview
This is a **Learn & Earn AI Platform** - an educational platform where users can:
- Browse and enroll in courses
- Track their learning progress
- Search for jobs matched to their skills
- Use AI for interview preparation
- Earn skill points and certifications

## 🛠️ Technologies Used
- **Streamlit**: Web application framework
- **SQLite**: Database for storing users, courses, and progress
- **Plotly**: Interactive data visualizations
- **Google Generative AI**: AI-powered features (interview prep, job matching)
- **Pandas & NumPy**: Data processing

---

## 📋 Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

---

## 🚀 Step-by-Step Setup Instructions

### Step 1: Install Required Packages
Open your terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

**Alternative** - Install packages individually:
```bash
pip install streamlit==1.25.0
pip install pandas==1.5.3
pip install numpy==1.24.3
pip install plotly==5.15.0
pip install Pillow==9.5.0
pip install google-generativeai==0.1.0
```

### Step 2: Verify Your Files
Make sure you have these files in your project folder:
- ✅ `learn-and-earn-app.py` (main application)
- ✅ `learn_and_earn_pro.db` (database file)
- ✅ `requirements.txt` (dependencies list)

### Step 3: Run the Application
In your terminal, navigate to the project folder and run:

```bash
streamlit run learn-and-earn-app.py
```

### Step 4: Access the Application
After running the command, Streamlit will:
- Start a local web server
- Automatically open your default browser
- Show the app at: `http://localhost:8501`

If the browser doesn't open automatically, copy the URL from the terminal and paste it into your browser.

---

## 👤 Using the Application

### First Time Users - Registration
1. Click the **"Register"** button on the welcome page
2. Fill in:
   - Username (unique)
   - Email (unique)
   - Password
   - Primary Skill
3. Click **"Register"** to create your account

### Logging In
1. Click the **"Login"** button
2. Enter your username and password
3. Click **"Login"**

### Main Features (After Login)
Once logged in, you can access these features from the sidebar:

1. **Dashboard** - View your learning statistics and progress
2. **Courses** - Browse available courses across different categories
3. **Enrolled Courses** - View and manage courses you've enrolled in
4. **Jobs** - Browse job opportunities
5. **AI Job Matching** - Upload your skills (JSON file) for AI-powered job recommendations
6. **AI Interview Preparation** - Practice with AI-powered interview questions
7. **Profile** - View your profile, skills, and badges
8. **Logout** - Sign out of your account

---

## 🔧 Troubleshooting

### Issue: "Module not found" error
**Solution**: Make sure all packages are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Database is locked" error
**Solution**: Close any other instances of the app and restart:
```bash
# Stop the app (Ctrl+C in terminal)
# Then run again:
streamlit run learn-and-earn-app.py
```

### Issue: AI features not working
**Note**: The Google Generative AI features require an API key. If you see AI-related errors:
- The app will show fallback responses
- You can still use all other features (courses, jobs, profile)
- To enable AI: You need to set up a Google Generative AI API key

### Issue: Port already in use
**Solution**: Streamlit is already running on port 8501. Either:
- Close the existing instance
- Or run on a different port:
```bash
streamlit run learn-and-earn-app.py --server.port 8502
```

### Issue: Browser doesn't open automatically
**Solution**: Manually open your browser and go to:
```
http://localhost:8501
```

---

## 📊 Database Information

The application uses SQLite database (`learn_and_earn_pro.db`) with these tables:
- **users** - User account information
- **courses** - Available courses catalog
- **user_courses** - Course enrollment and progress
- **course_modules** - Course content modules
- **user_skills** - User skills and proficiency levels
- **job_opportunities** - Available jobs
- **user_job_applications** - Job applications tracking
- **user_assignments** - Assignment submissions

The database comes pre-populated with sample courses and jobs!

---

## 💡 Quick Tips

1. **First time?** Create an account and explore the Dashboard
2. **Browse courses** in different categories (Technology, Business, Creative, etc.)
3. **Enroll in courses** to start learning and earning skill points
4. **Check out jobs** that match your skills
5. **Use AI features** for interview preparation

---

## 🆘 Need Help?

If you encounter any issues:
1. Check the terminal for error messages
2. Make sure all dependencies are installed correctly
3. Verify your database file is in the same folder as the Python script
4. Try restarting the application

---

## 📝 Notes

- The application stores all data locally in the SQLite database
- Your progress is automatically saved as you use the app
- The AI features may have limited functionality without proper API configuration
- The app includes sample data to help you get started immediately

---

**Enjoy learning and earning! 🎓💰**
