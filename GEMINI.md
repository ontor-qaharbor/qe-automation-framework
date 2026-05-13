dev-1/
├── features/
│   ├── web/
│   │   └── login_to_cart.feature
│   └── api/
├── src/
│   ├── businessfunctions/
│   │   ├── __init__.py
│   │   └── saucedemo.py
│   ├── corecomponents/
│   │   ├── __init__.py
│   │   ├── base_page.py
│   │   ├── constants.py
│   │   ├── xls_reader.py
│   │   └── xml_reader.py
│   ├── pageobjects/
│   │   ├── __init__.py
│   │   └── saucedemo_locators.py
│   ├── projectconfig/
│   │   └── project_config.py
│   ├── runner/
│   │   ├── __init__.py
│   │   └── conftest.py
│   ├── stepdefinitions/              ← ADD THIS
│   │   ├── __init__.py
│   │   └── test_saucedemo_steps.py
│   ├── testcasedriver/
│   │   ├── __init__.py
│   │   └── test_case_driver.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_bdd_login_to_cart.py
├── data/
│   └── Test_Data.xlsx
├── reports/
├── resources/
│   ├── apps/
│   ├── features/
│   └── TestCaseMappingFiles/
├── tools/
│   └── create_test_data_xlsx.py

├── requirements.txt
└── pytest.ini


Read my project completely first.

Make these two changes only:

1. Create src/stepdefinitions/ folder
   Add __init__.py inside it
   Move test_saucedemo_steps.py from
   src/tests/step_defs/ to src/stepdefinitions/

2. Create these folders inside resources/:
   resources/apps/
   resources/features/
   resources/TestCaseMappingFiles/

3. Update all imports in any file that
   imported from src/tests/step_defs/
   to now import from src/stepdefinitions/

4. Update pytest.ini if needed to find
   step definitions in new location

5. Delete src/tests/step_defs/ after move

Do not touch any other file.
Show me the plan first.
Wait for GO AHEAD before applying.