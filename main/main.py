from othello  import *
import time
from timeout_timer import timeout


#手番ループ
while True:
    board.screen()
    start = time.time()
 
#CPU対人間
    if board.CurrentColor == board.humanColor:
        #人間の手
        print('黒が思考中.....')
        IN = board.computer()   #input()  human vs computer
        
    else:
        print('白が思考中.....')
        IN = board.computer()
    print()
  
    time.sleep(4) #↑が表示されてしばらく待つ
       
    if board.CurrentColor == board.color['black'] :
         print('黒の一手が決まりました') # ,end=''
         #ここにINをprintする
         time.sleep(2)
        
    else:
         print('白の一手が決まりました') # ,end =''
         #ここにINをprintする
         time.sleep(2)

    #座標の入力形式が正しいか確認
    if board.checkIN(IN):
        # xのMovableposの範囲は2行目からなのでindex[0]、ｙは2列目からなのでindex[1]
       x = board.IN_ALPHABET.index(IN[0])+1
       y = board.IN_NUMBER.index(IN[1])+1
    else:
        print('形式が違います:例)a5')
        continue

#手を打つ
    if not board.move(x,y):
        print('positioningerror')
        continue


#終了判定
    if board.finish():
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

#1と0が入っているマスをカウントして集計する
count_black = np.count_nonzero(board.Square_Board[:,:] == board.color['black'])
count_white = np.count_nonzero(board.Square_Board[:,:] == board.color['white'])
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
 #1)0.008771419525146484
 #2)0.006307840347290039
 #3)0.010956287384033203
 #4)0.011012554168701172
 #5)0.008399248123168945
 
 