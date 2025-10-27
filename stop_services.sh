#!/bin/bash

# Stop Services Script for EC2

echo "Stopping E-commerce Services..."

# Colors for output
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Kill backend
echo -e "${YELLOW}Stopping backend...${NC}"
pkill -f "python main.py" || echo -e "${RED}Backend not running${NC}"
sleep 2

# Kill frontend
echo -e "${YELLOW}Stopping frontend...${NC}"
pkill -f "npm run dev" || echo -e "${RED}Frontend (npm) not running${NC}"
pkill -f "vite" || echo -e "${RED}Frontend (vite) not running${NC}"
sleep 2

echo -e "${GREEN}All services stopped${NC}"

