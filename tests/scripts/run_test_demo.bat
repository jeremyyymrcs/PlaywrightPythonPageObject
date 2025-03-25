@echo off
cd ..
pytest test_demo_site.py --headed

allure generate ../reports/allure-results --clean --single-file -o ../reports/allure-report
