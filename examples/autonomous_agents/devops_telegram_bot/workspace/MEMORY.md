# Long-Term Memory

## Server Baseline (2026-02-13)
- **Disk:** Root 16% used (82GB avail), Data volume 81% used
- **Memory:** ~10GB total, Active ~3.7GB, Free ~46MB
- **Error rate:** 13 errors/day, 6 5xx responses/day
- **Application:** Flask e-commerce API, PostgreSQL + Redis, 4 workers, port 3000

## Known Issues

### 🔴 Redis Connection Instability
- **Status:** Active concern
- **Pattern:** Disconnects 2x/day, auto-reconnects within seconds
- **Impact:** Session cache failures, brief service disruption
- **Action needed:** Monitor Redis memory usage, check Redis logs for root cause

### 🟡 Database Performance
- **Status:** Degraded
- **Queries:** 
  - `SELECT * FROM orders WHERE status='pending'` → 2340ms
  - Users/orders JOIN → 4120ms
- **Missing indexes:** `orders.status` column (confirmed in code comment)
- **Impact:** 504 gateway timeouts on /api/v1/orders endpoint
- **Action needed:** Add database indexes, review query optimization

### 🟢 Rate Limiting Working
- **Status:** Healthy
- **Config:** 1000 req/min per client
- **Evidence:** Client `api_key_prod_7x2k` properly blocked at 1042 req/min

### 🟢 Security Posture
- **Status:** Good
- **Scanner activity:** sqlmap from 185.220.101.1 properly blocked (403/400/404)
- **Probed endpoints:** /admin, /.env, /wp-admin — all blocked

## Patterns to Watch
- Redis disconnection frequency — if increases above 2x/day, investigate urgently
- Slow query warnings — track if performance degrades further
- Memory allocation errors — single MemoryError on image job #7291, watch for repeats
- Data volume disk usage at 81% — not urgent but monitor monthly

## Useful Commands
```bash
# Count errors by type
grep -E "ERROR|WARN" logs/error.log | cut -d' ' -f4 | sort | uniq -c | sort -rn

# Check for 5xx errors
grep " 5[0-9][0-9] " logs/access.log

# Redis reconnection events
grep "Redis" logs/error.log

# Slow queries
grep "Slow query" logs/error.log

# Security scanner activity
grep -E "sqlmap|scanner" logs/access.log
```

## Application Structure
- **Main:** `app/main.py` - Flask app
- **Config:** `app/config.yaml` - server/db/redis config
- **Helpers:** `app/utils/helpers.py` - token validation, input sanitization
- **Logs:** `logs/error.log`, `logs/access.log`, `logs/app-debug.log`
- **Backups:** `backups/` (empty, ready for use)
