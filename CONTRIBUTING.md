# Contributing to Image Converter and Resizer

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Setting Up Development Environment

1. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/image-converter-resizer.git
   cd image-converter-resizer
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies:**
   ```bash
   poetry install --with dev
   ```

4. **Install pre-commit hooks:**
   ```bash
   poetry run pre-commit install
   ```

5. **Create a branch for your feature:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting  
- **flake8** for linting
- **mypy** for type checking

Run these before committing:

```bash
# Format code
poetry run black src/
poetry run isort src/

# Check linting
poetry run flake8 src/

# Type checking
poetry run mypy src/

# Run tests
poetry run pytest
```

## Code Quality Guidelines

### Python Code Style

- Follow PEP 8 style guidelines (enforced by Black)
- Use type hints for all function parameters and return values
- Write descriptive docstrings for all classes and functions
- Keep functions small and focused on a single responsibility
- Use meaningful variable and function names

### Example of Good Code Style

```python
def calculate_new_dimensions(
    width: int, height: int, max_resolution: int
) -> Tuple[int, int]:
    """Calculate new dimensions while maintaining aspect ratio.
    
    Args:
        width: Original image width in pixels
        height: Original image height in pixels
        max_resolution: Maximum allowed dimension
        
    Returns:
        Tuple of (new_width, new_height) as integers
        
    Raises:
        ValueError: If any dimension is negative or zero
    """
    if width <= 0 or height <= 0 or max_resolution <= 0:
        raise ValueError("Dimensions must be positive integers")
        
    # Calculate maintaining aspect ratio
    if width > height:
        new_width = min(width, max_resolution)
        new_height = int(height * (new_width / width))
    else:
        new_height = min(height, max_resolution)
        new_width = int(width * (new_height / height))
    
    return new_width, new_height
```

## Testing Guidelines

- Write unit tests for new functionality
- Maintain or improve test coverage
- Test edge cases and error conditions
- Use descriptive test names

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test file
poetry run pytest tests/test_image_processor.py
```

## Commit Message Guidelines

We follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

**Examples:**
```
feat(processor): add support for WebP format
fix(ui): resolve progress bar not updating correctly
docs(readme): update installation instructions
```

## Issue Reporting

When creating an issue, please provide:

1. **Bug Reports:**
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Error logs/screenshots if applicable

2. **Feature Requests:**
   - Clear description of the desired functionality
   - Use case or problem it solves
   - Possible implementation approach (if you have ideas)

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## Getting Help

- Check existing [issues](https://github.com/jbone3311/image-converter-resizer/issues)
- Create a new issue with the "question" label
- Join discussions in existing issues and pull requests

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in our README.md file and release notes.

Thank you for contributing! 🎉