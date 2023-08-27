import cv2
import sys

# キャプチャオブジェクトの取得
cap = cv2.VideoCapture(0)
if( not cap.isOpened() ):
    print('Cannot open camera.')
    sys.exit()

# フレームの取得
ret, frame = cap.read()
if( ret is False ):
    print('Failed to read frame.')
elif( frame is None ):
    print('Frame is None.')
else:
    # 保存
    cv2.imwrite('frame.jpg', frame)

# キャプチャオブジェクトの解放
cap.release()
