import tkinter as tk
from tkinter import messagebox
import sympy
import re

main_win = tk.Tk()
main_win.title("Main Window")
main_win.geometry('1200x600')

# img set
# 後で参照するための画像保持
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
        print('from matrix class "self.mat" is', self.mat)

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
    val = 0
    for row in range(row_):
        for col in range(col_):
            cha = mat[row, col]
            cha = str(cha)
            cha = list(cha)
            if val < len(cha):
                val = len(cha)
    # print('val is',val)
    return val


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
        num = mat_cha_check(ans_mat, ans_row, ans_col)
        ans_wid = ans_col * (num + 100) + 300
        ans_hei = ans_row * (30 + 10) + 300

        super().__init__(root, width=ans_wid, height=ans_hei, borderwidth=4, relief='groove')
        self.pack(side='right', anchor=tk.NW)

    # 行列の表示
    def print_ans_mat(self, ans, row_, col_):
        mat_elem_wid = mat_cha_check(ans, row_, col_) * 10
        # 行列の要素を簡単にする
        ans = mat_elem_ease(ans, row_, col_)

        for row in range(row_):
            for col in range(col_):
                mat_text = tk.Message(self, font=("", 15), width=mat_elem_wid,
                                      text=f'{ans[row][col]}', bg='lightblue')
                # 行列要素位置
                elem_x = col * (mat_elem_wid + 30)
                elem_y = row * (30 + 10)
                # 行列要素位置指定
                mat_text.place(x=elem_x, y=elem_y)


##########################################################
# 行列計算のボタン
##########################################################

class calcButton(tk.Frame):
    def __init__(self, root, mat):
        # matはmatrix class
        self.mat = mat
        self.root = root
        super().__init__(root, width=1200, height=70, borderwidth=4, relief='groove')
        self.pack(side='bottom')
        self.pack_propagate(0)
        self.create_widgets()

        # すでに表示されているものがあるのかの判定
        self.pri_flag = 0

    def create_widgets(self):
        # 転置計算
        self.cal_trans = tk.Button(self, text='転置', font=("", 15),
                                   width=10, height=50, command=self.calc_transpose)
        self.cal_trans.pack(side='left', padx=10, pady=10)

        #定数倍
        self.cal_cons_entry = tk.Entry(self, width=8)
        self.cal_cons_entry.pack(side='left')
        self.cal_cons = tk.Button(self, text='倍を計算', font=("", 15),
                                   width=10, height=50, command=self.calc_cons)
        self.cal_cons.pack(side='left', padx=5, pady=10)

        # 累乗
        self.cal_power_entry = tk.Entry(self,width=8)
        self.cal_power_entry.pack(side='left')
        self.cal_power = tk.Button(self, text='乗を計算', font=("", 15),
                                   width=10, height=50, command=self.calc_power)
        self.cal_power.pack(side='left', padx=5, pady=10)

        #余因子行列
        self.cal_adj = tk.Button(self, text='余因子行列', font=("", 15),
                                 width=10, height=50, command=self.calc_adj)
        self.cal_adj.pack(side='left', padx=10, pady=10)

        #逆行列
        self.cal_inv = tk.Button(self, text='逆行列', font=("", 15),
                                   width=10, height=50, command=self.calc_inv)
        self.cal_inv.pack(side='left', padx=10, pady=10)

        #対角化
        self.cal_dia = tk.Button(self, text='対角化', font=("", 15),
                                 width=10, height=50, command=self.calc_dia)
        self.cal_dia.pack(side='left', padx=10, pady=10)

        #正則行列
        self.cal_sei = tk.Button(self, text='正則行列', font=("", 15),
                                 width=10, height=50, command=self.calc_sei)
        self.cal_sei.pack(side='left', padx=10, pady=10)



    # 転置
    def calc_transpose(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        m_mat = self.mat
        m_mat.get_elem()
        # 転置だから行と列の数は逆
        ans = m_mat.mat.transpose()
        row = m_mat.col
        col = m_mat.row
        print('Transposed ',ans)
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
        row = m_mat.row
        col = m_mat.col
        print(f'{cons} * mat is', ans)
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
        row = m_mat.row
        col = m_mat.col
        print(f'power of {power} is', ans)
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
        # 余因子行列だから行と列の数は逆
        ans = m_mat.mat.adjugate()
        #eigenvalsは辞書式配列で帰ってくるからsortedでキー名(固有値)のみ取得する
        ans_zisyo=m_mat.mat.eigenvals()
        self.ans_koyuti=sorted(ans_zisyo)#sorted()はlistで返す
        #対角行列なので行・列は同じ
        row = m_mat.row
        col = m_mat.col
        print('Adjugate mat is ', ans)
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

    #逆行列
    def calc_inv(self):
        # matrix classのmat → m_mat
        # このm_matで計算可能
        m_mat = self.mat
        m_mat.get_elem()
        # 逆行列だから行と列の数は同じ
        if m_mat.mat.det()==0:
            messagebox.showerror('Calculation Error', '行列式が0のため計算できません．')
        ans = m_mat.mat.inv()
        row = m_mat.row
        col = m_mat.col
        print('Inversed is ', ans)
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
        row = m_mat.col
        col = m_mat.row
        print('Transposed ', ans)
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
        row = m_mat.col
        col = m_mat.row
        print('Transposed ', ans)
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

main = matrix(main_win)
buttons = calcButton(main_win, main)

main.mainloop()
