@echo off
cd ..
pytest test_login.py --headed

allure generate ../reports/allure-results --clean --single-file -o ../reports/allure-report
