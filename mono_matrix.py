import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import sympy
import re

main_win = tk.Tk()
main_win.title("Main Window")
main_win.geometry('1200x600')

# img set
# 後で参照するための画像保持
if getattr(sys, 'frozen', False):
    # 実行ファイルからの実行時
    script_dir = sys._MEIPASS
else:
    # スクリプトからの実行時
    script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "sample.csv")

img_up = tk.PhotoImage(file='./img/up.png')
img_down = tk.PhotoImage(file='./img/down.png')
img_right = tk.PhotoImage(file='./img/right.png')
img_left = tk.PhotoImage(file='./img/left.png')


##########################################################
# 計算する行列を作成するクラス
##########################################################
class matrix(tk.Frame):
    def __init__(self, root):
        # rootの取得
        self.root = root

        # defalutは3x3
        self.row = 2
        self.col = 2

        # 行列要素のEntry要素の大きさ
        self.entry_x = 100
        self.entry_y = 30
        # 行列の要素間の大きさ指定
        self.x_adj = 10
        self.y_adj = 10

        # 行列自体のwindow上での大きさ指定
        self.mat_wid = self.col * (100 + self.x_adj) - self.x_adj
        self.mat_hei = self.row * (30 + self.y_adj) - self.y_adj

        # イニシャライザを呼び，行列の大きさを決定，作成
        super().__init__(root, width=self.mat_wid, height=self.mat_hei)

        # 行列自体の位置
        self.mat_posi_x = 10
        self.mat_posi_y = 10
        self.place(x=self.mat_posi_x, y=self.mat_posi_y)

        # 行列を表示する関数
        self.create_mat()

        # buttonの位置計算
        self.cal_but_posi()
        # buttonの作成
        self.create_set_button()

    def cal_but_posi(self):
        self.but_wid = self.mat_posi_x
        self.but_hei = self.row * (30 + self.y_adj) + self.mat_posi_y

    def create_mat(self):
        self.tk_mat = []
        row_ = self.row
        col_ = self.col
        for row in range(row_):
            mat_row_list = []
            for col in range(col_):
                mat_test = None
                mat_test = tk.Entry(main_win, font=("", 15), bg='lightblue')
                # 行列要素位置
                elem_x = col * (100 + self.x_adj) + self.mat_posi_x
                elem_y = row * (30 + self.y_adj) + self.mat_posi_y
                # 行列要素位置指定
                mat_test.place(x=elem_x, y=elem_y, width=self.entry_x, height=self.entry_y)
                mat_row_list.append(mat_test)
            self.tk_mat.append(mat_row_list)

    def mat_row_up(self):
        # すべてのentryを一度destroy
        for row in range(self.row):
            for col in range(self.col):
                self.tk_mat[row][col].destroy()
        self.row = self.row - 1
        self.create_mat()
        # print('row is', self.row)
        # buttonリセット，セット
        self.up.destroy()
        self.down.destroy()
        self.right.destroy()
        self.left.destroy()

        # matrix width height recalculate
        self.cal_but_posi()
        self.create_set_button()

    def mat_row_down(self):
        # すべてのentryを一度destroy
        for row in range(self.row):
            for col in range(self.col):
                self.tk_mat[row][col].destroy()
        self.row = self.row + 1
        self.create_mat()
        # print('row is', self.row)
        # buttonリセット，セット
        self.up.destroy()
        self.down.destroy()
        self.right.destroy()
        self.left.destroy()

        # matrix width height recalculate
        self.cal_but_posi()
        self.create_set_button()

    def mat_col_up(self):
        # すべてのentryを一度destroy
        for row in range(self.row):
            for col in range(self.col):
                self.tk_mat[row][col].destroy()
        self.col = self.col + 1
        self.create_mat()
        # print('col is', self.col)

    def mat_col_down(self):
        # すべてのentryを一度destroy
        for row in range(self.row):
            for col in range(self.col):
                self.tk_mat[row][col].destroy()
        self.col = self.col - 1
        self.create_mat()
        # print('col is', self.col)

    # Entry内の入力された値をself.matに格納
    def get_elem(self):
        self.mat = sympy.zeros(self.row, self.col)
        for row in range(self.row):
            for col in range(self.col):
                self.mat[row, col] = self.tk_mat[row][col].get()
        # print('from matrix class "self.mat" is', self.mat)

    # 行列操作ボタン
    def create_set_button(self):
        self.left = tk.Button(self.root, image=img_left, command=self.mat_col_down)
        self.left.place(x=self.but_wid, y=self.but_hei)

        self.up = tk.Button(self.root, image=img_up, command=self.mat_row_up)
        self.up.place(x=self.but_wid + 80, y=self.but_hei)

        self.down = tk.Button(self.root, image=img_down, command=self.mat_row_down)
        self.down.place(x=self.but_wid + 160, y=self.but_hei)

        self.right = tk.Button(self.root, image=img_right, command=self.mat_col_up)
        self.right.place(x=self.but_wid + 240, y=self.but_hei)


