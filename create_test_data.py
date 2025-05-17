import os
import django
import random
from datetime import datetime, timedelta

# Djangoの設定を読み込む
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tempmon.settings')
django.setup()

from core.models import Patient
from django.utils import timezone

def create_test_patients():
    
    # テストデータの作成
    for i in range(30):
        # 保険者番号を連番で生成（8桁）
        insurance_number = f"{i+1:08d}"
        
        # ランダムな生年月日（20-80歳）
        age = random.randint(20, 80)
        birth_date = timezone.now().date() - timedelta(days=age*365)
        
        # 初診日（過去1年以内）
        first_visit_date = timezone.now().date() - timedelta(days=random.randint(0, 365))
        
        # 入院日（初診日以降、またはNone）
        admission_date = None
        if random.random() < 0.3:  # 30%の確率で入院
            admission_date = first_visit_date + timedelta(days=random.randint(1, 30))
        
        # 患者データの作成
        Patient.objects.create(
            code=f"P{i+1:03d}",  # P001, P002, ... の形式
            name=f"テスト患者{i+1}",
            birth_date=birth_date,
            insurance_number=insurance_number,
            first_visit_date=first_visit_date,
            admission_date=admission_date
        )
    
    print("30件のテスト患者データを作成しました。")

if __name__ == "__main__":
    create_test_patients() 