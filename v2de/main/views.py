from . import main
from flask import render_template

@main.route('/')
def index():
    type_list = ['技术','好玩','Apple','酷工作','交易','城市','问答','全部']
    node_list = ['程序员','Python','iDev','Android','Linux','node.js','云计算','宽带症候群']
    return render_template('index.html',type_list=type_list,node_list=node_list)