##########################################################
# 答えを表示するためのクラス
##########################################################

# 行列内の最大文字列数を確認する関数
def mat_cha_check(mat, row_, col_):
    val = []
    for col in range(col_):
        max = 0
        #列ごとに最大文字数？を計算
        for row in range(row_):
            mat_value=mat[row,col]
            mat_val_str=str(mat_value)
            mat_val_list=list(mat_val_str)
            mat_val_len=len(mat_val_list)
            if max < mat_val_len:
                max=mat_val_len
        #列ごとの最大文字数をvalに格納
        val.append(max)


    # print('val is', val)


    return val

def mat_cha_check_for_list(mat, row_, col_):
    val = []
    for col in range(col_):
        max = 0
        #列ごとに最大文字数？を計算
        for row in range(row_):
            mat_value=mat[row][col]
            mat_val_str=str(mat_value)
            # print('文字は',mat_val_str)
            mat_val_list=list(mat_val_str)
            mat_val_len=len(mat_val_list)
            # print('長さは',mat_val_len)
            # print(row,col,'は',mat_val_len,'が文字数')
            if max < mat_val_len:
                max=mat_val_len
        # print('max is',max)
        #列ごとの最大文字数をvalに格納
        val.append(max)
        # print(f'{col}列目の最大文字数は',max)

    return val

#行列内の要素を見やすくする
def mat_elem_ease(mat, row_, col_):
    return_mat = []
    for row in range(row_):
        row_list = []
        for col in range(col_):
            value = str(mat[row, col])
            value = value.replace(' ', '')
            value = value.replace('**', '^')
            value = value.replace('*', '')
            value=value.replace('sqrt','√')
            row_list.append(value)
        return_mat.append(row_list)

    return return_mat


class print_ans(tk.Frame):
    def __init__(self, root, mat):
        # matはmatrixクラス
        self.c_mat = mat
        self.root = root
        # Frameの大きさを決める
        ans_mat = self.c_mat.mat
        ans_row = self.c_mat.row
        ans_col = self.c_mat.col
        #行列の答えを表示する幅，高さを決める
        #mat_cha_checkで列ごとの最大文字数のlistがかえてっくる
        max_col_cha= mat_cha_check(ans_mat, ans_row, ans_col)#list
        # print('列ごとの最大文字数のlistは',max_col_cha)
        #列ごとの最大文字数の幅を考慮した行列表示幅の計算
        ans_wid=0
        for i in range(len(max_col_cha)):
            length=max_col_cha[i]
            ans_wid=ans_wid+length*20#列ごとの最大文字数分の幅を加算
        ans_wid=ans_wid+len(max_col_cha)*40+(len(max_col_cha)+1)*15#行列要素の横幅20+20=40・行列要素の間隔(列数+1)*10
        ans_hei = ans_row * (30 + 10) + 300
        super().__init__(root, width=ans_wid, height=ans_hei, borderwidth=4, relief='groove')
        self.pack(side='right', anchor=tk.NW)

    # 行列の表示
    def print_ans_mat(self, ans, row_, col_):
        # 行列の要素を簡単にする
        ans = mat_elem_ease(ans, row_, col_)
        # print('表示したい答えは',ans)
        #実際に行列を配置する
        #列ごとに並べることにする．各列の最大文字数によって行列の列の幅を調整するため
        mat_col_cha_len_list= mat_cha_check_for_list(ans, row_, col_)
        col_position=0
        for col in range(col_):
            #列の最大文字列を格納
            #文字の位置は前の列の最後の位置を参照しなくてはいけない．一つ前の列の文字の最後の位置を計算して次の列の位置を計算する
            pri_col_cha_length=mat_col_cha_len_list[col]*15# 文字数×文字の横幅
            # print(f'{col}列目の表示したい最大文字数は is',mat_col_cha_len_list[col])
            # print('表示したい横幅は',pri_col_cha_length)

            for row in range(row_):
                mat_text = tk.Message(self, font=("", 15), width=pri_col_cha_length,
                                      text=f'{ans[row][col]}', bg='lightgreen')
                # 行列要素位置
                elem_x = col_position
                # print('表示位置は',elem_x)
                elem_y = row * (30 + 10)#文字の高さ分+行の間の隙間
                # 行列要素位置指定
                mat_text.place(x=elem_x, y=elem_y)
            #col_positionに表示した列の位置を足していく
            col_position=col_position+pri_col_cha_length+20#50は列同士の間隔





    def print_ans_koyuti(self,koyuti):
        self.pri_koyuti=koyuti
        self.pri_ans_koyu = tk.Label(self, text='固有値: ' + self.pri_koyuti)
        self.pri_ans_koyu.pack(side='bottom')
        self.pack_propagate(0)#オブジェクトサイズ指定

    def print_ans_det(self,det):
        self.det= det
        self.pri_ans_det = tk.Label(self, font=("", 12),text='行列式: ' + f'{self.det}')
        self.pri_ans_det.pack(side='bottom')
        self.pack_propagate(0)  # オブジェクトサイズ指定


