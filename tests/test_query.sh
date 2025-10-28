#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# API endpoint
API_URL="${API_URL:-http://localhost:8000}"

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Testing RAG Medical QA API${NC}"
echo -e "${YELLOW}========================================${NC}\n"

# Test 1: Health check
echo -e "${YELLOW}[Test 1]${NC} Health Check"
HEALTH_RESPONSE=$(curl -s "${API_URL}/health")
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
    echo "Response: $HEALTH_RESPONSE"
else
    echo -e "${RED}✗ Health check failed${NC}"
    echo "Response: $HEALTH_RESPONSE"
fi
echo ""

# Test 2: Root endpoint
echo -e "${YELLOW}[Test 2]${NC} Root Endpoint"
ROOT_RESPONSE=$(curl -s "${API_URL}/")
if echo "$ROOT_RESPONSE" | grep -q "RAG Medical QA API"; then
    echo -e "${GREEN}✓ Root endpoint passed${NC}"
    echo "Response: $ROOT_RESPONSE"
else
    echo -e "${RED}✗ Root endpoint failed${NC}"
    echo "Response: $ROOT_RESPONSE"
fi
echo ""

# Test 3: Query endpoint with sample question
echo -e "${YELLOW}[Test 3]${NC} Query Endpoint - Medical Question"
QUERY_DATA='{"query": "What are the symptoms of diabetes?", "top_k": 3}'
echo "Request: $QUERY_DATA"
QUERY_RESPONSE=$(curl -s -X POST "${API_URL}/query" \
    -H "Content-Type: application/json" \
    -d "$QUERY_DATA")

if echo "$QUERY_RESPONSE" | grep -q "answer"; then
    echo -e "${GREEN}✓ Query endpoint passed${NC}"
    echo "Response: $QUERY_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$QUERY_RESPONSE"
else
    echo -e "${RED}✗ Query endpoint failed${NC}"
    echo "Response: $QUERY_RESPONSE"
fi
echo ""

# Test 4: Empty query (should fail)
echo -e "${YELLOW}[Test 4]${NC} Query Endpoint - Empty Query (Expected Failure)"
EMPTY_QUERY='{"query": "", "top_k": 3}'
echo "Request: $EMPTY_QUERY"
EMPTY_RESPONSE=$(curl -s -X POST "${API_URL}/query" \
    -H "Content-Type: application/json" \
    -d "$EMPTY_QUERY")

if echo "$EMPTY_RESPONSE" | grep -q "error\|detail"; then
    echo -e "${GREEN}✓ Empty query correctly rejected${NC}"
    echo "Response: $EMPTY_RESPONSE"
else
    echo -e "${RED}✗ Empty query should have been rejected${NC}"
    echo "Response: $EMPTY_RESPONSE"
fi
echo ""

# Test 5: Custom top_k value
echo -e "${YELLOW}[Test 5]${NC} Query Endpoint - Custom top_k"
CUSTOM_QUERY='{"query": "What is hypertension?", "top_k": 2}'
echo "Request: $CUSTOM_QUERY"
CUSTOM_RESPONSE=$(curl -s -X POST "${API_URL}/query" \
    -H "Content-Type: application/json" \
    -d "$CUSTOM_QUERY")

if echo "$CUSTOM_RESPONSE" | grep -q "answer"; then
    echo -e "${GREEN}✓ Custom top_k query passed${NC}"
    echo "Response: $CUSTOM_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$CUSTOM_RESPONSE"
else
    echo -e "${RED}✗ Custom top_k query failed${NC}"
    echo "Response: $CUSTOM_RESPONSE"
fi
echo ""

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Testing Complete${NC}"
echo -e "${YELLOW}========================================${NC}"
