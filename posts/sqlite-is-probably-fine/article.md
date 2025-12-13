---
title: "SQLite is Probably Fine"
date: 2024-11-14
category: Databases
subtitle: "Your startup doesn't need Postgres. It definitely doesn't need a distributed database."
excerpt: "Your startup doesn't need Postgres. It definitely doesn't need a distributed database. Let me explain."
---

Every few months, I see the same pattern play out. A team spins up a new project. Within the first week, someone's already drafted an {note: RFC}(Request for Comments — a doc proposing technical decisions, borrowed from the IETF tradition.) for the database architecture. It includes words like "sharding," "replication," and "eventual consistency."

The project? A todo app with maybe three users.

## The complexity trap

We've been conditioned to believe that "real" applications need "real" databases. PostgreSQL at minimum. Maybe {note: CockroachDB}(A distributed SQL database designed to survive datacenter failures. Overkill for 99% of projects.) if you're feeling fancy. Redis for caching, of course. And don't forget the message queue.

> "But what if we need to scale?"

You won't. Not for a long time. And when you do, migration is a solved problem. The real risk isn't hitting SQLite's limits — it's spending six months building infrastructure for users who don't exist yet.

## What SQLite actually handles

Let's talk numbers. SQLite can handle:

- Hundreds of thousands of reads per second
- Thousands of writes per second (with {note: WAL mode}(Write-Ahead Logging — writes go to a separate log first, allowing concurrent reads without blocking.))
- Databases up to 281 terabytes
- Concurrent readers without blocking

For context, most SaaS products never exceed a few hundred concurrent users. You're probably fine.

## The deployment story

Here's my favorite part. Your entire database is a single file. Backups? `cp database.db backup.db`. Deployment? It's already there. No connection strings, no credentials management, no network latency.

```bash
# Your entire backup strategy
cp /data/app.db /backups/app-$(date +%Y%m%d).db
```

There's something deeply satisfying about a system you can reason about completely. No mysterious connection pools. No "the replica is lagging" incidents at 3am. Just a file.

## When to actually reach for Postgres

I'm not saying SQLite is always the answer. Reach for something heavier when you need multiple servers writing to the same database, or when you need advanced features like full-text search with custom ranking, JSONB operations, or PostGIS.

But be honest with yourself about whether you actually need those things today, or whether you're just planning for a future that may never arrive.

Start simple. Add complexity when it's earned.
