import sympy
import PySimpleGUI as sg
#sympy setting
sympy.init_printing()

class make_matrix:
    def __init__(self,line,column):
        self.line=line
        self.col=column
        #line,columnのゼロ行列作成
        self.mat=sympy.zeros(self.line,self.col)
        # self.layoutにmatrix elem入力用のlayout追加
        self.input_layout=[]
        self.input_mat_layout()
        #print用のmatrix layout(get_elemの実行と同時に作成）
        self.pri_mat_layout=[]


    def input_mat_layout(self):
        for line in range(self.line):
            line_list=[]
            for col in range(self.col):
                line_list.append(sg.Text(f'a{line+1}{col+1}'))
                line_list.append(sg.InputText(size=(15,40),key=f"a{line+1}{col+1}"))#行のlayout設定
            self.input_layout.append(line_list)#インスタンスにlayoutとして追加
    #while文内で実行する必要あり？
    def get_elem(self):
        for line in range(self.line):
            line_list=[]
            for col in range(self.col):
                value=values[f"a{line+1}{col+1}"]
                self.mat[line,col]=value
                value_text=sg.Text(value)
                line_list.append(value_text)
            self.pri_mat_layout.append(line_list)


##################################### try ##################################
data=make_matrix(2,2)

window_layout=[data.input_layout,[sg.Button("get",key="get")],data.pri_mat_layout]
############################################################################
#GUI settings


window = sg.Window("My Window", window_layout,resizable=True)


#表示
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "get":
        data.get_elem()
        window_layout=[data.pri_mat_layout]

window.close()
#TODO 他のファイルとのやり取りで実装する．mainの画面から値を出すwindowを新しく表示する


# sympy.var("a b x y")
# f=sympy.exp(x)*sympy.cos(x)
# i=sympy.integrate(f,(x,a,b))
# i=sympy.simplify(i)
# i=str(i)
# i=i.replace('*','×')
# i=i.replace('sqrt','√')
# i=i.replace('pi','π')

