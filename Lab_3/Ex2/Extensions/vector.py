import math

def calculateVectorProduct(firstVector: list[float], secondVector: list[float]) -> float:
    result: float = 0.0
    
    if(len(firstVector) != len(secondVector)):
        raise Exception("Não é possível o cálculo do produto interno do vetor!")
    
    for i in range(len(firstVector)):
        result += firstVector[i] * secondVector[i]

    return result

def calculateVectorNorm(vector: list[float]) -> float:
    result: float = 0

    for value in vector:
        result += value**2
    
    return math.sqrt(result)

def calculateVectorNormProduct(firstVector: list[float], secondVector: list[float]) -> float:
    result: float = calculateVectorNorm(firstVector) * calculateVectorNorm(secondVector)
    if result == 0:
        return 1

    return result