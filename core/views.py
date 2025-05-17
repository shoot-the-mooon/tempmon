from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient, VitalSigns
from django.utils import timezone
import uuid
from datetime import timedelta
import json
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder

def patient_list(request):
    # 検索クエリの取得
    search_query = request.GET.get('search', '')
    
    # 検索条件に基づいてクエリを構築
    if search_query:
        patients = Patient.objects.filter(
            Q(name__icontains=search_query) |  # 名前で検索（部分一致）
            Q(insurance_number__icontains=search_query)  # 保険者番号で検索
        ).order_by("admission_date")
    else:
        patients = Patient.objects.all().order_by("admission_date")
    
    # ページネーション
    paginator = Paginator(patients, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "list.html", {
        "page_obj": page_obj,
        "search_query": search_query
    })

def patient_add(request):
    if request.method == "POST":
        patient = Patient.objects.create(
            code=str(uuid.uuid4())[:8],  # 8文字のランダムなコードを生成
            name=request.POST.get("name", ""),
            birth_date=request.POST.get("birth_date") or None,
            insurance_number=request.POST.get("insurance_number", ""),
            first_visit_date=request.POST.get("first_visit_date") or None,
            admission_date=request.POST.get("admission_date") or None,
        )
        return redirect("detail", pk=patient.pk)
    return render(request, "patient_add.html")

def patient_detail(request, pk):
    p = get_object_or_404(Patient, pk=pk)
    
    # 期間の取得（デフォルトは1週間）
    period = request.GET.get('period', 'week')
    end_date = timezone.now()
    
    # 期間に応じて開始日を設定
    if period == 'week':
        start_date = end_date - timedelta(days=7)
    elif period == 'month':
        start_date = end_date - timedelta(days=30)
    elif period == 'all':
        start_date = None
    else:
        # 不正な期間パラメータの場合はデフォルトの週間表示にフォールバック
        period = 'week'
        start_date = end_date - timedelta(days=7)
    
    # 期間でフィルタリング
    if start_date:
        vitals = VitalSigns.objects.filter(
            patient=p,
            measured__gte=start_date,
            measured__lte=end_date
        ).order_by('-measured')  # 新しい順に並べる
    else:
        # 'all'の場合は全データを取得
        vitals = VitalSigns.objects.filter(patient=p).order_by('-measured')  # 新しい順に並べる
    
    # 時間フォーマットを設定
    if period == 'all':
        time_format = "%Y/%m/%d %H:%M"
    else:
        time_format = "%m/%d %H:%M"
    
    # グラフ用データ - 古い順
    graph_vitals = list(vitals.order_by('measured'))
    
    # データ準備
    labels = []
    temps = []
    pulses = []
    
    for v in graph_vitals:
        local_time = timezone.localtime(v.measured)
        labels.append(local_time.strftime(time_format))
        
        # 体温データを確実に数値型に変換
        if v.celsius is not None:
            try:
                temp_value = float(v.celsius)
            except (ValueError, TypeError):
                temp_value = None
        else:
            temp_value = None
        temps.append(temp_value)
        
        pulses.append(v.pulse)
    
    # 表示用の詳細データを準備（新しい順）
    vitals_data = []
    for v in vitals:
        local_time = timezone.localtime(v.measured)
        vitals_data.append({
            'measured': local_time.strftime(time_format),
            'celsius': v.celsius,
            'pulse': v.pulse,
            'systolic': v.systolic,
            'diastolic': v.diastolic,
            'weight': v.weight,
            # 血圧表示用（例：120/80）
            'blood_pressure': f"{v.systolic}/{v.diastolic}" if v.systolic and v.diastolic else "-"
        })
    
    # JSONエンコード用にリストをJSONに変換
    labels_json = json.dumps(labels, cls=DjangoJSONEncoder)
    temps_json = json.dumps(temps, cls=DjangoJSONEncoder)
    pulses_json = json.dumps(pulses, cls=DjangoJSONEncoder)
    
    return render(request, "detail.html", {
        "patient": p,
        "labels": labels_json,
        "temps": temps_json,
        "pulses": pulses_json,
        "period": period,
        "vitals_count": len(vitals),  # デバッグ用：取得データ数
        "vitals_data": vitals_data,   # 表示用の詳細データ
    })

def add_temp(request, pk):
    p = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        measured_str = request.POST.get("measured")
        if measured_str:
            try:
                # タイムゾーン情報を付加
                measured = timezone.make_aware(timezone.datetime.strptime(measured_str, "%Y-%m-%dT%H:%M"))
            except ValueError:
                # 日付形式が不正な場合は現在時刻を使用
                measured = timezone.now()
        else:
            measured = timezone.now()
            
        VitalSigns.objects.create(
            patient=p,
            measured=measured,
            celsius=request.POST.get("celsius", ""),
            pulse=request.POST.get("pulse") or None,
            systolic=request.POST.get("systolic") or None,
            diastolic=request.POST.get("diastolic") or None,
            weight=request.POST.get("weight") or None,
        )
        return redirect("detail", pk=pk)
    
    # 現在時刻の5分前をdatetime-localフォーマットに変換
    jst_now = timezone.localtime(timezone.now())
    dt = jst_now - timedelta(minutes=5)
    current_time = dt.strftime("%Y-%m-%dT%H:%M")
    return render(request, "add.html", {
        "patient": p,
        "current_time": current_time
    })