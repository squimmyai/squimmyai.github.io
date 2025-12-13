---
title: "Why I Stopped Using Kubernetes for Side Projects"
date: 2024-11-28
category: Infrastructure
subtitle: "After three years of over-engineering everything, I finally embraced the radical simplicity of a single VPS and some shell scripts."
excerpt: "After three years of over-engineering everything, I finally embraced the radical simplicity of a single VPS and some shell scripts."
---

I used to deploy everything to Kubernetes. A personal blog? Kubernetes. A weekend hack project? Kubernetes. A script that runs once a day? You guessed it.

It took me three years to realize I was solving problems I didn't have.

## The turning point

Last month, I spent an entire weekend debugging why my side project's pods kept getting evicted. The culprit? I'd misconfigured resource limits. The fix took 30 seconds. Finding it took 16 hours.

That's when it hit me: I was mass a small-scale problem with a large-scale solution.

## What I use now

A single VPS. Seriously. Here's my entire deployment strategy:

```bash
ssh server "cd /app && git pull && docker compose up -d"
```

That's it. No Helm charts. No ingress controllers. No service meshes. Just a server running Docker Compose.

## But what about...

**Scaling?** I don't need to scale. My side projects have maybe 10 users, and 8 of them are me testing on different devices.

**High availability?** If my blog goes down for an hour, literally nothing bad happens.

**Load balancing?** See above.

## The same philosophy applies everywhere

This is the same mindset I wrote about in [[sqlite-is-probably-fine]]. We've been conditioned to reach for enterprise-grade solutions before we've earned the problems they solve.

A VPS costs $5/month. Kubernetes costs your sanity.

## When Kubernetes actually makes sense

To be clear, Kubernetes is genuinely excellent when you need:

- Multiple teams deploying independently
- Automatic scaling based on load
- Zero-downtime deployments at scale
- Complex networking between services

If you're running a real business with real traffic and a real ops team, Kubernetes might be the right call. But if you're building something for fun on the weekend? Just use a VPS.

Start simple. Add complexity when it's earned.
