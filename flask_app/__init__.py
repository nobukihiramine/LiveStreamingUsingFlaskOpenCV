# __init__.py
#
# Function to crate flask app.
#
# Author : Nobuki HIRAMINE, http://www.hiramine.com
# History :
#   2023/08/06 Created.

# Copyright 2023 Nobuki HIRAMINE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import flask
from flask_app.camera import Camera

def create_app():
    # Flaskインスタンスの作成
    app = flask.Flask(__name__)

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
            if( frame is None ):
                # フレーム画像の取得に失敗したときは、取得成功するまで試行する
                continue

            # yieldを使用してフレーム画像のエンティティを返す。
            # エンティティのデータはバイト列。
            # １行目は、エンティティの境界行。先頭は「--」、続けてエンティティ境界文字列。
            # ２行目は、Content-Typeフィールド行。「image/jpeg」。
            # ３行目は、空行。
            # ４行目は、データ行。jpgフォーマットのバイト列の画像データ。
            # ５行目は、空行。
            yield( b'--boundary_frame\r\n' \
                 + b'Content-Type: image/jpeg\r\n' \
                 + b'\r\n' \
                 + frame \
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
        return flask.Response( generate_frame_entity(Camera()),
                            mimetype='multipart/x-mixed-replace; boundary=boundary_frame')

    # 生成したFlaskインスタンスを返す
    return app
