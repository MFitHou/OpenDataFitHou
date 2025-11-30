# Contributing to OpenDataFitHou

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/OpenDataFitHou.git
   cd OpenDataFitHou
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Code Style

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

## Project Structure

Please follow the established project structure:
- Place new source code in appropriate `src/` subdirectories
- Add tests in `tests/` directory
- Update documentation as needed

## Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Ensure all tests pass

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   Use conventional commit messages:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

4. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Testing

Run tests before submitting:
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_specific.py
```

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions and classes
- Update docs/ if changing architecture
- Add examples to notebooks/ for complex features

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update documentation as needed
3. Add tests for new functionality
4. Ensure all tests pass
5. Create a pull request with a clear description

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the code
- Documentation improvements

Thank you for contributing!
