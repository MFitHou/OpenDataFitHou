#!/bin/bash
# Quick deployment script for VPS

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}OpenDataFitHou IoT Collector - Quick Deploy${NC}"
echo ""

# Step 1: Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Installing Docker...${NC}"
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo -e "${YELLOW}Docker installed. Please logout and login again, then run this script again.${NC}"
    exit 0
fi

# Step 2: Check .env file
if [ ! -f ".env" ]; then
    if [ -f ".env.template" ]; then
        echo -e "${YELLOW}Creating .env from template...${NC}"
        cp .env.template .env
        echo -e "${YELLOW}Please edit .env file and add your API keys, then run this script again.${NC}"
        echo "Required variables:"
        echo "  - INFLUXDB_TOKEN (generate: openssl rand -base64 32)"
        echo "  - OPENWEATHER_API_KEY"
        echo "  - INFLUXDB_ADMIN_PASSWORD"
        exit 0
    else
        echo "Error: .env.template not found!"
        exit 1
    fi
fi

# Step 3: Start services
echo -e "${GREEN}Starting services...${NC}"
docker compose up -d

echo ""
echo -e "${GREEN}Deployment complete!${NC}"
echo ""
echo "Check status: docker compose ps"
echo "View logs: docker compose logs -f iot-collector"
echo ""
echo "InfluxDB UI: http://$(hostname -I | awk '{print $1}'):8086"
echo "  Username: admin"
echo "  Password: <from your .env file>"
