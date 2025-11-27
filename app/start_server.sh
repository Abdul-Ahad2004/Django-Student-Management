#!/bin/bash

# Script to wait for database and then run Django development server

echo "Starting Django application with database check..."

# Wait for database to be ready
echo "Checking database connection..."
python manage.py wait_for_db --timeout=60

# Check if database wait was successful
if [ $? -eq 0 ]; then
    # echo "Database is ready. Running migrations..."
    # python manage.py migrate
    
    # if [ $? -eq 0 ]; then
    echo "Starting development server..."
    python manage.py runserver 0.0.0.0:8001
    # else
    #     echo "Migrations failed!"
    #     exit 1
    # fi
else
    echo "Database connection failed!"
    exit 1
fi
