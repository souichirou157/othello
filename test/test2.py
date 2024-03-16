from test  import *
import time


start = time.time()
#手番ループ
while True:
    board.screen()

    if board.CurrentColor == black :
         print('黒の番です:', end = "")
    else:
         print('白の番です:', end = "") 
#CPU対人間
    if board.CurrentColor == board.humanColor:
        #人間の手
        IN = board.computer()
        print(IN)
        print()
    else:
        IN = board.computer()
        print(IN)
    print()       
    #座標の入力形式が正しいか確認
    if board.checkIN(IN):
        # xのMovableposの範囲は2行目からなのでindex[0]、ｙは2列目からなのでindex[1]
       x = IN_ALPHABET.index(IN[0])+1
       y = IN_NUMBER.index(IN[1])+1
    else:
        print('形式が違います:例)a5')
        continue

#手を打つ
    if not board.move(x,y):
        print('positioningerror')
        continue


#終了判定
    if board.judge_game():
        board.screen()
        print('終了')
        break
#パス
    
        
         
    if not board.MovablePos[:, :].any():
        board.CurrentColor = -board.CurrentColor
        board.initMovable() 
        print('パス')
        print()
        continue
#終了後の表示
print()

#石のカウント
count_black = np.count_nonzero(board.Raw_Board[:,:] == black)
count_white = np.count_nonzero(board.Raw_Board[:,:] == white)
print('黒',count_black)
print('白',count_white)

#勝敗の判定、黒から白の数の差分を出す
#黒から白を引いてので差が負の数なら白の勝ちになる
game_end = count_black - count_white
end = time.time()
if game_end > 0:
    print('winner black!')
    print(end-start)
elif game_end < 0:
    print('winner white!')
    print(end-start)
else:
    print('draw、、、')
    print(end-start)
    
    
#実行速度
 #1)0.28859472274780273
 #2)0.651820182800293
 #3)0.30590033531188965
 #4)0.40020084381103516
 #5)0.3393423557281494    