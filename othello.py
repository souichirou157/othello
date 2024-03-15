import numpy as np
import random
import sys

#方向（8桁の2進数,おける範囲は8ｘ8マス）
NONE = 0
LEFT = 2**0        #1        00000001 
UPPER_LEFT = 2**1  #=2       00000010
UPEER = 2**2       # =4      00000100
UPEER_RIGHT = 2**3 # 8       00001000
RIGHT = 2**4 # =16           00010000
LOWER_RIGHT = 2**5 # =32     00100000
LOWER = 2**6 # =64           01000000
LOWER_LEFT = 2**7 # = 128    01000000

#手の表現
IN_ALPHABET = ['a','b','c','d','e','f','g','h']
IN_NUMBER  =  ['1','2','3','4','5','6','7','8']

square = len(IN_ALPHABET)



#人間の色 
if len(sys.argv) ==2:
    HUMAN_COLOR =sys.argv[1] 
else:
    HUMAN_COLOR = 'B'    

    

class Board:
    def __init__(self):
        
        #石の置けないマス
        self.wall = 2
        #石を置けるマスの範囲８ｘ８
        self.board_size = 8
        #オセロ板の生成 
        self.Square_Board = np.zeros(( self.board_size + self.wall, self.board_size + self.wall ),dtype  = int)
        
        
        #壁を設定
        self.Square_Board[:,0] = self.wall  #全ての列の0行目はアルファベットを振ってあるので石を置けない
        self.Square_Board[0,:] = self.wall  #0列目の全ての行は番号が振ってあるので石を置けない
       
        self.Square_Board[:,self.board_size + 1] = self.wall #全ての列の9行目は石が置けない
        self.Square_Board[self.board_size +1, :] = self.wall #9列目のすべての行は石が置けない
      
        #石の色
        self.white = -1
        self.black = 1 
        
        
        #スタート時の石の配置　黒は１、白は　‐１
        self.Square_Board[4,4] = self.white #-1
        self.Square_Board[5,5] = self.white 
        self.Square_Board[4,5] = self.black # 1
        self.Square_Board[5,4] = self.black
        
        #順番
        self.Turns = 0
        
        #石が置いてないマス
        self.free = 0
        
        
        #手番の数
        self.JUDGE_TURN = 60
        
      
        
        
        #順番が回っている色
        self.CurrentColor = self.black


        self.MovablePos = np.zeros((self.board_size + self.wall ,self.board_size  + self.wall),dtype =int)
        self.MovableDir = np.zeros((self.board_size + self.wall , self.board_size + self.wall),dtype = int)

        self.initMovable()
        
        if HUMAN_COLOR == 'B':
            self.humanColor = self.black
        elif HUMAN_COLOR == 'W':
            self.humanColor = self.white
        else:
            print('引数にBかWを指定してください')
            sys.exit()     

        

