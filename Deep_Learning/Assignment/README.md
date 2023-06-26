목적: neural network의 구조와 그 과정 이해  
Task: 이미지를 예측하는 neural network를 구현  

특이사항 
1. 데이터의 구조를 변형시키는 범위 내에서의 코드(e.g. view, unflatten, reshape, torch.zeros) 활용은 가능, but 연산이 있는 모듈화된 코드(e.g. nn.Upsample, nn.functional.interpolate)를 사용하는 것은 불가능  
2. data는 주어진 그대로 사용해야 함. 변형 및 증강을 하는 코드 제한 -> 데이터 변형 보다는 모델 구조에 집중!

