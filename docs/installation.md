# Installation Guide

## Prerequisites

- Python 3.10 or higher
- Git

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/magicskills/magic-skills.git
cd magic-skills
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e ".[dev]"
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Verify Installation

```bash
magic-skill --version
```

## Configuration

### API Keys

Set your LLM API keys in `.env`:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

### Default Model

Change default model in `.env`:

```bash
MAGIC_SKILLS_DEFAULT_PROVIDER=openai
MAGIC_SKILLS_DEFAULT_MODEL=gpt-4o-mini
```

## Troubleshooting

### Import Errors

If you see import errors, ensure you're in the virtual environment:

```bash
source venv/bin/activate
```

### API Key Errors

Verify your API keys are set correctly:

```bash
echo $OPENAI_API_KEY
```

### Permission Errors

On Linux/Mac, you may need to make scripts executable:

```bash
chmod +x venv/bin/magic-skill
```
