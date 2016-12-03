from datetime import timedelta
from flask import current_app, jsonify,g,session
from flask_login import user_logged_out
from flask_security import url_for_security

from app import  app
from flask import render_template, redirect, request, flash, url_for, abort
import logging as log
from app.views.pages import post_get
from app.util import exceptions


@user_logged_out.connect_via(app)
def logoutSignalHandler(sender,user):
    session['login_retry']=0
@app.context_processor
def inject_global_args():
    return app.config['G_SHARE']

@app.before_request
def before_reuquest():
    #flask sessions expire once you close the browser unless you have a permanent session
    session.permanent = True
    #By default in Flask, permanent_session_lifetime is set to 31 days.
    app.permanent_session_lifetime = timedelta(minutes=30)

    max_login_retry=5
    if (not getattr(g.identity,'user',None)) and request.path==url_for_security('login'):
        login_retry=session.get('login_retry',0)+1
        session['login_retry'] = login_retry
        if login_retry>max_login_retry:
            return render_template('hintInfo.html',msg='登录次数超出限制,请2小时后重试')
    ip=request.headers['X-Real-IP'] or request.headers['Remote_Addr']
    log.info(ip+" enter into "+request.path or ''+" for "+request.endpoint or ''+" of http method:"+request.method)

@app.errorhandler(exceptions.ArgsErrorException)
def argsErrorHandle(e):
    if request.is_xhr:
        return jsonify({'status':'fail','msg':e.msg})
    flash(e.msg,'danger')
    return render_template('hintInfo.html')

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    # flash('这是首页', 'success')
    return post_get('home')
    #return render_template('home.html', title="xbynet平台首页")
