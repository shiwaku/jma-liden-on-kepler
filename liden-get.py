import requests
import time
from datetime import datetime, timedelta
import os

# 開始時間と終了時間を設定
start_time = datetime(2024, 8, 7, 16, 0, 0)  # 日本時間 2024/08/07 16:00:00
end_time = datetime(2024, 8, 7, 22, 0, 0)    # 日本時間 2024/08/07 22:00:00
delta = timedelta(minutes=5)

# 出力フォルダを設定
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# 日本時間をUTCに変換
def to_utc(jst_time):
    return jst_time - timedelta(hours=9)

# GeoJSONを取得して保存する関数
def fetch_geojson(jst_time, utc_time):
    url = f"https://www.jma.go.jp/bosai/jmatile/data/nowc/{utc_time}/none/{utc_time}/surf/liden/data.geojson?id=liden"
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"{output_folder}/data_{jst_time}.geojson"
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Successfully fetched and saved data for {jst_time}")
    else:
        print(f"Failed to fetch data for {jst_time}, status code: {response.status_code}")

# メインループ
current_time = start_time
while current_time <= end_time:
    utc_time = to_utc(current_time).strftime("%Y%m%d%H%M%S")
    jst_time = current_time.strftime("%Y%m%d%H%M%S")
    fetch_geojson(jst_time, utc_time)
    current_time += delta
    time.sleep(1)  # 連続リクエストを避けるためのスリープ
