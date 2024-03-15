from othello  import *




#手番ループ
while True:
    board.screen()

    if board.CurrentColor == board.black :
         print('黒の番です:', end = "")
    else:
         print('白の番です:', end = "") 
#CPU対人間
    if board.CurrentColor == board.humanColor:
        #人間の手
        IN = board.computer()   #input()  human vs computer
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
count_black = np.count_nonzero(board.Square_Board[:,:] == board.black)
count_white = np.count_nonzero(board.Square_Board[:,:] == board.white)
print('黒',count_black)
print('白',count_white)


#勝敗の判定、黒から白の数の差分を出す
#黒から白を引いてので差が負の数なら白の勝ちになる
game_end = count_black - count_white
if game_end > 0:
    print('winner black!')
elif game_end < 0:
    print('winner white!')
else:
    print('draw、、、')         
    
    
    