# cloud-security-platform

```mermaid
---
title: System Architecture
---
flowchart LR

A[cspm-ui] -->|http| B(cspm-api - cloud data ingestion + security analysis) --> C[postgres]
```
