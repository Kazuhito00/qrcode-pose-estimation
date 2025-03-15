# qrcode-pose-estimation
QRコードの姿勢推定サンプルです。<br>
> **Note**
> <br>試験的なリポジトリです
> <br>マーカーの姿勢推定を行いたいだけであれば、ArUcoマーカーやApriltagの利用を推奨します

https://github.com/user-attachments/assets/f3f57d45-a906-40f7-8cc1-058a869499f6

# Requirement 
* opencv-python 4.9.0.80 or later

# Calibration Pattern
サンプルでは以下の7×10のチェスボード型のキャリブレーションパターンを使用します。
* http://opencv.jp/sample/pics/chesspattern_7x10.pdf
  
# Usage
<img src="https://github.com/user-attachments/assets/1a52a9dc-6ccb-4ac3-a4c3-7d14fb9a447f" width="90%">
01_calibrate_camera.pyのサンプルでキャリブレーションパラメータをcsvに保存し、<br>
02_qrcode_pose_estimation.pyを実行してください。

#### 01_calibrate_camera.py
```bash
python 01_calibrate_camera.py --square_len=23.0
```
キャリブレーションパターン検出時にEnterを押すことで撮影します。<Br>
ESCを押すことでプログラムを終了し、キャリブレーションパラメータを保存します。<Br>

実行時には、以下のオプションが指定可能です。
<details>
<summary>オプション指定</summary>
   
* --device<br>
カメラデバイス番号の指定<br>
デフォルト：0
* --file<br>
動画ファイル名の指定 ※指定時はカメラデバイスより優先し動画を読み込む<br>
デフォルト：None
* --width<br>
カメラキャプチャ時の横幅<br>
デフォルト：1280
* --height<br>
カメラキャプチャ時の縦幅<br>
デフォルト：720
* --square_len<br>
キャリブレーションパターン(チェスボード)の1辺の長さ(mm)<br>
デフォルト：23.0
* --grid_size<br>
キャリブレーションパターン(チェスボード)の行列数(カンマ区切り指定)<br>
デフォルト：10,7
* --k_filename<br>
半径方向の歪み係数の保存ファイル名(csv)<br>
デフォルト：K.csv
* --d_filename<br>
円周方向の歪み係数の保存ファイル名(csv)<br>
デフォルト：d.csv
* --use_autoappend<br>
キャリブレーションパターン検出時に自動で撮影するか否か(指定しない場合はEnterで明示的に撮影)<br>
デフォルト：指定なし
* --interval_time<br>
use_autoappend指定時の撮影間隔(ms)<br>
デフォルト：100
</details>
  
#### 02_qrcode_pose_estimation.py
```bash
python 02_qrcode_pose_estimation.py --qr_size=8.7
```

実行時には、以下のオプションが指定可能です。
<details>
<summary>オプション指定</summary>
   
* --device<br>
カメラデバイス番号の指定<br>
デフォルト：0
* --file<br>
動画ファイル名の指定 ※指定時はカメラデバイスより優先し動画を読み込む<br>
デフォルト：None
* --width<br>
カメラキャプチャ時の横幅<br>
デフォルト：1280
* --height<br>
カメラキャプチャ時の縦幅<br>
デフォルト：720
* --qr_size<br>
QRコードの1辺の長さ(cm)<br>
デフォルト：8.7
* --k_filename<br>
半径方向の歪み係数の保存ファイル名(csv)<br>
デフォルト：K.csv
* --d_filename<br>
円周方向の歪み係数の保存ファイル名(csv)<br>
デフォルト：d.csv
</details>
  
# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
qrcode-pose-estimation is under [Apache-2.0 License](LICENSE).
