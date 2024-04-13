import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    create_db()
    yield
    os.remove('users.db')

def test_create_db(setup_database):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Проверяем, существует ли таблица users
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists

def test_add_new_user(setup_database):
    add_user('adduser', 'adduser@gmail.com', 'password123')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='adduser';")
    user = cursor.fetchone()
    assert user

def test_add_existing_user(setup_database):
    add_user('adduser', 'adduser@email.com', 'password123')
    assert not add_user('adduser', 'newuser@email.com', 'newpassword456')

def test_authenticate_user_success(setup_database):
    add_user('testuser', 'adduser@email.com', 'password123')
    assert authenticate_user('adduser', 'password123')

def test_authenticate_user_not_found(setup_database):
    assert not authenticate_user('unknownuser', 'password123')

def test_authenticate_user_wrong_password(setup_database):
    add_user('adduser', 'adduser@gmail.com', 'password123')
    assert not authenticate_user('adduser', 'wrongpassword')

# Фикстура для создания и удаления базы данных
@pytest.fixture(scope="module")
def setup_database():
    create_db()
    connection = sqlite3.connect('users.db')
    yield connection
    connection.close()




