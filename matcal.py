import PySimpleGUI as sg

layout1=[[sg.Text("hello")],[sg.Button("get", key="get")]]
layout2=[[sg.Text("hello")],[sg.Button("get", key="get")]]
while True:
    window = sg.Window("My Window",layout1, resizable=True)
    event, values = window.read()
    if event == "get":
        window = sg.Window("print",layout2)
        event, values = window.read()
