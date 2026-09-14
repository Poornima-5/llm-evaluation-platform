from app.targets.mock import MockTarget

if __name__ == "__main__":
    target = MockTarget("A mock response explaining prompt injection.")
    response = target.generate("What is prompt injection?")
    print(response)