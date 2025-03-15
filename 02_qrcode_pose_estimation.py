#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import cv2
import numpy as np


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)

    parser.add_argument("--qr_size", type=float, default=8.7)

    parser.add_argument("--k_filename", type=str, default="K.csv")
    parser.add_argument("--d_filename", type=str, default="d.csv")

    args = parser.parse_args()
    return args


def main():
    # コマンドライン引数
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    qr_size = args.qr_size

    k_filename = args.k_filename
    d_filename = args.d_filename

    # キャリブレーションデータの読み込み
    camera_mat = np.loadtxt(k_filename, delimiter=",")
    dist_coef = np.loadtxt(d_filename, delimiter=",")

    # カメラを起動
    cap = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # QRコード検出器の生成
    qr_detector = cv2.QRCodeDetector()

    # 実世界座標の定義（左上を原点、Z=0の平面上）
    obj_points = np.array(
        [
            [0, 0, 0],
            [qr_size, 0, 0],
            [qr_size, qr_size, 0],
            [0, qr_size, 0],
        ],
        dtype=np.float32,
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # QRコード検出
        retval, decoded_info, points, _ = qr_detector.detectAndDecodeMulti(frame)
        if not retval or points is None:
            pass
        else:
            # 検出された各QRコードについて処理
            for qrcode_index, data in enumerate(decoded_info):
                # 空文字列の場合は無視
                if data == "":
                    continue

                # points[index] は各QRコードの4角点（形状: (4,2)）
                pts = points[qrcode_index].astype(np.float32)

                # 姿勢推定: solvePnPにより回転ベクトルと並進ベクトルを計算
                ret_pnp, rvec, tvec = cv2.solvePnP(
                    obj_points, pts, camera_mat, dist_coef
                )
                if ret_pnp:
                    # 回転ベクトルから回転行列に変換
                    R, _ = cv2.Rodrigues(rvec)

                    # QRコードの中心はオブジェクト座標系上で (qr_size/2, qr_size/2, 0)
                    center_obj = np.array(
                        [[qr_size / 2], [qr_size / 2], [0]], dtype=np.float32
                    )
                    # 中心位置をカメラ座標系に変換
                    tvec_center = tvec + R.dot(center_obj)

                    # デバッグ描画
                    # 検出したQRコードの4角点を画像に描画
                    for point_index in range(4):
                        pt1 = tuple(pts[point_index].astype(int))
                        pt2 = tuple(pts[(point_index + 1) % 4].astype(int))
                        cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
                    # ARUCOマーカーのようにQRコード中心を原点とした座標軸を描画
                    cv2.drawFrameAxes(
                        frame, camera_mat, dist_coef, rvec, tvec_center, qr_size / 2, 2
                    )
                    # カメラからQRコード中心までの相対座標をテキスト表示
                    # 表示位置は右下の角付近（pts[3]）に描画
                    cv2.putText(
                        frame,
                        "X:{:.1f}cm Y:{:.1f}cm".format(
                            tvec_center[0][0], tvec_center[1][0]
                        ),
                        (int(pts[3][0]), int(pts[3][1]) - 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        "Z:{:.1f}cm".format(tvec_center[2][0]),
                        (int(pts[3][0]), int(pts[3][1]) - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )

        cv2.imshow("QR Code Pose Estimation", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESCキーで終了
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
