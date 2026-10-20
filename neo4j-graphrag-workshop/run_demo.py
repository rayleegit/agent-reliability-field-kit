from graphrag import demo_graph, evaluate


def main() -> None:
    question = "How could a compliance startup use GraphRAG and evaluation?"
    evidence = demo_graph().retrieve(question)
    for item in evidence:
        print(f"[{item.source}] {item.path}: {item.text}")
    print(evaluate(question, evidence))


if __name__ == "__main__":
    main()
