from targets.mock import MockTarget


target = MockTarget()

response = target.generate("What is prompt injection?")

print(response)