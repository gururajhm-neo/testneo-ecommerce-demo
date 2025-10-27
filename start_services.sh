#!/bin/bash

# Start Services Script for EC2
# This script starts the backend and frontend services

echo "Starting E-commerce Services..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0
    else
        return 1
    fi
}

# Kill existing services if running
echo -e "${YELLOW}Checking for existing services...${NC}"

# Kill backend if running
if check_port 9000; then
    echo -e "${YELLOW}Killing existing backend on port 9000...${NC}"
    pkill -f "python main.py" || true
    sleep 2
fi

# Kill frontend if running
if check_port 3001; then
    echo -e "${YELLOW}Killing existing frontend on port 3001...${NC}"
    pkill -f "npm run dev" || true
    pkill -f "vite" || true
    sleep 2
fi

# Navigate to project directory
# Try multiple common locations
if [ -f "main.py" ]; then
    echo -e "${GREEN}Found main.py in current directory${NC}"
elif [ -d "testneo-ecommerce-demo" ]; then
    cd testneo-ecommerce-demo
elif [ -d "~/ecom-app/testneo-ecommerce-demo" ]; then
    cd ~/ecom-app/testneo-ecommerce-demo
elif [ -d "/home/ubuntu/ecom-app/testneo-ecommerce-demo" ]; then
    cd /home/ubuntu/ecom-app/testneo-ecommerce-demo
elif [ -d "/home/ec2-user/testneoendtoend" ]; then
    cd /home/ec2-user/testneoendtoend
fi

echo -e "${YELLOW}Current directory: $(pwd)${NC}"

# Start backend in background
echo -e "${YELLOW}Starting backend on port 9000...${NC}"
nohup python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}Backend started with PID: $BACKEND_PID${NC}"

# Wait for backend to start
sleep 5

# Check if backend started successfully
if check_port 9000; then
    echo -e "${GREEN}✓ Backend is running on port 9000${NC}"
else
    echo -e "${RED}✗ Backend failed to start${NC}"
    echo "Check backend.log for errors"
    exit 1
fi

# Start frontend in background
echo -e "${YELLOW}Starting frontend...${NC}"
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend started with PID: $FRONTEND_PID${NC}"
cd ..

# Wait for frontend to start
sleep 5

# Check if frontend started successfully
if check_port 3001; then
    echo -e "${GREEN}✓ Frontend is running on port 3001${NC}"
else
    echo -e "${RED}✗ Frontend failed to start${NC}"
    echo "Check frontend.log for errors"
    exit 1
fi

echo ""
echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}All services are running!${NC}"
echo -e "${GREEN}==============================================${NC}"
echo -e "Backend URL: http://44.202.138.57:9000"
echo -e "Frontend URL: http://44.202.138.57:3001"
echo -e "Admin Panel: http://44.202.138.57:3001/admin"
echo -e "${GREEN}==============================================${NC}"
echo ""
echo "Services are running in the background."
echo "To view logs:"
echo "  Backend:  tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo ""
echo "To stop services: ./stop_services.sh"
echo ""

