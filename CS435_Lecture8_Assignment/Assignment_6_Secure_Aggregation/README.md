# Secure Aggregation Simulation
**Assignment 6**

**Group Members:**
Azkaa Nasir, Abdullah Naveed

---

## Overview
This project simulates a privacy-preserving aggregation technique used in federated learning.
Multiple clients (phones) generate model update vectors. Instead of sending raw updates to the server,
each client masks its update using pairwise random masks shared with other clients.

The server receives only masked updates and computes their sum.

---

## Masking Rule
For each pair of clients (i, j):

- Client i adds mask(i,j)
- Client j subtracts mask(i,j)

Each client applies all masks related to it before sending its update.

---

## Why Masks Cancel
When the server aggregates the masked updates:
```
(update_i + mask_ij) + (update_j - mask_ij)
```

The masks cancel out:
```
+mask_ij - mask_ij = 0
```

This means the server recovers the correct total sum of all updates but cannot see any individual client update.

---

## Privacy Benefit
The server only receives masked vectors which appear random. Because masks are shared between clients, the server cannot isolate any individual update. However, the server can learn the aggregate sum of all updates. This is the exact outcome we need — useful collective information is extracted while individual privacy is preserved.

---

## Example Output
```
SECURE AGGREGATION SIMULATION

Client Updates (PRIVATE)
Client 1: [6 1 7 2 2]
Client 2: [8 9 8 6 4]
Client 3: [2 7 7 7 7]
Client 4: [4 0 6 3 7]

Masked Updates Sent To Server
Client 1: [-2  8 10  2  0]
Client 2: [ 8  8  6 -2  0]
Client 3: [12  3  9 10 12]
Client 4: [ 2 -2  3  8  8]

Server Secure Aggregate
[20 17 28 18 20]

Plain Sum (for validation)
[20 17 28 18 20]

Correctness Check:
True
```

---

## How to Run
**Requirements:** Python 3.10+, numpy
```
pip install reqs.txt
python secure_aggregation.py
```