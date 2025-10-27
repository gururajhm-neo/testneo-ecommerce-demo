#!/bin/bash

# Diagnostic script to check services on EC2

echo "=========================================="
echo "Checking Services on EC2"
echo "=========================================="
echo ""

echo "1. Checking if processes are running..."
echo "----------------------------------------"
ps aux | grep -E "python.*main.py|npm.*dev|vite" | grep -v grep
echo ""

echo "2. Checking if ports are listening..."
echo "----------------------------------------"
sudo netstat -tuln | grep -E '3001|9000'
echo ""

echo "3. Testing backend from localhost..."
echo "----------------------------------------"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:9000/docs || echo "Backend not responding"
echo ""

echo "4. Testing frontend from localhost..."
echo "----------------------------------------"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:3001 || echo "Frontend not responding"
echo ""

echo "5. Checking UFW firewall status..."
echo "----------------------------------------"
sudo ufw status 2>/dev/null || echo "UFW not installed or not running"
echo ""

echo "6. Checking recent backend logs..."
echo "----------------------------------------"
tail -10 backend.log 2>/dev/null || echo "No backend.log found"
echo ""

echo "7. Checking recent frontend logs..."
echo "----------------------------------------"
tail -10 frontend.log 2>/dev/null || echo "No frontend.log found"
echo ""

echo "=========================================="
echo "Diagnostic Complete"
echo "=========================================="