#石をおいたときに裏返す方向を探すプログラム
    def checkMobility(self,x,y,color):
        
        #指定の空きマス
        dir = 0
        #既にある場合は置けないようにする
        if(self.Square_Board[x,y] != self.free):
            return dir
        
        #左） ひっくりかえせるか探す
        if(self.Square_Board[x -1 ,y] == - color):#一つ進んだ先に石があるか
            
            #上のスクリプトとこのスクリプトで挟んだ相手の石の数を確認している
            x_temp = x - 2 #左横の一つ先の座標
            y_temp = y
            
            #医師の座標が白の間
            while self.Square_Board[x_temp, y_temp] == -color:
                x_temp -=1     
            #石の色が変わるので、dirの石を裏返せる方向の情報の更新が起きる
            if self.Square_Board[x_temp,y_temp] == color:
                dir = dir|LEFT
            
        #左上）ｘのインデックス　－１，ｙもー１
        if(self.Square_Board[x -1, y -1] == -color): #進んだ先に相手の石があるか
            
            x_temp = x-2 #左横の一つ先の座標座標
            y_temp = y-2 #上方向の一つ先の座標
            
            #相手の石の数だけ石を返す、プログラムは上方向から石を探している
            while self.Square_Board[x_temp,y_temp] == -color:
                x_temp -=1
                y_temp -=1
            # 石の色がかわるので、ｄｉｒの石を裏返せる方向の情報が更新される
            if self.Square_Board[x_temp,y_temp] ==   color:
                dir = dir|UPPER_LEFT
        
        #上）真上に行くのでｙのインデックス－１
        if(self.Square_Board[x, y -1] == -color): #進んだ先に相手の石があるか
            
            x_temp = x
            y_temp = y-2 #上方向の一つ先の座標
            #相手の石の数だけ返す
            while self.Square_Board[x_temp,y_temp] == -color:
                y_temp -= 1
            #石の色が変わるので、ｄｉｒの石を裏返せる方向の情報が更新
            if self.Square_Board[x_temp,y_temp] == color:      
                dir = dir|UPEER
        
        #右上　右横に進む、ｘのインデックス＋１ｙは下がる
        if(self.Square_Board[x +1,y-1] == -color): #進んだ先に相手の石があるか
            
            x_temp = x + 2 #右横の一つ先の座標
            y_temp = y - 2 #上方向の一つ先の座標
            
            #相手の石の数だけ返す
            while self.Square_Board[x_temp,y_temp] == -color:
                x_temp +=1
                y_temp -=1
            #石の色が変わるので、ｄｉｒの石を裏返せる方向の情報が更新される
            if self.Square_Board[x_temp,y_temp] ==   color:
                dir = dir|UPEER_RIGHT
            
        # 右　横に行くだけ、ｘのインデックスが＋１
        if(self.Square_Board[x +1 ,y]==  -color):#進んだ先に相手の石があるか
            
            x_temp = x + 2 #右横の一つ先の座標
            y_temp = y     
            #相手の石の数だけ返す
            while self.Square_Board[x_temp,y_temp] ==  -color:
                x_temp +=1
            #石の色がかわるので、ｄｉｒの石を裏返せる方向の情報が更新される
            if self.Square_Board[x_temp,y_temp] == color:
                dir = dir | RIGHT
                
        #右下）　右横に行く、ｘのインデックス＋１、下に一つ進む、ｙのインデックスが＋１　
        if(self.Square_Board[x + 1, y + 1 ]== -color): #進んだ先に相手の石があるか
            
            x_temp = x + 2 #右横の一つ先の座標
            y_temp = y + 2 #下の一つ先の座標
            
            #相手の石の数だけ返す
            while self.Square_Board[x_temp,y_temp] == -color:
                x_temp +=1
                y_temp +=1
            #石の色がかわるので、ｄｉｒの石を裏返せる情報の更新がされる
            if self.Square_Board[x_temp,y_temp] == color:
                dir = dir|LOWER_RIGHT
        
        #下）　真下に行くので　ｙのみインデックスが＋１
        if(self.Square_Board[x, y + 1]==-color): #進んだ先に相手の石があるか
            x_temp = x
            y_temp = y + 2 #石を置いた1つ先の場所を代入 
            
            #相手の石の数だけ返す
            while self.Square_Board[x_temp,y_temp] == -color:
                y_temp +=1
            #石の色がかわるので、ｄｉｒの石を裏返せる情報が更新される
            if self.Square_Board[x_temp,y_temp] == color:
                dir = dir|LOWER    
                
        # 左下）左横　ｘのインデックス　―１　ｙはインデックス＋１
        if(self.Square_Board[x-1, y + 1 ]==-color): #進んだ先に相手の石があるか        
            
            #どちらも置いたマスの一つ先の座標
            x_temp = x -2 #左横の一つ先
            y_temp = y +2 #下方向の一つ先
            
            #相手の石の数だけ返す
            while self.Square_Board[x_temp,y_temp] == -color:
                x_temp  -=1
                y_temp  +=1 
            if self.Square_Board[x_temp,y_temp] == color:
                dir = dir|LOWER_LEFT
        
        return dir            
        
        
        
                                  
    #盤面の反映）CurrentColorはーをかけると反対の色になる,
    #{黒：１,白：－１}　 2進数は if文右横にそれぞれ表示 
    def flipDiscs(self,x,y):
    #石を置く
        self.Square_Board[x,y] = self.CurrentColor
    
        #石を裏返す動き
        #MobableDir裏返せる方向の座標をｄｉｒに代入している
        dir = self.MovableDir[x,y]
        
        #１左)#MovableDirの2進数と成立しているか確認する
        if dir & LEFT:
            x_temp = x -1  # 00000010
            
        #成立したら色を更新する　＊-を成立時のCurrentcolorに掛け代入し直して更新される
            while self.Square_Board[x_temp,y] == -self.CurrentColor:
                self.Square_Board[x_temp,y] = self.CurrentColor
                
                #挟まれた石を全て裏返し終えるまで続く
                x_temp -=1    
        
        #２左上) MovableDirの2進数と成立している確認
        if dir & UPPER_LEFT:
            x_temp = x -1
            y_temp = y -1  # 00000010
            
        #成立したら色を更新する　＊-を成立時のCurrentcolorに掛け代入し直して更新される
            while self.Square_Board[x_temp,y_temp] == -self.CurrentColor:
                self.Square_Board[x_temp,y_temp] = self.CurrentColor
                
                #挟まれた石を全て裏返し終えるまで続く
                x_temp -= 1
                y_temp -= 1
        
        #４上）MovableDirの2進数と成立している成立するか確認
        if dir & UPEER:
            
            y_temp = y -1 #00000100
            
        #成立したら色を更新する　＊-を成立時のCurrentcolorに掛け代入し直して更新される
            while self.Square_Board[x,y_temp] == -self.CurrentColor:
                self.Square_Board[x,y_temp] = self.CurrentColor
                
                #挟まれた石を全て裏返し終えるまで続く
                y_temp -= 1            
       
        #8) 右上）MovableDirの2進数と成立しているか確認 
        if dir & UPEER_RIGHT:
            
            x_temp = x + 1
            y_temp = y - 1   #00001000、右上
        
        #成立したら色を更新する　＊-を成立時のCurrentcolorに掛け代入し直して更新される
            while self.Square_Board[x_temp,y_temp] == -self.CurrentColor:
                self.Square_Board[x_temp,y_temp] = self.CurrentColor
            #挟まれた石を全て裏返し終えるまで続く
                x_temp += 1
                y_temp -= 1
        
        #16)右）MovableDirの2進数と成立しているか確認
        if dir & RIGHT:
            
            x_temp = x + 1 #00010000
        
        #成立したら色を更新する　＊-を成立時のCurrentcolorに掛け、代入し直して更新される
            while self.Square_Board[x_temp,y] == -self.CurrentColor:
                self.Square_Board[x_temp,y] = self.CurrentColor
            #挟まれた石を全て裏返し終えるまで続く
                x_temp += 1    
        
        #32右下)　MovableDirの2進数と成立しているか確認
        if dir & LOWER_RIGHT:
            
            x_temp = x + 1 #00100000
            y_temp = y + 1
        
        #成立したら色を更新する　*ーを成立時のCurrentcolorに掛け、代入し直して更新される
            
            while self.Square_Board[x_temp,y_temp] == -self.CurrentColor:
                 self.Square_Board[x_temp,y_temp] = self.CurrentColor
            
            #挟まれた石を全て裏返し終える続く
                 x_temp +=1
                 y_temp +=1     
        
        #64)下） MovableDirの2進数が成立しているか確認
        if dir & LOWER:

            y_temp = y + 1 #01000000
        #成立したら色を更新する　＊ーを成立時のCurrentcolorに掛け、代入して更新される
            
            while self.Square_Board[x,y_temp] == -self.CurrentColor:
                self.Square_Board[x,y_temp] = self.CurrentColor
            
            #挟まれた石を全て裏返し終えるまで続く
                y_temp +=1    
            
        #128) 左下）MovableDirの２進数が成立しているか確認
        if dir & LOWER_LEFT:
            
            x_temp = x - 1
            y_temp = y + 1   #100000000
        #成立したら色を更新する
            while self.Square_Board[x_temp,y_temp] == -self.CurrentColor:
                self.Square_Board[x_temp,y_temp] = self.CurrentColor

        #挟まれた石を全て裏返し終えるまで続く
                x_temp -=1
                y_temp +=1
        
             
                 
            
    
    def move(self,x,y):
        
    

        if x < 1 or self.board_size < x:
            return False
        if y < 1 or self.board_size < y:
            return False
        if self.MovablePos[x,y] == 0:
            return False
     
        #石を裏返す
        self.flipDiscs(x,y)
        
        #手番を進める
        self.Turns +=1
        
        #手番を交代
        self.CurrentColor = - self.CurrentColor
        
        #MovableposとMovableDirの更新
        self.initMovable()
        
        return True
        
        
    #MovablePos, MovableDirの更新    
    def initMovable(self):
            
        #MovablePosの初期化（すべてFalseにする）
        self.MovablePos[:,:] = False
            
        # 壁以外のマスに対してループ
        for x in range(1, self.board_size +1):
            for y in range(1, self.board_size+1):
                
                #checkMobility関数の実行
                dir = self.checkMobility(x,y,self.CurrentColor)
            
                #各マスのMobavleDirにそれぞれのdirを代入
                self.MovableDir[x,y] = dir
            
                #dirが０でないならMovablePosにTrueを代入
                if dir !=0:
                    self.MovablePos[x,y] = True

