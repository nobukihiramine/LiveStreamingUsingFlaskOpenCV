import cv2

# Cameraクラス
class Camera(object):

    # クラスメンバー
    _video_capture = None

    # コンストラクタ
    def __init__(self):
        # ビデオキャプチャオブジェクトの生成
        self._video_capture = cv2.VideoCapture(0)

        # 画像フォーマットの指定
        # 「MJPG」もしくは「YUYV」を指定する。
        # 一般的に「MJPEG」の方が高フレームレートで取得でき「YUYV」の方が高解像度で取得できる。
        # 利用可能な解像度とフレームレートの組み合わせは、Webカメラに依存する。
        # 利用可能な解像度とフレームレートの組み合わせは「v4l2-ctl --list-formats-ext」コマンドで確認できる。
        # （メモ：動作確認で使用したLogicoolのC270は、「MJPG」を指定すると
        #        「Corrupt JPEG data: ? extraneous bytes before marker 0x??」警告が大量に出た。
        #        ネット上に同様の報告多数あり。）
        #self._video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        self._video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
        # 解像度の指定
        # （指定した解像度が利用できない場合、
        # 　利用可能な最も近い解像度が設定される）
        self._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        # フレームレートの指定
        self._video_capture.set(cv2.CAP_PROP_FPS, 15)

    # デストラクタ
    def __del__(self):
        # ビデオキャプチャオブジェクトの解放
        self._video_capture.release()

    # フレーム画像の取得
    def get_frame(self):
        # フレーム画像の取得
        ret, frame = self._video_capture.read()
        if( not ret ):
            # Failed to read frame.
            return b''  # 空のバイト列を返す
        elif( frame is None ):
            # Frame is None.
            return b''  # 空のバイト列を返す

        # 「ピクセルごとの色の配列の画像」を「jpgフォーマットのバイト列の画像」に変換
        _, jpgImage = cv2.imencode('.jpeg', frame )

        # バイト列を返す
        return jpgImage.tobytes()
