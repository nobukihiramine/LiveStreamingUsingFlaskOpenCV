import flask
from camera import Camera

# Flaskインスタンスの作成
app = flask.Flask(__name__)

# Cameraインスタンスの作成
#   Cameraインスタンスのグローバル変数化の理由
#   Cameraのインスタンス化を、streamed_response関数内で行うと、「/stream」への２回目以降のアクセス時に、カメラ画像の取得に失敗する。
#   （たとえば、ブラウザのページ更新や、複数のブラウザからアクセスを行うと、「/stream」への２回目以降のアクセスとなる）
#   失敗する理由は、Cameraクラスのコンストラクタでの処理 cv2.VideoCapture(0)は、２回目以降の呼び出しが「can't open camera by index」となるから。
#   対策としては、１度生成したインスタンスを使いまわすこと。
#   対策の実現方法としては、Cameraインスタンスのグローバル変数化、もしくは、Cameraクラスのシングルトンクラス化。
#   今回は、Cameraインスタンスのグローバル変数化での対策とした。
g_camera = Camera()

# 「/」にアクセスしたときの処理
@app.route("/")
def index():
    # index.htmlを表示する
    return flask.render_template('index.html')

# フレーム画像のエンティティを生成するジェネレータ関数
def generate_frame_entity(camera):
    while True:
        # フレーム画像の取得。
        frame = camera.get_frame()

        # yieldを使用してフレーム画像のエンティティを返す。
        # エンティティのデータはバイト列。
        # １行目は、エンティティの境界行。先頭は「--」、続けてエンティティ境界文字列。
        # ２行目は、Content-Typeフィールド行。「image/jpeg」。
        # ３行目は、空行。
        # ４行目は、データ行。jpgフォーマットのバイト列の画像データ。
        # ５行目は、空行。
        yield( b'--boundary_frame\r\n'
             + b'Content-Type: image/jpeg\r\n'
             + b'\r\n'
             + frame
             + b'\r\n\r\n' )

# 「/stream」にアクセスしたときの処理
@app.route('/stream')
def streamed_response():
    # flask.Responseオブジェクトを返却する。
    # 第１引数：ジェネレータを渡すことによってストリーミングが可能となる。
    #          （ジェネレータ関数を呼び出すとジェネレータが生成される）
    # 第２引数：MIMEタイプの設定。
    #          MIMEタイプに「multipart/x-mixed-replace」を設定し、動的に更新されるコンテンツをウェブブラウザーにプッシュするようにする。
    #          マルチパートのエンティティ境界文字列を「boundary_frame」とした。
    return flask.Response( generate_frame_entity(g_camera),
                           mimetype='multipart/x-mixed-replace; boundary=boundary_frame')

# メイン関数
if __name__ == "__main__":
    app.run("0.0.0.0")
