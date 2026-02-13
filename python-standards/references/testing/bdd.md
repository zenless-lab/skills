# Behavior Driven Development (BDD)

## Core Philosophy
Tests are written in plain English (Gherkin syntax) to facilitate collaboration between developers and non-technical stakeholders (The "Three Amigos").

## Tools
* **Behave**: The most common Python BDD framework.
* **pytest-bdd**: Integrates Gherkin with pytest fixtures.

## Structure
1.  **Feature File** (`features/login.feature`):
    ```gherkin
    Feature: User Login
      Scenario: Successful login
        Given a user exists with password "secure"
        When the user logs in with password "secure"
        Then the login should be successful
    ```

2.  **Step Definition** (`features/steps/login_steps.py`):
    ```python
    from behave import given, when, then

    @given('a user exists with password "{pwd}"')
    def step_impl(context, pwd):
        context.user = create_user(password=pwd)

    @when('the user logs in with password "{pwd}"')
    def step_impl(context, pwd):
        context.response = context.client.login(pwd)

    @then('the login should be successful')
    def step_impl(context):
        assert context.response.status_code == 200
    ```
