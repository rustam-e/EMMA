#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
else
    echo -e "${YELLOW}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install or upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${YELLOW}Installing requirements...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}Setup complete. Virtual environment is activated.${NC}"
echo -e "${YELLOW}To deactivate, run 'deactivate'${NC}"

# Optionally, you can add your OpenAI API key to the virtual environment
read -p "Do you want to set up your OpenAI API key? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    read -p "Enter your OpenAI API key: " apikey
    echo "export OPENAI_API_KEY='$apikey'" >> venv/bin/activate
    echo -e "${GREEN}OpenAI API key has been added to the virtual environment.${NC}"
    echo -e "${YELLOW}To apply the changes, deactivate and reactivate the virtual environment.${NC}"
fi