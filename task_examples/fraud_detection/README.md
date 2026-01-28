# Banking Fraud Detection

This example demonstrates a comprehensive **Upsonic LLM agent** that detects potential fraud in banking transactions using multiple storage providers and persistent memory.

## Overview

The fraud detection agent analyzes banking transactions and user behavior patterns to identify suspicious activities. It uses:

1. **Transaction Analysis** — examines amount, merchant, location, and timing patterns
2. **User Profiling** — maintains persistent user behavior profiles across sessions  
3. **Risk Assessment** — provides fraud probability scores and recommendations
4. **Multi-Storage Support** — demonstrates all available storage providers

The agent uses LLM reasoning combined with custom tools for merchant reputation, location verification, and pattern analysis.

---

## Setup

### 1. Install dependencies

```bash
uv add upsonic
uv add upsonic[storage]
```

### 2. Start required services (optional)

For full functionality with all storage providers, start the required services:

```bash
# Start Redis, MongoDB, and PostgreSQL
./docker_services.sh
```

**Note**: JSON, SQLite, InMemory, and Mem0 storage work without external services.

---

## Run the Agent

### Basic fraud detection (JSON storage)

```bash
# Run with JSON storage (no external services required)
uv run task_examples/fraud_detection/fraud_detection.py --storage json
```

### Run with specific storage provider

```bash
# SQLite storage
uv run task_examples/fraud_detection/fraud_detection.py --storage sqlite

# Redis storage (requires Redis service)
uv run task_examples/fraud_detection/fraud_detection.py --storage redis

# MongoDB storage (requires MongoDB service)  
uv run task_examples/fraud_detection/fraud_detection.py --storage mongo

# PostgreSQL storage (requires PostgreSQL service)
uv run task_examples/fraud_detection/fraud_detection.py --storage postgres

# Mem0 storage (cloud-based)
uv run task_examples/fraud_detection/fraud_detection.py --storage mem0

# In-memory storage (ephemeral)
uv run task_examples/fraud_detection/fraud_detection.py --storage inmemory
```

### Test all storage providers

```bash
# Run with all available storage providers
uv run task_examples/fraud_detection/fraud_detection.py --storage all
```

### Quick test (JSON storage only)

```bash
# Simple test with JSON storage (no external dependencies)
uv run task_examples/fraud_detection/test_example.py
```

### Example Output

**Transaction Analysis:**

```json
{
  "is_fraud": true,
  "risk_score": 0.85,
  "risk_factors": ["Unusual merchant", "High amount", "Suspicious location"],
  "confidence": 0.92,
  "recommendation": "Block transaction and contact user",
  "suspicious_patterns": ["Merchant blacklisted", "Location inconsistent"]
}
```

---

## How It Works

1. **Input**: The agent receives transaction details and user profile data
2. **Tool Usage**: Custom tools check merchant reputation, location consistency, and transaction patterns
3. **LLM Analysis**: The agent reasons about fraud indicators using all available information
4. **Memory**: Results are stored persistently using the selected storage provider
5. **Output**: Returns structured fraud analysis with risk scores and recommendations

### Storage Providers Demonstrated

- **JSON**: File-based storage for development
- **SQLite**: Local database for production
- **Redis**: High-performance in-memory storage
- **MongoDB**: Document-based NoSQL storage
- **PostgreSQL**: Relational database storage
- **Mem0**: Cloud-based memory service
- **InMemory**: Ephemeral storage for testing

---

## File Structure

```bash
task_examples/fraud_detection/
├── fraud_detection.py      # Main fraud detection agent
├── test_example.py         # Simple test script
├── docker_services.sh      # Docker setup script
└── README.md               # This file
```

---

## Features Demonstrated

- **Agent with Memory**: Persistent session and user memory across interactions
- **Custom Tools**: Merchant reputation, location verification, pattern analysis
- **Structured Output**: Pydantic models for type-safe responses
- **Multi-Storage**: Support for all Upsonic storage providers
- **Async Operations**: Full async/await support for high performance
- **Error Handling**: Graceful handling of storage provider failures

---

## Notes

- **Production Ready**: Demonstrates real-world fintech fraud detection patterns
- **Extensible**: Easy to add new fraud detection rules and storage providers
- **Memory Persistence**: User profiles and session data persist across runs
- **Tool Integration**: Shows how to integrate external APIs and services
- **Use Case**: Ideal for banking, fintech, and financial services applications
