"""
Learn & Earn AI
Purpose:
This project demonstrates handling of structured data, database operations,
basic data analysis, and dashboard-style reporting using Python.

Focus Areas:
- Data storage using SQLite
- Data retrieval and processing using SQL and Pandas
- Visualization of user progress and metrics
- Script maintenance, testing, and debugging
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import random
from datetime import datetime, timedelta
import google.generativeai as genai
import uuid
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import sqlite3
import hashlib
import re
import json

class AdvancedLearnAndEarnPlatform:
    def __init__(self):
        # Enhanced Configuration
        self.SECRET_KEY = "your_secure_secret_key_here"
        
        # Database Connection
        self.conn = sqlite3.connect('learn_and_earn_pro.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Initialize Database and Core Components
        self.initialize_comprehensive_database()
        self.initialize_session_state()
        
        # Load Comprehensive Catalogs
        self.course_catalog = self.create_comprehensive_course_catalog()
        self.job_marketplace = self.create_advanced_job_marketplace()
        self.skill_ecosystem = self.create_skill_ecosystem()

    def initialize_session_state(self):
        # Initialize session state variables if they don't already exist
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False
        if 'user_id' not in st.session_state:
            st.session_state['user_id'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 'Login'

    def initialize_comprehensive_database(self):
        # Expanded Database Schema
        tables = {
            'users': '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    profile_image BLOB,
                    primary_skill TEXT,
                    total_earnings REAL DEFAULT 0,
                    skill_points INTEGER DEFAULT 0,
                    subscription_tier TEXT DEFAULT 'Basic',
                    learning_credits REAL DEFAULT 100.0,
                    account_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME
                )
            ''',
            'courses': '''
                CREATE TABLE IF NOT EXISTS courses (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    category TEXT,
                    difficulty TEXT,
                    price REAL,
                    duration_weeks INTEGER,
                    total_modules INTEGER,
                    skill_points_reward INTEGER
                )
            ''',
            'user_courses': '''
                CREATE TABLE IF NOT EXISTS user_courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    course_id TEXT,
                    enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completion_status TEXT DEFAULT 'In Progress',
                    progress_percentage REAL DEFAULT 0,
                    completed_date DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )
            ''',
            'course_modules': '''
                CREATE TABLE IF NOT EXISTS course_modules (
                    id TEXT PRIMARY KEY,
                    course_id TEXT,
                    title TEXT,
                    content TEXT,
                    video_lecture_url TEXT,
                    assignment_details TEXT,
                    quiz_data TEXT,
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )
            ''',
            'user_skills': '''
                CREATE TABLE IF NOT EXISTS user_skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    skill_name TEXT,
                    proficiency_level TEXT,
                    experience_points INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''',
            'job_opportunities': '''
                CREATE TABLE IF NOT EXISTS job_opportunities (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    company TEXT,
                    description TEXT,
                    required_skills TEXT,
                    salary_range TEXT,
                    location TEXT,
                    remote_friendly BOOLEAN
                )
            ''',
            'user_job_applications': '''
                CREATE TABLE IF NOT EXISTS user_job_applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    job_id TEXT,
                    application_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'Pending',
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (job_id) REFERENCES job_opportunities(id)
                )
            ''',
            'user_assignments': '''
                CREATE TABLE IF NOT EXISTS user_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    course_id TEXT,
                    module_id TEXT,
                    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id),
                    FOREIGN KEY (module_id) REFERENCES course_modules(id)
                )
            '''
        }

        # Create Tables
        for table_name, table_schema in tables.items():
            try:
                self.cursor.execute(table_schema.strip())
            except sqlite3.OperationalError as e:
                st.error(f"Error creating table {table_name}: {e}")
        self.conn.commit()

        # Populate Initial Data if Not Exists
        self.populate_initial_data()

    def populate_initial_data(self):
        # Populate Courses
        courses_data = [
            # Technology
            ('cloud001', 'Cloud Computing Essentials', 'Technology', 'Intermediate', 299.99, 10, 15, 400),
            ('cyber001', 'Cybersecurity Fundamentals', 'Technology', 'Beginner', 199.99, 8, 12, 300),
            ('block001', 'Blockchain Basics', 'Technology', 'Advanced', 399.99, 12, 20, 500),
            
            # Business
            ('fin001', 'Finance for Non-Finance Professionals', 'Business', 'Beginner', 149.99, 6, 10, 200),
            ('ent001', 'Entrepreneurship 101', 'Business', 'Intermediate', 249.99, 8, 12, 300),
            
            # Creative
            ('design001', 'Graphic Design Mastery', 'Creative', 'Advanced', 349.99, 10, 15, 400),
            ('video001', 'Video Editing for Beginners', 'Creative', 'Beginner', 199.99, 6, 10, 200),
            
            # Personal Development
            ('speak001', 'Public Speaking Confidence', 'Personal Development', 'Beginner', 99.99, 4, 8, 150),
            ('lead001', 'Leadership Skills for Managers', 'Personal Development', 'Intermediate', 249.99, 8, 12, 300)
        ]

        # Insert courses into the database if they don't already exist
        for course in courses_data:
            self.cursor.execute('''
                INSERT OR IGNORE INTO courses 
                (id, title, category, difficulty, price, duration_weeks, total_modules, skill_points_reward) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', course)

        self.conn.commit()

        # Populate Modules for Courses
        modules_data = [
            # Modules for "Advanced Digital Marketing Mastery"
            ('mod001', 'ds001', 'SEO Fundamentals', 'Learn the basics of SEO, including on-page and off-page optimization.', 'https://example.com/seo-video', 'Perform an SEO audit for a website.'),
            ('mod002', 'ds001', 'Social Media Strategy', 'Understand how to create effective social media campaigns.', 'https://example.com/social-media-video', 'Design a social media campaign for a product.'),
            
            # Modules for "Professional Machine Learning Engineer"
            ('mod003', 'ai001', 'Python for Machine Learning', 'Learn Python libraries like NumPy, Pandas, and Scikit-learn for ML.', 'https://example.com/python-ml-video', 'Build a simple machine learning model.'),
            ('mod004', 'ai001', 'Deep Learning Techniques', 'Explore neural networks and deep learning frameworks.', 'https://example.com/deep-learning-video', 'Implement a neural network for image classification.')
        ]

        # Insert modules into the database if they don't already exist
        for module in modules_data:
            self.cursor.execute('''
                INSERT OR IGNORE INTO course_modules 
                (id, course_id, title, content, video_lecture_url, assignment_details) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', module)

        self.conn.commit()

        # Populate Job Opportunities
        jobs_data = [
            ('job001', 'Senior AI Engineer', 'TechCorp', 
            'Develop advanced AI solutions and machine learning models', 
            'Machine Learning,Python,AI', '$120,000 - $180,000', 'San Francisco, CA', True),
            ('job002', 'Digital Marketing Specialist', 'MarketingPro', 
            'Create and manage digital marketing campaigns', 
            'Digital Marketing,SEO,Social Media', '$70,000 - $100,000', 'New York, NY', True),
            ('job003', 'Full Stack Web Developer', 'WebInnovate', 
            'Build scalable web applications', 
            'JavaScript,React,Node.js,Python', '$90,000 - $140,000', 'Remote', True)
        ]

        # Insert job opportunities into the database if they don't already exist
        for job in jobs_data:
            self.cursor.execute('''
                INSERT OR IGNORE INTO job_opportunities 
                (id, title, company, description, required_skills, salary_range, location, remote_friendly) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', job)

        self.conn.commit()
    
    def enroll_in_course(self, user_id, course_id):
        # Check if the user is already enrolled
        self.cursor.execute('''
            SELECT * FROM user_courses WHERE user_id = ? AND course_id = ?
        ''', (user_id, course_id))
        if self.cursor.fetchone():
            st.warning("You are already enrolled in this course!")
            return
        
        # Enroll the user in the course
        self.cursor.execute('''
            INSERT INTO user_courses (user_id, course_id, enrollment_date, completion_status, progress_percentage)
            VALUES (?, ?, CURRENT_TIMESTAMP, 'In Progress', 0)
        ''', (user_id, course_id))
        self.conn.commit()
        st.success("Successfully enrolled in the course!")

    def enrolled_courses(self):
        st.title("📘 Enrolled Courses")
        
        # Fetch enrolled courses for the user
        user_id = st.session_state['user_id']
        self.cursor.execute('''
            SELECT c.id, c.title, c.category, c.difficulty, uc.progress_percentage, uc.completion_status, c.duration_weeks
            FROM user_courses uc
            JOIN courses c ON uc.course_id = c.id
            WHERE uc.user_id = ?
        ''', (user_id,))
        enrolled_courses = self.cursor.fetchall()
        
        if not enrolled_courses:
            st.info("You have not enrolled in any courses yet. Explore courses to get started!")
            return
        
        # Display enrolled courses
        for course in enrolled_courses:
            course_id, title, category, difficulty, progress, status, duration = course
            with st.expander(f"{title} ({difficulty}) - {status}"):
                st.write(f"**Category:** {category}")
                st.write(f"**Duration:** {duration} weeks")
                st.write(f"**Progress:** {progress}%")
                
                if status == "In Progress":
                    if st.button(f"Learn {title}", key=f"learn_{course_id}"):
                        self.learn_course(user_id, course_id)
                    # Allow exam registration when progress is at least 20%
                    if progress >= 20 and st.button(f"Register for Exam for {title}", key=f"exam_{course_id}"):
                        self.register_for_exam(user_id, course_id)
                elif status == "Exam Registered":
                    st.success("Exam Registered! 🎉")
                elif status == "Completed":
                    st.success("Course Completed! 🎉")

    def learn_course(self, user_id, course_id):
        st.title("📖 Learn Course")
        
        # Fetch course modules
        self.cursor.execute('''
            SELECT id, title, content, video_lecture_url, assignment_details 
            FROM course_modules 
            WHERE course_id = ?
        ''', (course_id,))
        modules = self.cursor.fetchall()
        
        if not modules:
            st.info("No modules available for this course.")
            return
        
        # Display modules
        for i, module in enumerate(modules, 1):
            module_id, title, content, video_url, assignment = module
            st.subheader(f"Module {i}: {title}")
            st.write(f"**Notes:** {content}")
            if video_url:
                st.video(video_url)
            if assignment:
                st.write(f"**Assignment:** {assignment}")
                if st.button(f"Submit Assignment for {title}", key=f"submit_{module_id}"):
                    self.submit_assignment(user_id, course_id, module_id)
                    st.success(f"Assignment for '{title}' has been successfully submitted!")  # Success message
            
        # Check if all modules are completed
        self.cursor.execute('''
            SELECT COUNT(*) FROM course_modules 
            WHERE course_id = ? AND id NOT IN (
                SELECT module_id FROM user_assignments WHERE user_id = ? AND course_id = ?
            )
        ''', (course_id, user_id, course_id))
        remaining_modules = self.cursor.fetchone()[0]
        
        if remaining_modules == 0:
            st.success("All modules completed! You can now register for the exam.")
            self.update_course_progress(user_id, course_id, 20)  # Add 20% progress for completing modules
        else:
            st.info(f"{remaining_modules} module(s) remaining to complete the course.")

    def register_for_exam(self, user_id, course_id):
        st.title("📋 Exam Registration")
        
        # Check if the user is eligible for the exam
        self.cursor.execute('''
            SELECT progress_percentage FROM user_courses 
            WHERE user_id = ? AND course_id = ?
        ''', (user_id, course_id))
        progress = self.cursor.fetchone()[0]
        
        if progress < 20:  # Double-check eligibility
            st.warning("You must complete all modules and assignments to register for the exam.")
            return
        
        # Display exam guidelines
        st.subheader("📜 Exam Guidelines")
        st.write("""
        1. Ensure you have completed all modules and assignments before registering for the exam.
        2. The exam will be conducted online and monitored.
        3. Cheating or plagiarism will result in disqualification.
        4. You must complete the exam within the allotted time.
        5. Results will be announced within 7 days of exam completion.
        """)
        
        # Accept guidelines
        accept_guidelines = st.checkbox("I have read and accept the exam guidelines.")
        
        if accept_guidelines:
            if st.button("Register for Exam"):
                # Register the user for the exam without updating the progress further.
                self.cursor.execute('''
                    UPDATE user_courses 
                    SET completion_status = 'Exam Registered'
                    WHERE user_id = ? AND course_id = ?
                ''', (user_id, course_id))
                self.conn.commit()
                st.success("You have successfully registered for the exam!")
        else:
            st.info("Please accept the guidelines to proceed with exam registration.")
        
    def submit_assignment(self, user_id, course_id, module_id):
        st.info(f"Submitting assignment for User ID: {user_id}, Course ID: {course_id}, Module ID: {module_id}")
        
        # Check if the assignment is already submitted
        self.cursor.execute('''
            SELECT * FROM user_assignments 
            WHERE user_id = ? AND course_id = ? AND module_id = ?
        ''', (user_id, course_id, module_id))
        if self.cursor.fetchone():
            st.warning("You have already submitted this assignment.")
            return
        
        # Submit the assignment
        try:
            self.cursor.execute('''
                INSERT INTO user_assignments (user_id, course_id, module_id, submission_date)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, course_id, module_id))
            self.conn.commit()
            st.success(f"Assignment for module '{module_id}' submitted successfully!")
            
            # Debugging: Check remaining modules
            self.cursor.execute('''
                SELECT COUNT(*) FROM course_modules 
                WHERE course_id = ? AND id NOT IN (
                    SELECT module_id FROM user_assignments WHERE user_id = ? AND course_id = ?
                )
            ''', (course_id, user_id, course_id))
            remaining_modules = self.cursor.fetchone()[0]
            st.info(f"Remaining modules: {remaining_modules}")
            
            if remaining_modules == 0:
                st.success("All modules completed! You have earned 20% progress. You can now register for the exam.")
                self.update_course_progress(user_id, course_id, 20)  # Add 20% progress for completing modules
            else:
                st.info(f"{remaining_modules} module(s) remaining to complete the course.")
        except sqlite3.Error as e:
            st.error(f"Error submitting assignment: {e}")

    def evaluate_performance(self, user_id, course_id):
        # Mock performance evaluation logic
        performance_score = random.randint(70, 100)  # Example: Random score between 70 and 100
        
        # Assign achievements based on performance
        if performance_score >= 90:
            badge_type = "Gold"
        elif performance_score >= 75:
            badge_type = "Silver"
        else:
            badge_type = "Bronze"
        
        self.update_user_achievements(user_id, course_id, badge_type)
        st.success(f"Congratulations! You earned a {badge_type} badge for this course.")

    def search_and_filter_courses(self):
        st.title("🔍 Search and Filter Courses")
        
        # Search bar
        search_query = st.text_input("Search for a course")
        
        # Filters
        category_filter = st.selectbox("Filter by Category", ['All', 'Technology', 'Business', 'Creative', 'Personal Development'])
        difficulty_filter = st.selectbox("Filter by Difficulty", ['All', 'Beginner', 'Intermediate', 'Advanced'])
        
        # Fetch courses based on filters
        query = '''
            SELECT id, title, category, difficulty, price 
            FROM courses 
            WHERE title LIKE ? AND (category = ? OR ? = 'All') AND (difficulty = ? OR ? = 'All')
        '''
        self.cursor.execute(query, (f"%{search_query}%", category_filter, category_filter, difficulty_filter, difficulty_filter))
        courses = self.cursor.fetchall()
        
        # Display filtered courses
        for course in courses:
            course_id, title, category, difficulty, price = course
            with st.expander(f"{title} ({difficulty}) - ${price:.2f}"):
                if st.button(f"Enroll in {title}", key=course_id):
                    self.enroll_in_course(st.session_state['user_id'], course_id)
                    st.success(f"Enrolled in {title}!")

    def create_comprehensive_course_catalog(self):
        return {
            'Digital Marketing': [
                {
                    'id': 'ds001',
                    'name': 'Advanced Digital Marketing Mastery',
                    'modules': [
                        {'title': 'SEO Fundamentals', 'video_url': '', 'assignment': 'SEO Audit Project'},
                        {'title': 'Social Media Strategy', 'video_url': '', 'assignment': 'Campaign Design'}
                    ],
                    'skills_gained': ['SEO', 'Social Media Marketing', 'Analytics'],
                    'certification_potential': True
                }
            ],
            'Artificial Intelligence': [
                {
                    'id': 'ai001',
                    'name': 'Professional Machine Learning Engineer',
                    'modules': [
                        {'title': 'Python for Machine Learning', 'video_url': '', 'assignment': 'ML Model Development'},
                        {'title': 'Deep Learning Techniques', 'video_url': '', 'assignment': 'Neural Network Project'}
                    ],
                    'skills_gained': ['Machine Learning', 'Python', 'Deep Learning'],
                    'certification_potential': True
                }
            ]
        }

    def create_advanced_job_marketplace(self):
        return [
            {
                'id': 'job001',
                'title': 'Senior AI Engineer',
                'company': 'TechCorp',
                'skills_required': ['Machine Learning', 'Python', 'AI'],
                'salary_range': '$120,000 - $180,000',
                'location': 'San Francisco, CA',
                'remote': True
            }
        ]

    def create_skill_ecosystem(self):
        return {
            'Digital Marketing': {
                'entry_level_jobs': ['Social Media Coordinator', 'Digital Marketing Assistant'],
                'mid_level_jobs': ['Digital Marketing Specialist', 'SEO Strategist'],
                'advanced_jobs': ['Digital Marketing Manager', 'Head of Digital Strategy']
            },
            'Artificial Intelligence': {
                'entry_level_jobs': ['AI Research Assistant', 'Machine Learning Intern'],
                'mid_level_jobs': ['Machine Learning Engineer', 'AI Developer'],
                'advanced_jobs': ['Senior AI Scientist', 'AI Research Lead']
            }
        }

    def user_registration(self):
        st.title("Learn & Earn Pro - Registration")
        
        with st.form("registration_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            primary_skill = st.selectbox("Primary Skill Interest", 
                ['Digital Marketing', 'Artificial Intelligence', 'Web Development', 'Data Science'])
            
            submit = st.form_submit_button("Register")
            
            if submit:
                # Registration logic
                self.register_new_user(username, email, password, primary_skill)

    def register_new_user(self, username, email, password, primary_skill):
        # Implement secure registration
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            self.cursor.execute('''
                INSERT INTO users 
                (username, email, password, primary_skill, learning_credits, skill_points, total_earnings) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, hashed_password, primary_skill, 100.0, 0, 0.0))
            self.conn.commit()
            st.success("Registration Successful!")
        except sqlite3.IntegrityError:
            st.error("Username or Email already exists")

    def get_user_metrics(self, user_id):
        self.cursor.execute('''
            SELECT learning_credits, skill_points, total_earnings, 
                (SELECT COUNT(*) FROM user_courses WHERE user_id = ? AND completion_status = 'Completed') AS completed_courses,
                (SELECT COUNT(*) FROM user_courses WHERE user_id = ? AND completion_status = 'In Progress') AS in_progress_courses
            FROM users WHERE id = ?
        ''', (user_id, user_id, user_id))
        return self.cursor.fetchone()

    def course_recommendation_engine(self, user_skills):
        # AI-powered course recommendations
        recommended_courses = []
        for category, courses in self.course_catalog.items():
            for course in courses:
                # Match courses based on overlapping skills
                matching_skills = set(course['skills_gained']) & set(user_skills)
                if matching_skills:
                    recommended_courses.append(course)
        return recommended_courses

    def update_user_skills(self, user_id, skills_gained):
        for skill in skills_gained:
            # Check if the skill already exists for the user
            self.cursor.execute('''
                SELECT * FROM user_skills WHERE user_id = ? AND skill_name = ?
            ''', (user_id, skill))
            existing_skill = self.cursor.fetchone()
            
            if existing_skill:
                # Update experience points for the existing skill
                self.cursor.execute('''
                    UPDATE user_skills 
                    SET experience_points = experience_points + 10 
                    WHERE user_id = ? AND skill_name = ?
                ''', (user_id, skill))
            else:
                # Insert a new skill
                self.cursor.execute('''
                    INSERT INTO user_skills (user_id, skill_name, proficiency_level, experience_points)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, skill, 'Beginner', 10))
        
        self.conn.commit()

    def skill_progression_dashboard(self):
        st.title("Skill Progression & Recommendations")
        
        # Fetch user skills
        user_id = st.session_state['user_id']
        self.cursor.execute('''
            SELECT skill_name, experience_points 
            FROM user_skills 
            WHERE user_id = ?
        ''', (user_id,))
        skills_data = [{'Skill': row[0], 'Progress': row[1]} for row in self.cursor.fetchall()]
        
        if not skills_data:
            # No skills found - guide the user to enroll in courses
            st.info("No skills found. Explore courses to start building your skills!")
            
            # Fetch all available courses
            self.cursor.execute('SELECT id, title, category, difficulty, price FROM courses')
            courses = self.cursor.fetchall()
            
            # Display courses
            st.subheader("📚 Explore Courses")
            for course in courses:
                course_id, title, category, difficulty, price = course
                with st.expander(f"{title} ({difficulty}) - ${price:.2f}"):
                    st.write(f"Category: {category}")
                    st.write(f"Difficulty: {difficulty}")
                    st.write(f"Price: ${price:.2f}")
                    if st.button(f"Enroll in {title}", key=course_id):
                        self.enroll_in_course(user_id, course_id)
                        st.success(f"Enrolled in {title}!")
            return  # Exit the method after showing courses
        
        # If skills are found, display skill progression
        df = pd.DataFrame(skills_data)
        
        # Skill Progress Bar Chart
        fig = px.bar(df, x='Skill', y='Progress', 
                    title='Your Skill Progression',
                    labels={'Progress': 'Skill Level (%)'})
        st.plotly_chart(fig)

        # Course Recommendations Section
        st.subheader("Recommended Courses")
        
        # Fetch user's skills and recommend courses
        user_skills = [skill['Skill'] for skill in skills_data]
        recommended_courses = self.course_recommendation_engine(user_skills)
        
        if not recommended_courses:
            st.info("No course recommendations available. Try adding more skills!")
        else:
            for course in recommended_courses:
                with st.expander(course['name']):
                    st.write(f"Skills Gained: {', '.join(course['skills_gained'])}")
                    if st.button(f"Enroll in {course['name']}", key=course['id']):
                        self.enroll_in_course(user_id, course['id'])
                        st.success(f"Enrolled in {course['name']}!")

    def job_matching_system(self):
        st.title("Job Matching & Opportunities")
        
        # Fetch user badges
        user_id = st.session_state['user_id']
        self.cursor.execute('''
            SELECT skill_name FROM user_skills WHERE user_id = ?
        ''', (user_id,))
        user_badges = [row[0] for row in self.cursor.fetchall()]

        # Filter jobs based on badges
        matching_jobs = []
        for job in self.job_marketplace:
            if any(badge.split(' ')[0] in job['skills_required'] for badge in user_badges):
                matching_jobs.append(job)
        
        st.subheader("Recommended Jobs")
        for job in matching_jobs:
            with st.expander(job['title']):
                st.write(f"Company: {job.get('company', 'N/A')}")
                st.write(f"Skills Required: {', '.join(job['skills_required'])}")
                st.write(f"Salary Range: {job['salary_range']}")
                
                if st.button(f"Apply to {job['title']}"):
                    st.success(f"Application for {job['title']} submitted!")
    
    def get_upcoming_deadlines(self, user_id):
        # Fetch deadlines for enrolled courses
        self.cursor.execute('''
            SELECT c.title AS Task, uc.enrollment_date + c.duration_weeks * 7 AS DueDate
            FROM user_courses uc
            JOIN courses c ON uc.course_id = c.id
            WHERE uc.user_id = ? AND uc.completion_status = 'In Progress'
        ''', (user_id,))
        course_deadlines = [{'Task': row[0], 'DueDate': row[1]} for row in self.cursor.fetchall()]

        # Fetch deadlines for job applications
        self.cursor.execute('''
            SELECT j.title AS Task, uja.application_date + 7 AS DueDate
            FROM user_job_applications uja
            JOIN job_opportunities j ON uja.job_id = j.id
            WHERE uja.user_id = ? AND uja.status = 'Pending'
        ''', (user_id,))
        job_deadlines = [{'Task': row[0], 'DueDate': row[1]} for row in self.cursor.fetchall()]

        # Combine all deadlines
        deadlines = course_deadlines + job_deadlines
        return deadlines

    def display_deadline_graph(self, deadlines):
        if not deadlines:
            st.info("No upcoming deadlines. You're all caught up!")
            return

        # Convert deadlines to a DataFrame
        df = pd.DataFrame(deadlines)
        df['DueDate'] = pd.to_datetime(df['DueDate']).dt.floor('s')  # Remove nanoseconds

        # Create a bar chart for deadlines
        fig = px.bar(
            df,
            x='DueDate',
            y='Task',
            title="Upcoming Deadlines",
            labels={'DueDate': 'Deadline', 'Task': 'Task'},
            color='DueDate',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig, use_container_width=True)

    def get_notifications(self, user_id):
        notifications = []

        # Fetch upcoming deadlines
        deadlines = self.get_upcoming_deadlines(user_id)
        for deadline in deadlines:
            days_left = (pd.to_datetime(deadline['DueDate']) - pd.Timestamp.now()).days
            if days_left <= 3:  # Notify if the deadline is within 3 days
                notifications.append(f"⏳ Reminder: '{deadline['Task']}' is due in {days_left} days!")

        # Add other notifications (e.g., achievements, job opportunities)
        notifications.append("🎉 You earned 50 skill points for completing a module!")
        notifications.append("💼 New job opportunity: Senior AI Engineer at TechCorp")

        return notifications

    def interactive_learning_path(self):
        st.title("🛤️ Interactive Learning Path")
        
        # Define the learning stages
        learning_stages = [
            {"stage": "Skill Assessment", "description": "Evaluate your current skills and identify areas for improvement."},
            {"stage": "Course Selection", "description": "Choose courses that align with your goals."},
            {"stage": "Learning Modules", "description": "Complete modules to gain knowledge and skills."},
            {"stage": "Skill Practice", "description": "Apply your skills through projects and assignments."},
            {"stage": "Certification", "description": "Earn certifications to showcase your expertise."},
            {"stage": "Job Placement", "description": "Leverage your skills to secure job opportunities."}
        ]
        
        # Fetch user progress dynamically (replace with actual database logic)
        user_id = st.session_state['user_id']
        self.cursor.execute('''
            SELECT COUNT(*) FROM user_courses 
            WHERE user_id = ? AND completion_status = 'Completed'
        ''', (user_id,))
        user_progress = self.cursor.fetchone()[0]  # Number of completed stages

        # Display the learning path
        for i, stage in enumerate(learning_stages, 1):
            if i <= user_progress:
                st.markdown(f"✅ **{i}. {stage['stage']}** - {stage['description']}")
            else:
                st.markdown(f"🔲 **{i}. {stage['stage']}** - {stage['description']}")
            
            # Add a clickable button for each stage
            if st.button(f"Go to {stage['stage']}", key=f"stage_{i}"):
                st.info(f"Navigating to {stage['stage']}... (Implement navigation logic here)")
            
            # Add a visual separator between stages
            if i < len(learning_stages):
                st.markdown("↓")

    def main_dashboard(self):
        # Dashboard Title
        st.title("🌟 Learn & Earn Pro Dashboard 🚀")
        
        # Notification Icon at the Top
        with st.container():
            col1, col2 = st.columns([9, 1])  # Adjust column widths
            with col1:
                st.markdown("---")  # Add a horizontal line for better separation
            with col2:
                if st.button("🔔"):  # Notification button
                    st.session_state['show_notifications'] = not st.session_state.get('show_notifications', False)
        
        # Show Notifications if the button is clicked
        if st.session_state.get('show_notifications', False):
            st.subheader("🔔 Notifications")
            notifications = [
                "New job opportunity: Senior AI Engineer at TechCorp",
                "You earned 50 skill points for completing a module!",
                "Upcoming deadline: Complete 'Social Media Strategy' by March 30."
            ]
            for notification in notifications:
                st.write(f"✅ {notification}")
            st.markdown("---")  # Add a horizontal line for better separation

        # Fetch user metrics
        user_id = st.session_state['user_id']
        metrics = self.get_user_metrics(user_id)
        learning_credits, skill_points, total_earnings, completed_courses, in_progress_courses = metrics

        # Key Metrics Section
        st.subheader("📊 Key Metrics")
        with st.container():
            col1, col2, col3 = st.columns(3, gap="large")
            with col1:
                st.metric("Completed Courses", completed_courses)
                st.metric("Skill Points", skill_points)
            with col2:
                st.metric("In Progress Courses", in_progress_courses)
                st.metric("Learning Credits", learning_credits)
            with col3:
                st.metric("Total Earnings", f"${total_earnings:.2f}")
                st.metric("Potential Job Matches", 5)  # Example static value

        st.markdown("---")  # Add a horizontal line for better separation

        # Real-Time Progress Tracking Section
        st.subheader("📈 Real-Time Progress Tracking")
        progress_data = self.get_course_progress(user_id)
        progress_df = pd.DataFrame(progress_data, columns=['Course', 'Progress'])

        if progress_df.empty:
            st.info("No course progress data available. Enroll in a course to start tracking your progress!")
        else:
            progress_chart = px.bar(
                progress_df,
                x='Course',
                y='Progress',
                title="Course Progress",
                labels={'Progress': 'Completion (%)'},
                color='Progress',
                color_continuous_scale=px.colors.sequential.Viridis
            )
            st.plotly_chart(progress_chart, use_container_width=True)

        st.markdown("---")  # Add a horizontal line for better separation

        # Achievements Section
        st.subheader("🏅 Your Achievements")
        self.cursor.execute('''
            SELECT skill_name, proficiency_level FROM user_skills WHERE user_id = ?
        ''', (user_id,))
        badges = self.cursor.fetchall()

        if badges:
            with st.container():
                cols = st.columns(len(badges))
                for i, (badge_name, badge_type) in enumerate(badges):
                    with cols[i]:
                        st.markdown(f"🏆 **{badge_name}** ({badge_type})")
        else:
            st.info("No achievements yet. Complete courses to earn badges!")

        # Leaderboard Section
        st.subheader("📋 Leaderboard")
        leaderboard_data = [
            {'Rank': 1, 'Username': 'pro_learner', 'Skill Points': 1200},
            {'Rank': 2, 'Username': 'ai_master', 'Skill Points': 1100},
            {'Rank': 3, 'Username': 'web_dev', 'Skill Points': 950}
        ]
        leaderboard_df = pd.DataFrame(leaderboard_data)
        st.table(leaderboard_df)

        st.markdown("---")  # Add a horizontal line for better separation

        # Personalized Recommendations Section
        st.subheader("🎯 Personalized Recommendations")
        recommended_courses = self.course_recommendation_engine(['Digital Marketing', 'SEO'])
        for course in recommended_courses:
            with st.expander(course['name']):
                st.write(f"Skills Gained: {', '.join(course['skills_gained'])}")
                if st.button(f"Enroll in {course['name']}"):
                    st.success(f"Enrolled in {course['name']}!")

        st.markdown("---")  # Add a horizontal line for better separation

        # Upcoming Deadlines Section
        st.subheader("⏳ Upcoming Deadlines")
        deadlines = self.get_upcoming_deadlines(user_id)
        self.display_deadline_graph(deadlines)

        st.markdown("---")  # Add a horizontal line for better separation

        # Interactive Learning Path Section
        st.subheader("🛤️ Interactive Learning Path")
        learning_stages = [
            "Skill Assessment",
            "Course Selection",
            "Learning Modules",
            "Skill Practice",
            "Certification",
            "Job Placement"
        ]
        for i, stage in enumerate(learning_stages, 1):
            st.markdown(f"{i}. **{stage}**")
            if i < len(learning_stages):
                st.markdown("↓")
    
    def update_user_metrics(self, user_id, skill_points=0, earnings=0.0, course_id=None):
        # Update skill points and earnings
        self.cursor.execute('''
            UPDATE users 
            SET skill_points = skill_points + ?, 
                total_earnings = total_earnings + ?
            WHERE id = ?
        ''', (skill_points, earnings, user_id))
        
        # Mark course as completed if course_id is provided
        if course_id:
            self.cursor.execute('''
                UPDATE user_courses 
                SET completion_status = 'Completed', progress_percentage = 100, completed_date = CURRENT_TIMESTAMP
                WHERE user_id = ? AND course_id = ?
            ''', (user_id, course_id))

            # Assign badge based on course difficulty
            self.cursor.execute('SELECT difficulty FROM courses WHERE id = ?', (course_id,))
            course_difficulty = self.cursor.fetchone()[0]
            badge_type = 'Gold' if course_difficulty == 'Advanced' else 'Silver' if course_difficulty == 'Intermediate' else 'Bronze'
            self.update_user_achievements(user_id, course_id, badge_type)

        self.conn.commit()
    
    def update_user_achievements(self, user_id, course_id, badge_type):
        # Define earnings based on badge type
        badge_earnings = {
            'Gold': 500,
            'Silver': 300,
            'Bronze': 100
        }
        earnings = badge_earnings.get(badge_type, 0)

        # Update user earnings and assign badge
        self.cursor.execute('''
            UPDATE users 
            SET total_earnings = total_earnings + ?
            WHERE id = ?
        ''', (earnings, user_id))

        # Insert badge into achievements table
        self.cursor.execute('''
            INSERT INTO user_skills (user_id, skill_name, proficiency_level, experience_points)
            VALUES (?, ?, ?, ?)
        ''', (user_id, f"{badge_type} Badge for {course_id}", badge_type, earnings))

        self.conn.commit()

    def get_course_progress(self, user_id):
        self.cursor.execute('''
            SELECT c.title AS Course, uc.progress_percentage AS Progress
            FROM user_courses uc
            JOIN courses c ON uc.course_id = c.id
            WHERE uc.user_id = ?
        ''', (user_id,))
        result = self.cursor.fetchall()
        if not result:
            return []  # Return an empty list if no data is found
        return result
    
    def update_course_progress(self, user_id, course_id, progress_increment):
        # Fetch current progress and status
        self.cursor.execute('''
            SELECT progress_percentage, completion_status FROM user_courses 
            WHERE user_id = ? AND course_id = ?
        ''', (user_id, course_id))
        row = self.cursor.fetchone()
        current_progress = row[0]
        current_status = row[1]
        
        # Update progress
        new_progress = min(current_progress + progress_increment, 100)  # Cap progress at 100%
        if current_status == "Exam Registered":
            new_status = "Exam Registered"
        else:
            new_status = 'Completed' if new_progress == 100 else 'In Progress'
        
        self.cursor.execute('''
            UPDATE user_courses 
            SET progress_percentage = ?, completion_status = ?
            WHERE user_id = ? AND course_id = ?
        ''', (new_progress, new_status, user_id, course_id))
        self.conn.commit()
        st.success(f"Progress updated to {new_progress}%!")

    def ai_based_job_matching(self):
        st.title("🤖 AI-Based Job Matching")
        
        # Input space for uploading skills
        uploaded_file = st.file_uploader("Upload your skills file (JSON format)", type=["json"])
        
        if uploaded_file:
            try:
                # Parse uploaded JSON file
                skills_data = json.load(uploaded_file)
                uploaded_skills = skills_data.get("skills", [])
                
                if not uploaded_skills:
                    st.warning("No skills found in the uploaded file. Please ensure the file contains a 'skills' key.")
                    return
                
                st.success(f"Skills uploaded successfully: {', '.join(uploaded_skills)}")
                
                # AI-based job matching
                st.subheader("🔍 Matching Jobs")
                matching_jobs = self.get_ai_matched_jobs(uploaded_skills)
                
                if not matching_jobs:
                    st.info("No matching jobs found for the uploaded skills.")
                else:
                    for job in matching_jobs:
                        with st.expander(job['title']):
                            st.write(f"**Company:** {job['company']}")
                            st.write(f"**Skills Required:** {', '.join(job['skills_required'])}")
                            st.write(f"**Salary Range:** {job['salary_range']}")
                            st.write(f"**Location:** {job['location']}")
                            st.write(f"**Remote Friendly:** {'Yes' if job['remote'] else 'No'}")
                            if st.button(f"Apply to {job['title']}", key=f"apply_{job['id']}"):
                                self.apply_to_job(st.session_state['user_id'], job['id'])
                                st.success(f"Application for '{job['title']}' submitted!")
            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload a valid JSON file containing your skills.")

    def get_ai_matched_jobs(self, uploaded_skills):
        # AI-based matching logic
        matched_jobs = []
        for job in self.job_marketplace:
            # Match jobs based on overlapping skills
            matching_skills = set(uploaded_skills) & set(job['skills_required'])
            if matching_skills:
                matched_jobs.append(job)
        return matched_jobs

    def apply_to_job(self, user_id, job_id):
        # Insert job application into the database
        try:
            self.cursor.execute('''
                INSERT INTO user_job_applications (user_id, job_id, application_date, status)
                VALUES (?, ?, CURRENT_TIMESTAMP, 'Pending')
            ''', (user_id, job_id))
            self.conn.commit()
        except sqlite3.IntegrityError:
            st.warning("You have already applied for this job.")

    def ai_interview_preparation(self):
        st.title("🤖 AI-Based Interview Preparation")
        
        # Introduction
        st.write("Prepare for your interviews with AI-powered assistance. Ask questions or simulate an interview session!")
        
        # Input for user question
        user_question = st.text_input("Ask a question or start a mock interview:")
        
        if user_question:
            # Generate AI response
            try:
                # Ensure the AI service is properly configured
                if not hasattr(genai, 'generate_text'):
                    raise RuntimeError("AI service is not configured correctly.")
                
                ai_response = genai.generate_text(prompt=user_question, max_output_tokens=200)
                if ai_response and hasattr(ai_response, 'text'):
                    st.subheader("AI Response:")
                    st.write(ai_response.text.strip())
                else:
                    raise RuntimeError("AI service returned an invalid response.")
            except Exception as e:
                st.error("AI is currently unavailable. Please try again later.")
                st.info("Fallback Response: Practice answering common interview questions like 'Tell me about yourself' or 'What are your strengths and weaknesses?'")
        
        # Example questions for guidance
        st.subheader("Example Questions:")
        st.write("- What are the key skills required for a Data Scientist role?")
        st.write("- How should I answer the question: 'Tell me about yourself'?")
        st.write("- Can you simulate a mock interview for a Software Engineer position?")

    def get_ai_response(self, question):
        # Mock AI response logic (replace with actual AI API integration)
        # Example using Google Generative AI or any other AI service
        try:
            response = genai.generate_text(prompt=question, max_output_tokens=200)
            return response.text.strip()
        except Exception as e:
            raise RuntimeError("Failed to fetch AI response") from e

    def run(self):
        st.set_page_config(page_title="Learn & Earn Pro", page_icon="🚀", layout="wide")
        
        # Ensure session state variables are initialized
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False
        if 'user_id' not in st.session_state:
            st.session_state['user_id'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 'Login'

        # Navigation logic based on session state
        if not st.session_state['logged_in']:
            st.title("Welcome to Learn & Earn Pro")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Register", key="register_button"):
                    st.session_state['current_page'] = 'Register'
            with col2:
                if st.button("Login", key="login_button"):
                    st.session_state['current_page'] = 'Login'

            # Render the appropriate page
            if st.session_state['current_page'] == 'Register':
                self.user_registration()
            elif st.session_state['current_page'] == 'Login':
                self.login_page()
        else:
            # If logged in, show the full menu
            menu = ["Dashboard", "Courses", "Enrolled Courses", "Jobs", "AI Job Matching", "AI Interview Preparation", "Profile", "Logout"]
            choice = st.sidebar.selectbox("Navigation", menu)
            
            if choice == "Dashboard":
                self.main_dashboard()
            elif choice == "Courses":
                self.skill_progression_dashboard()
            elif choice == "Enrolled Courses":
                self.enrolled_courses()
            elif choice == "Jobs":
                self.job_matching_system()
            elif choice == "AI Job Matching":
                self.ai_based_job_matching()
            elif choice == "AI Interview Preparation":
                self.ai_interview_preparation()
            elif choice == "Profile":
                self.user_profile()
            elif choice == "Logout":
                # Logout logic
                st.session_state['logged_in'] = False
                st.session_state['user_id'] = None
                st.session_state['username'] = None
                st.session_state['current_page'] = 'Login'
                st.success("You have been logged out.")

    def login_page(self):
        st.title("Login to Learn & Earn Pro")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Implement login logic
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            self.cursor.execute('''
                SELECT id, username FROM users 
                WHERE username = ? AND password = ?
            ''', (username, hashed_password))
            
            user = self.cursor.fetchone()
            
            if user:
                st.success("Login Successful!")
                # Set session state variables
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user[0]
                st.session_state['username'] = user[1]
                st.session_state['current_page'] = 'Dashboard'
                
                # Rerun the app to navigate to the dashboard
                st.rerun()
            else:
                st.error("Invalid Credentials")

    def user_profile(self):
        st.title("User Profile")
        
        # Profile Information
        st.subheader("Personal Details")
        
        # Mock data - replace with actual user data retrieval
        profile_data = {
            'Username': 'learner123',
            'Email': 'learner@example.com',
            'Primary Skill': 'Digital Marketing',
            'Total Skill Points': 750,
            'Subscription Tier': 'Pro'
        }
        
        for key, value in profile_data.items():
            st.write(f"**{key}:** {value}")
        
        # Skill Badges
        st.subheader("Skill Badges")
        badges = ['Digital Marketing Fundamentals', 'SEO Certified', 'Social Media Marketing']
        
        cols = st.columns(len(badges))
        for i, badge in enumerate(badges):
            with cols[i]:
                st.markdown(f"🏅 {badge}")

if __name__ == "__main__":
    platform = AdvancedLearnAndEarnPlatform()
    platform.run()
