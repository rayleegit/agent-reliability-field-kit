# GraphRAG for Startup Workflows — Workshop Sample

This 20-minute workshop sample shows why a graph can improve retrieval when the answer depends on relationships—not just text similarity.

## Learning objectives

By the end, a developer can:

1. model companies, founders, needs, technologies, and programs as typed nodes and relationships;
2. retrieve a lexical seed and expand its connected context;
3. keep source provenance and traversal paths inspectable;
4. enforce access policy during retrieval; and
5. evaluate whether context is connected and source-diverse before generation.

## Run it

```bash
python3 run_demo.py
python3 -m unittest discover -s test -v
```

No credentials or dependencies are required.

## Neo4j translation

The in-memory implementation is deliberate so every reviewer can run it. In Neo4j, the central expansion maps to a parameterized Cypher query such as:

```cypher
MATCH (seed)
WHERE seed.id IN $seed_ids AND seed.access IN $allowed_access
MATCH path = (seed)-[relationship]->(neighbor)
WHERE neighbor.access IN $allowed_access
RETURN path, seed.source, neighbor.source
LIMIT $max_evidence
```

A production workshop would replace lexical seeding with Neo4j vector search or a hybrid retriever, then pass the returned paths and source metadata to the generation layer.

## Honest scope

This is a teaching/reference implementation using fictional data. It demonstrates GraphRAG concepts, access-aware traversal, provenance, and evaluation; it does not claim production Neo4j deployment experience.
