@echo off
cd ..
pytest test_login.py test_demo_site.py -n 2

allure generate ../reports/allure-results --clean --single-file -o ../reports/allure-report
