#!/bin/bash

# Change directory to the parent directory
echo "Navigating to the parent directory..."
cd ..

# Run tests with pytest, using 2 parallel processes
echo "Running pytest tests..."
pytest test_login.py

# Generate the Allure report from the test results
echo "Generating Allure report..."
allure generate /app/reports/allure-results --clean --single-file -o /app/reports/allure-report

