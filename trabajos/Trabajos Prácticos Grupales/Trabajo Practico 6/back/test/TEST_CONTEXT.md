---
applyTo: '**'
---
Provide project context and coding guidelines that AI should follow when generating code, answering questions, or reviewing changes.



# Project Context
This project is a FastAPI application that manages ticket purchases for an event. It includes features such as visitor age validation, payment method handling, and token validation for security. The application uses Pydantic models for data validation and FastAPI's dependency injection for managing unique purchase IDs.
# Coding Guidelines
- Use FastAPI and Pydantic for building APIs and data validation.
- Ensure all data models are well-defined with appropriate validation methods.
- Follow RESTful principles for API design.
- Write clear and concise docstrings for all functions and classes.
- Include error handling for invalid inputs and edge cases.

# Testing Guidelines
- Use pytest for writing and running tests.
- Write unit tests for individual functions and classes.
- Every test should be independent and not rely on the state of other tests.
- Every test should follow the followed structure:
  - Setup: Prepare the environment, inputs and preconditions.
  - Execution: Call the function or method being tested.
  - Assertion: Verify that the output matches the expected result and a comment in case the assertion fails.
- Every test should have a docstring explaining its purpose.