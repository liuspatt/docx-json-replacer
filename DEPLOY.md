# Deployment Instructions for PyPI

## Prerequisites

1. **PyPI Account**: Create accounts at:
   - Production: https://pypi.org/account/register/
   - Test: https://test.pypi.org/account/register/

2. **API Tokens**: Generate API tokens for both environments:
   - Go to Account Settings → API tokens
   - Create a token with "Entire account" scope
   - Save tokens securely

3. **Install Build Tools**:
   ```bash
   # In a virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install --upgrade pip build twine
   ```

## Pre-deployment Checklist

- [ ] Version updated in `docx_json_replacer/__init__.py`
- [ ] Version updated in `pyproject.toml`
- [ ] CHANGELOG.md updated with version notes
- [ ] README.md updated with new features
- [ ] All tests pass locally
- [ ] Git repository is clean (all changes committed)
- [ ] Previous version is tagged in git

## Build the Package

1. **Clean previous builds**:
   ```bash
   rm -rf build/ dist/ *.egg-info
   ```

2. **Build the distribution**:
   ```bash
   python3 -m build
   ```

   This creates:
   - `dist/docx-json-replacer-0.7.0.tar.gz` (source distribution)
   - `dist/docx_json_replacer-0.7.0-py3-none-any.whl` (wheel)

3. **Verify the build**:
   ```bash
   ls -la dist/
   # Check file sizes are reasonable (should be ~20-50 KB)
   ```

## Test on TestPyPI (Recommended)

1. **Upload to TestPyPI**:
   ```bash
   python3 -m twine upload --repository testpypi dist/*
   ```

   When prompted, use:
   - Username: `__token__`
   - Password: Your TestPyPI API token

2. **Test installation from TestPyPI**:
   ```bash
   # In a new virtual environment
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ docx-json-replacer==0.7.0
   ```

3. **Verify the package works**:
   ```python
   from docx_json_replacer import DocxReplacer
   print(DocxReplacer.__module__)
   ```

## Deploy to Production PyPI

1. **Final verification**:
   ```bash
   # Check the distribution contents
   tar -tzf dist/docx-json-replacer-0.7.0.tar.gz | head -20
   ```

2. **Upload to PyPI**:
   ```bash
   python3 -m twine upload dist/*
   ```

   When prompted, use:
   - Username: `__token__`
   - Password: Your PyPI API token

3. **Verify on PyPI**:
   - Visit: https://pypi.org/project/docx-json-replacer/0.7.0/
   - Check that all metadata displays correctly
   - Verify README renders properly

## Post-deployment

1. **Test production installation**:
   ```bash
   # In a clean virtual environment
   pip install docx-json-replacer==0.7.0
   python3 -c "from docx_json_replacer import DocxReplacer; print('Success!')"
   ```

2. **Tag the release in Git**:
   ```bash
   git tag -a v0.7.0 -m "Release version 0.7.0"
   git push origin v0.7.0
   ```

3. **Create GitHub Release** (if using GitHub):
   - Go to https://github.com/liuspatt/docx-json-replacer/releases
   - Click "Create a new release"
   - Choose tag `v0.7.0`
   - Title: "v0.7.0 - Formatting Preservation & Cell Padding"
   - Copy release notes from CHANGELOG.md
   - Attach the distribution files from `dist/`

## Using a .pypirc File (Optional)

Create `~/.pypirc` for easier uploads:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TEST-TOKEN-HERE
```

Then you can upload with:
```bash
# TestPyPI
python3 -m twine upload --repository testpypi dist/*

# Production PyPI
python3 -m twine upload --repository pypi dist/*
```

## Troubleshooting

### Common Issues:

1. **"Invalid distribution file"**: Rebuild with `python3 -m build`
2. **"Version already exists"**: Increment version number
3. **"Invalid credentials"**: Check API token and use `__token__` as username
4. **"Missing required metadata"**: Check setup.py/pyproject.toml

### Verification Commands:

```bash
# Check package metadata
python3 -m twine check dist/*

# View package contents
tar -tzf dist/docx-json-replacer-0.7.0.tar.gz

# Test import locally
python3 -c "import sys; sys.path.insert(0, 'dist/docx_json_replacer-0.7.0-py3-none-any.whl'); from docx_json_replacer import DocxReplacer"
```

## Version Management

For future releases:
1. Update version in `__init__.py` and `pyproject.toml`
2. Update CHANGELOG.md
3. Update README.md if needed
4. Follow this deployment process
5. Consider semantic versioning:
   - MAJOR.MINOR.PATCH
   - MAJOR: Breaking changes
   - MINOR: New features (backward compatible)
   - PATCH: Bug fixes

## Security Notes

- Never commit API tokens to version control
- Use environment variables for CI/CD:
  ```bash
  export TWINE_USERNAME=__token__
  export TWINE_PASSWORD=your-token-here
  python3 -m twine upload dist/*
  ```
- Rotate tokens periodically
- Use project-specific tokens when possible