##########################################################
# 行列計算のボタン
##########################################################
#listで帰ってくる固有値を表示するための文字列にする関数
def list_to_pri(koyuti_list):
    result=[]
    for i in range(len(koyuti_list)):
        value=str(koyuti_list[i])
        result.append(f'{i+1}個目')
        result.append(value)
        result.append(' ')
    result=' '.join(result)
    return result

def char_ease(char):
    result=char
    result=result.replace('**','^')
    result=result.replace('*','')
    result=result.replace('sqrt','√')
    return result

class calcButton(tk.Frame):
    def __init__(self, root, mat):
        # matはmatrix class
        self.mat = mat
        self.root = root
        self.mat_ans=[]
        super().__init__(root, width=1200, height=70, borderwidth=4, relief='groove')
        self.pack(side='bottom')
        self.pack_propagate(0)
        self.create_widgets()

        #行列式の再表示に使う
        self.det=None
        # すでに表示されているものがあるのかの判定
        self.pri_flag = 0

    def create_widgets(self):
        # 転置計算
        self.cal_trans = tk.Button(self, text='転置', font=("", 15),
                                   width=8, height=50, command=self.calc_transpose)
        self.cal_trans.pack(side='left', padx=5, pady=10)

        #定数倍
        self.cal_cons_entry = tk.Entry(self, width=8)
        self.cal_cons_entry.pack(side='left')
        self.cal_cons = tk.Button(self, text='倍を計算', font=("", 15),
                                   width=8, height=50, command=self.calc_cons)
        self.cal_cons.pack(side='left', padx=5, pady=10)

        # 累乗
        self.cal_power_entry = tk.Entry(self,width=8)
        self.cal_power_entry.pack(side='left')
        self.cal_power = tk.Button(self, text='乗を計算', font=("", 15),
                                   width=8, height=50, command=self.calc_power)
        self.cal_power.pack(side='left', padx=5, pady=10)

        #余因子行列
        self.cal_adj = tk.Button(self, text='余因子行列', font=("", 15),
                                 width=10, height=50, command=self.calc_adj)
        self.cal_adj.pack(side='left', padx=10, pady=10)

        #行列式
        self.cal_det = tk.Button(self, text='行列式', font=("", 15),
                                   width=8, height=50, command=self.calc_det)
        self.cal_det.pack(side='left', padx=5, pady=10)

        #逆行列
        self.cal_inv = tk.Button(self, text='逆行列', font=("", 15),
                                   width=8, height=50, command=self.calc_inv)
        self.cal_inv.pack(side='left', padx=10, pady=10)

        #対角化
        self.cal_dia = tk.Button(self, text='対角化', font=("", 15),
                                 width=8, height=50, command=self.calc_dia)
        self.cal_dia.pack(side='left', padx=10, pady=10)

        #正則行列
        self.cal_sei = tk.Button(self, text='正則行列', font=("", 15),
                                 width=8, height=50, command=self.calc_sei)
        self.cal_sei.pack(side='left', padx=10, pady=10)

        #行列がうまく表示されないときのボタン
        self.re_print = tk.Button(self.root, text='別ウィンドウで答えを表示', font=("", 15), command=self.re_print_mat)
        self.re_print.pack(side='bottom', padx=10, pady=10,anchor=tk.SE)


    # 転置
    def calc_transpose(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        m_mat = self.mat
        m_mat.get_elem()
        # 転置だから行と列の数は逆
        ans = m_mat.mat.transpose()
        self.mat_ans=ans
        row = m_mat.col
        col = m_mat.row
        # print('Transposed ',ans)
        # 表示するためのクラスを作成
        # ただし，すでに表示しているものがあれば一度destroy()する
        if self.pri_flag == 0:
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)
            self.pri_flag = 1
        elif self.pri_flag == 1:
            self.print_answer.destroy()
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)

    #定数倍
    def calc_cons(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        m_mat = self.mat
        m_mat.get_elem()
        num=self.cal_cons_entry.get()
        num=float(num)
        #整数倍の時，intにする
        if num.is_integer():
            cons=int(num)
        else:
            cons=num
        # 定数倍だから行と列の数はそのまま
        ans = m_mat.mat*cons
        self.mat_ans=ans
        row = m_mat.row
        col = m_mat.col
        # print(f'{cons} * mat is', ans)
        # 表示するためのクラスを作成
        # ただし，すでに表示しているものがあれば一度destroy()する
        if self.pri_flag == 0:
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)
            self.pri_flag = 1
        elif self.pri_flag == 1:
            self.print_answer.destroy()
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)

    # 累乗計算
    def calc_power(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        m_mat = self.mat
        m_mat.get_elem()
        power=self.cal_power_entry.get()
        # 累乗だから行と列の数はそのまま
        ans = m_mat.mat**power
        self.mat_ans=ans
        row = m_mat.row
        col = m_mat.col
        # print(f'power of {power} is', ans)
        # 表示するためのクラスを作成
        # ただし，すでに表示しているものがあれば一度destroy()する
        if self.pri_flag == 0:
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)
            self.pri_flag = 1
        elif self.pri_flag == 1:
            self.print_answer.destroy()
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)

    #余因子行列
    def calc_adj(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        m_mat = self.mat
        m_mat.get_elem()
        # 余因子行列だから行と列の数は同じ
        ans = m_mat.mat.adjugate()
        self.mat_ans=ans
        row = m_mat.row
        col = m_mat.col
        # print('Adjugate mat is ', ans)
        # 表示するためのクラスを作成
        # ただし，すでに表示しているものがあれば一度destroy()する
        if self.pri_flag == 0:
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)
            self.pri_flag = 1
        elif self.pri_flag == 1:
            self.print_answer.destroy()
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)

    #行列式
    def calc_det(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        m_mat = self.mat
        m_mat.get_elem()
        ans=m_mat.mat.det()
        self.det=ans
        #簡単にする
        ans=str(ans)
        ans=char_ease(ans)
        # print('Det of mat is ', ans)
        # 表示するためのクラスを作成
        # ただし，すでに表示しているものがあれば一度destroy()する
        if self.pri_flag == 0:
            self.print_answer = print_ans(self.root, m_mat)
            # self.print_answer.print_ans_mat(ans, row, col)
            self.print_answer.print_ans_det(ans)
            self.pri_flag = 1
        elif self.pri_flag == 1:
            self.print_answer.destroy()
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_det(ans)

            # self.print_answer.print_ans_mat(ans, row, col)


    #逆行列
    def calc_inv(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        m_mat = self.mat
        m_mat.get_elem()
        # 逆行列だから行と列の数は同じ
        if m_mat.mat.shape[0]!=m_mat.mat.shape[1]:
            messagebox.showerror('Calculation Error', '正方行列でないため計算できません．')
        if m_mat.mat.det()==0:
            messagebox.showerror('Calculation Error', '行列式が0のため計算できません．')
        ans = m_mat.mat.inv()
        self.mat_ans=ans
        row = m_mat.row
        col = m_mat.col
        # print('Inversed is ', ans)
        # 表示するためのクラスを作成
        # ただし，すでに表示しているものがあれば一度destroy()する
        if self.pri_flag == 0:
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)
            self.pri_flag = 1

        elif self.pri_flag == 1:
            self.print_answer.destroy()
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)


    #対角化
    def calc_dia(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        m_mat = self.mat
        m_mat.get_elem()
        # 対角化だから行と列の数は逆
        ans = m_mat.mat.diagonalize()
        #diagonolize()では(P,D)で帰ってくるPDP**(-1)
        #だからans[1]を渡す
        ans=ans[1]
        self.mat_ans=ans
        row = m_mat.row
        col = m_mat.col
        # eigenvalsは辞書式配列で帰ってくるからsortedでキー名(固有値)のみ取得する
        ans_zisyo = m_mat.mat.eigenvals()
        ans_koyuti = sorted(ans_zisyo)  # sorted()はlistで返す
        # 固有値のlistを表示するための文字列に直す
        koyuti_char = list_to_pri(ans_koyuti)
        #固有値の文字列を簡単にする
        self.pri_koyuti=char_ease(koyuti_char)

        # print('Diagonalized is ', ans)
        # print('Koyuti is ',self.pri_koyuti)
        # 表示するためのクラスを作成
        # ただし，すでに表示しているものがあれば一度destroy()する
        if self.pri_flag == 0:
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)
            # 固有値をprint_ansowerウィジェットの下部に配置する
            self.print_answer.print_ans_koyuti(self.pri_koyuti)

            self.pri_flag = 1
        elif self.pri_flag == 1:
            self.print_answer.destroy()
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)
            # 固有値をprint_ansowerウィジェットの下部に配置する
            self.print_answer.print_ans_koyuti(self.pri_koyuti)

    #正則行列
    def calc_sei(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        m_mat = self.mat
        m_mat.get_elem()
        # 対角化だから行と列の数は逆
        ans = m_mat.mat.diagonalize()
        # diagonolize()では(P,D)で帰ってくるPDP**(-1)
        # だからans[1]を渡す
        ans = ans[0]
        self.mat_ans=ans
        row = m_mat.col
        col = m_mat.row
        # print('Transposed ', ans)
        # 表示するためのクラスを作成
        # ただし，すでに表示しているものがあれば一度destroy()する
        if self.pri_flag == 0:
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)
            self.pri_flag = 1
        elif self.pri_flag == 1:
            self.print_answer.destroy()
            self.print_answer = print_ans(self.root, m_mat)
            self.print_answer.print_ans_mat(ans, row, col)

    #行列がうまく表示されないときの関数
    def re_print_mat(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        ans = self.mat_ans
        # 行数，列数を取得
        row_ = ans.shape[0]
        col_ = ans.shape[1]

        # print('re_print ans is', ans)
        #新しいウィンドウで表示する処理
        re_print_window = tk.Tk()
        re_print_window.title("Reprinted Window")

        #reprint_matにpymatrixからlistとしてansを格納
        reprint_mat=ans.tolist()
        #reprint_matを簡単にする
        reprint_mat=remat_elem_ease(reprint_mat)
        # for row in range(row_):
        #     re_print_row=tk.Label(re_print_window,text=reprint_mat[row],font=("", 15))
        #     re_print_row.pack(side='top', padx=5, pady=5)

        for row in range(row_):
            reprint_row=reprint(re_print_window,reprint_mat[row])
        # print('reprint_mat is',reprint_mat)
        re_print_window.pack_propagate(0)  # オブジェクトサイズ指定
        re_print_window.mainloop()

#行列の再表示するときのクラス
class reprint(tk.Frame):
    def __init__(self, root, row):
        # matはmatrix class
        self.row=row
        super().__init__(root)
        self.pack(side='top')

        for row_len in range(len(self.row)):
            row_val=tk.Label(self,text=self.row[row_len],font=("",15),background='lightgreen')
            row_val.pack(side='left',padx=5,pady=5)


#再表示する行列を簡単にする関数
def remat_elem_ease(mat):
    row_=len(mat)
    col_=len(mat[0])
    return_remat = []
    for row in range(row_):
        row_list = []
        for col in range(col_):
            value = str(mat[row][col])
            value = value.replace(' ', '')
            value = value.replace('**', '^')
            value = value.replace('*', '')
            value=value.replace('sqrt','√')
            row_list.append(value)
        return_remat.append(row_list)

    return return_remat

##########################################################
#   注意書き
##########################################################
class caution(tk.Frame):
    def __init__(self, root):
        # matはmatrix class
        super().__init__(root)
        self.pack(side='bottom',anchor=tk.SW)
        text1 = tk.Label(self, text="!!CAUTION!!", font=("Helvetica", 15), background='yellow')
        text1.pack(side='top', padx=5,anchor=tk.NW)
        text2 = tk.Label(self, text="・行列を拡大した際に表示が他と被った場合にはウィンドウのサイズを調整してください．", font=("", 12))
        text2.pack(side='top', padx=5,anchor=tk.NW)
        text2 = tk.Label(self, text="・文字を含んだ計算をする際には演算記号(+,-,*,/,^)を忘れずつけてください．", font=("", 12))
        text2.pack(side='top', padx=5, anchor=tk.NW)
        text3 = tk.Label(self, text="・回答となる行列がうまく表示されないときは右の「別ウィンドで答えを表示」を使ってください．", font=("", 12))
        text3.pack(side='top', padx=5,anchor=tk.NW)
        text4 = tk.Label(self, text="・下の演算ボタンを押しても変化がない場合はエラーです．", font=("", 12))
        text4.pack(side='top', padx=5,anchor=tk.NW)




main = matrix(main_win)
buttons = calcButton(main_win, main)
cautions=caution(main_win)

main.mainloop()




