#!/bin/bash

# Deployment Script for ApsnyTravelCapsuleOS
# This script automates the build and deployment process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-production}
DEPLOY_DIR="dist/public"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}ApsnyTravelCapsuleOS Deployment${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Environment: $ENVIRONMENT"
echo "Timestamp: $TIMESTAMP"
echo ""

# Step 1: Validate content
echo -e "${YELLOW}Step 1: Validating content...${NC}"
if ! python3 scripts/validate-capsules.py; then
    echo -e "${RED}Content validation failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Content validation passed${NC}"
echo ""

# Step 2: Generate report
echo -e "${YELLOW}Step 2: Generating report...${NC}"
python3 scripts/generate-report.py > "reports/report_${TIMESTAMP}.txt"
echo -e "${GREEN}✓ Report generated${NC}"
echo ""

# Step 3: Install dependencies
echo -e "${YELLOW}Step 3: Installing dependencies...${NC}"
pnpm install --frozen-lockfile
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 4: Run tests
echo -e "${YELLOW}Step 4: Running tests...${NC}"
if ! pnpm test; then
    echo -e "${RED}Tests failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Tests passed${NC}"
echo ""

# Step 5: Build application
echo -e "${YELLOW}Step 5: Building application...${NC}"
pnpm build
echo -e "${GREEN}✓ Build completed${NC}"
echo ""

# Step 6: Performance audit
echo -e "${YELLOW}Step 6: Running performance audit...${NC}"
python3 scripts/performance-audit.py > "reports/performance_${TIMESTAMP}.txt"
echo -e "${GREEN}✓ Performance audit completed${NC}"
echo ""

# Step 7: Verify build output
echo -e "${YELLOW}Step 7: Verifying build output...${NC}"
if [ ! -d "$DEPLOY_DIR" ]; then
    echo -e "${RED}Build output directory not found!${NC}"
    exit 1
fi

if [ ! -f "$DEPLOY_DIR/index.html" ]; then
    echo -e "${RED}index.html not found in build output!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Build output verified${NC}"
echo ""

# Step 8: Create backup
echo -e "${YELLOW}Step 8: Creating backup...${NC}"
if [ -d "$DEPLOY_DIR" ]; then
    tar -czf "backups/backup_${TIMESTAMP}.tar.gz" "$DEPLOY_DIR"
    echo -e "${GREEN}✓ Backup created${NC}"
fi
echo ""

# Step 9: Deployment instructions
echo -e "${YELLOW}Step 9: Deployment ready${NC}"
echo ""
echo "Build output location: $DEPLOY_DIR"
echo "Backup location: backups/backup_${TIMESTAMP}.tar.gz"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "1. Review the build output in $DEPLOY_DIR"
echo "2. Deploy to your hosting provider"
echo "3. Monitor the application for any issues"
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Deployment preparation complete!${NC}"
echo -e "${GREEN}================================${NC}"
