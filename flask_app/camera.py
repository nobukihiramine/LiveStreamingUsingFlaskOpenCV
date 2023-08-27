import cv2

# Cameraクラス
# Singletonクラスとする
#   Singletonクラスとする理由
#     Cameraのインスタンス化を、streamed_response関数内で行うと、「/stream」への２回目以降のアクセス時に、カメラ画像の取得に失敗する。
#     （たとえば、ブラウザのページ更新や、複数のブラウザからアクセスを行うと、「/stream」への２回目以降のアクセスとなる）
#     失敗する理由は、Cameraクラスのコンストラクタでの処理 cv2.VideoCapture(0)は、２回目以降の呼び出しが「can't open camera by index」となるから。
#     対策としては、１度生成したインスタンスを使いまわすこと。
#     対策の実現方法として、CameraクラスのSingletonクラス化する。
class Camera(object):

    # クラスメンバー
    _instance = None
    _video_capture = None

    # コンストラクタ（Singletonクラス化）
    def __new__(cls):
        # 既にインスタンス化されている場合は、そのインスタンスを返す
        if( cls._instance is not None ):
            return cls._instance

        # まだインスタンス化されていない場合は、インスタンス生成
        cls._instance = super().__new__( cls )

        # ビデオキャプチャオブジェクトの生成
        cls._video_capture = cv2.VideoCapture(0)

        # 画像フォーマットの指定
        # 「MJPG」もしくは「YUYV」を指定する。
        # 一般的に「MJPEG」の方が高フレームレートで取得でき「YUYV」の方が高解像度で取得できる。
        # 利用可能な解像度とフレームレートの組み合わせは、Webカメラに依存する。
        # 利用可能な解像度とフレームレートの組み合わせは「v4l2-ctl --list-formats-ext」コマンドで確認できる。
        # （メモ：動作確認で使用したLogicoolのC270は、「MJPG」を指定すると
        #        「Corrupt JPEG data: ? extraneous bytes before marker 0x??」警告が大量に出た。
        #        ネット上に同様の報告複数あり。）
        #cls._video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        cls._video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
        # 解像度の指定
        # （指定した解像度が利用できない場合、
        # 　利用可能な最も近い解像度が設定される）
        cls._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cls._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # フレームレートの指定
        cls._video_capture.set(cv2.CAP_PROP_FPS, 30)

        # 生成したインスタンスを返す
        return cls._instance

    # デストラクタ
    def __del__(self):
        # ビデオキャプチャオブジェクトの解放
        self._video_capture.release()

    # フレーム画像の取得
    def get_frame(self):
        # フレーム画像の取得
        ret, frame = self._video_capture.read()
        if( ret is False ):
            print('Failed to read frame.')
            return None
        elif( frame is None ):
            print('Frame is None.')
            return None

        # 「ピクセルごとの色の配列の画像」を「jpgフォーマットのバイト列の画像」に変換
        _, jpgImage = cv2.imencode('.jpeg', frame )

        # バイト列を返す
        return jpgImage.tobytes()
