#!/bin/bash

# Change directory to the parent directory
echo "Navigating to the parent directory..."
cd ..

# Run tests with pytest, using 2 parallel processes
echo "Running pytest tests..."
pytest test_login.py test_demo_site.py -n 2

# Generate the Allure report from the test results
echo "Generating Allure report..."
allure generate ../reports/allure-results --clean --single-file -o ../reports/allure-report
