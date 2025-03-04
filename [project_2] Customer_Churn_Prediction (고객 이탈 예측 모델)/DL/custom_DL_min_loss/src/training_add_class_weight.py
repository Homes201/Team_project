import numpy as np
import nni

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import lightning as L


class ChurnModule(L.LightningModule):
    def __init__(
        self,
        model: nn.Module,          # 모델 객체 (nn.Module을 상속받은 모델)
        configs: dict,
        class_weights: torch.Tensor = None,
    ):
        super().__init__()
        self.model = model         # 모델을 초기화
        self.configs = configs
        self.learning_rate = configs.get('learning_rate')  # 학습률을 초기화
        self.class_weights = class_weights

        self.val_losses = []
        self.test_losses = []

    def training_step(self, batch, batch_idx):
        # 학습 단계에서 호출되는 메서드
        X = batch.get('X')  # 입력 데이터를 가져옴
        y = batch.get('y')  # 레이블 데이터를 가져옴

        output = self.model(X)  # 모델을 통해 예측값을 계산
        
        # class weight
        if self.class_weights is not None:
            weights = self.class_weights.to(y.device)[y.long()]  # 각 샘플에 대한 가중치를 타겟에 따라 할당
            self.loss = F.binary_cross_entropy_with_logits(output, y, weight=weights)
        else:
            self.loss = F.binary_cross_entropy_with_logits(output, y)
        
        #self.loss = F.binary_cross_entropy_with_logits(output, y)  # 예측값과 실제 값 간의 손실 계산 (MSE 손실 함수 사용)

        return self.loss  # 계산된 손실 반환
    
    def on_train_epoch_end(self, *args, **kwargs):
        # 학습 에포크가 끝날 때 호출되는 메서드
        self.log_dict(
            {'loss/train_loss': self.loss},  # 학습 손실을 로그에 기록
            on_epoch=True,
            prog_bar=True,  # 진행 막대에 표시
            logger=True,    # 로그에 기록
        )
    
    def validation_step(self, batch, batch_idx):
        if batch_idx == 0:
            self.val_losses.clear()

        # 검증 단계에서 호출되는 메서드
        X = batch.get('X')  # 입력 데이터를 가져옴
        y = batch.get('y')  # 레이블 데이터를 가져옴

        output = self.model(X)  # 모델을 통해 예측값을 계산
        
        if self.class_weights is not None:
            weights = self.class_weights.to(y.device)[y.long()]  # 각 샘플에 대한 가중치를 타겟에 따라 할당
            self.val_loss = F.binary_cross_entropy_with_logits(output, y, weight=weights)
        else:
            self.val_loss = F.binary_cross_entropy_with_logits(output, y)
    
        #self.val_loss = F.binary_cross_entropy_with_logits(output, y)  # 예측값과 실제 값 간의 검증 손실 계산 (MSE 손실 함수 사용)
        self.val_losses.append(self.val_loss)

        return self.val_loss  # 검증 손실 반환
    
    def on_validation_epoch_end(self):
        # 검증 에포크가 끝날 때 호출되는 메서드
        val_losses_cpu = [loss.cpu().numpy() for loss in self.val_losses]
        val_loss_mean = np.mean(val_losses_cpu)
        
        self.log_dict(
            {'loss/val_loss': val_loss_mean,  # 검증 손실을 로그에 기록
             'learning_rate': self.optimizers().param_groups[0].get('lr')},  # 학습률도 로그에 기록
            on_epoch=True,
            prog_bar=True,  # 진행 막대에 표시
            logger=True,    # 로그에 기록
        )

        if self.configs.get('nni'):
            nni.report_intermediate_result(val_loss_mean.item())

    def test_step(self, batch, batch_idx):
        if batch_idx == 0:
            self.test_losses.clear()

        # 테스트 단계에서 호출되는 메서드
        X = batch.get('X')  # 입력 데이터를 가져옴
        y = batch.get('y')  # 레이블 데이터를 가져옴

        output = self.model(X)  # 모델을 통해 예측값을 계산

        test_loss = F.binary_cross_entropy_with_logits(output, y)
        self.test_losses.append(test_loss)

        return output  # 예측된 레이블 반환

    def on_test_epoch_end(self):
        test_losses_cpu = [loss.cpu().numpy() for loss in self.test_losses]
        test_loss_mean = np.mean(test_losses_cpu)
        nni.report_final_result(test_loss_mean)

    def configure_optimizers(self):
        # 옵티마이저와 스케줄러를 설정하는 메서드
        optimizer = optim.Adam(
            self.model.parameters(),  # 모델의 파라미터를 옵티마이저에 전달
            lr=self.learning_rate,    # 학습률 설정
            weight_decay=1e-4,
        )
        scheduler = optim.lr_scheduler.CyclicLR(
            optimizer,
            base_lr=1e-4,
            step_size_up=5,
            step_size_down=10,
            max_lr= 0.01,
            gamma=0.5,
            mode='triangular',
            verbose=True
        )

        return {
            'optimizer': optimizer,   # 옵티마이저 반환
            'lr_scheduler': {
                'scheduler': scheduler,
                'monitor': 'loss/val_loss',  # 검증 손실을 기준으로 스케줄러 작동
                'interval': 'epoch',
                'frequency': 1,
            }     
        }
