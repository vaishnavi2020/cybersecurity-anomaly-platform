Performance Analysis Using Little’s Law

To estimate system capacity, we applied Little’s Law:

𝐿 = 𝜆 × 𝑊

Where:

λ = arrival rate (logs/sec)

W = average processing time per log (seconds)

L = average number of logs in system

For 10,000 logs/hour:

λ = 2.78 logs/sec
W = 0.5 sec

L = 1.39 logs

Since one worker can process 2 logs/sec, we require:

2 workers to avoid backlog.

This ensures:

Low latency

No queue overflow

Horizontal scalability


if doubles


If logs become:

20,000/hour

λ = 5.56 logs/sec

Workers needed:

5.56/2 = 2.78

Round up → 3 workers

That shows your system scales horizontally.