# coding=utf-8
# @Author: 莫冉
# @Date: 2021-02-26
from apps.main import app, OutlineApp

outline_app = OutlineApp()

app.add_url_rule("/", view_func=outline_app.index)
app.add_url_rule("/index", view_func=outline_app.index)
app.add_url_rule("/init", view_func=outline_app.init_model, methods=["POST"])
app.add_url_rule("/analysis", view_func=outline_app.analysis, methods=["POST"])