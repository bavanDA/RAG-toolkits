#!/bin/bash
set -e  # exit if any command fails

# 1. Create venv if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Activate venv
source venv/bin/activate

# 3. Upgrade pip (optional but recommended)
pip install --upgrade pip

# 4. Install dependencies (if requirements.txt exists)
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping dependency install."
fi

# 5. Run main.py
echo "Starting main.py..."
python main.py