#終局の判定
    def finish(self):
        #60ターン目に勝負が決まれば終了、手番がループするのを全てFalseで返している
        if self.Turns>=self.JUDGE_TURN:
            return True

        #(player)打てる手があれば続行
        if self.MovablePos[:,:].any():
            return False
        #(computer)打てる手があれば続行
        for x in range(1,self.board_size+1):
            for y in range(1,self.board_size):
       #おける場所が1つでもあれば終了ではない
                if self.checkMobility(x,y,-self.CurrentColor) !=0:
                    return False

        #ここにたどり着くときはゲームが終了
        return True


#パスの判定をする関数を入れる
    def skip(self):
      #全ての要素が０の時だけパス
        if any(self.MovablePos[:,:]):
            return False
    #ゲームが終了時にはパスできない
        if self.finish():
            return False
    #ここに来たらパスなので相手の順番になる
        self.CurrentColor = -self.CurrentColor
    #MobablePosとMovableDirの更新
        self.initMovable()
        return True
#---------------------------

    # 盤面を表示
    def screen (self):
        #x軸の座標
        
        for x in range(self.board_size):
            print(IN_ALPHABET[x],end=" ")
        print() 
        #縦軸方向にマスをループ
        for y in range(self.board_size):         
        
            print(IN_NUMBER[y],end = "")

            for x in range(self.board_size):
                
                #マスの配置が更新される
                grid = self.Square_Board[x+1,y+1]
                
                #各表示の設定
                if grid == self.free:
                    print('□', end = " ")
                elif grid == self.white:
                    print('●', end = " ")
                elif grid == self.black:
                    print('○', end = " ")
            print()                

    def checkIN(self,IN):
        #INが空でないか確認
        if not IN:
            return False
        #x軸が a～h,  ｙ軸が1～８ の範囲で正しく入力確認 　（例）ｂ６：
        if IN[0] in IN_ALPHABET:
            if IN[1] in IN_NUMBER:
                return True
        return False
    
    def computer(self):
              #おけるマスがない時はパスなのでFalseを返す
        if board.skip == True:
            return False
        
        #Movableposの情報を入れる、置けるマスは 
        grids = np.where(self.MovablePos == 1)
        
        #置けるマス[0]をランダムに選ぶ  lenで指定の要素のある範囲のみを選択肢にしている
        random_chosen_index= random.randrange(len(grids[0])) 
        
        x_line = grids[0][random_chosen_index]
        y_line = grids[1][random_chosen_index]
        
        #選んだマスの座標を返す
        return IN_ALPHABET[x_line-1] + IN_NUMBER[y_line-1] 

#Boardインスタンスの作成

'''
#テスト、パス動作確認用 #e7に置くと必ずパスになる
board.Square_Board= np.array([
    [2, 2, 2, 2, 2, 2, 2, 2, 2,2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1,2],
    [2, 1, 1,-1,-1, 1, 1, 1, 1,2],
    [2, 1, 1,-1,-1,-1, 1,-1, 1,2],
    [2, 1, 1, 1,-1, 1, 1, 1, 1,2],
    [2, 1, 1,-1, 1,-1,-1, 0, 1,2],
    [2, 1,-1, 1, 1, 1, 1, 1, 1,2],
    [2, 1, 0,-1,-1,-1,-1, 1, 1,2],
    [2, 1, 0, 0, 0, 0,-1, 1, 1,2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2,2] ])
board.initMovable()
'''

board = Board()    
    