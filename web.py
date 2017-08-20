#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from flask import Flask, session, redirect, abort
from flask import request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from NewTransaction import getResult
from Random import getRandomData
from DataVisi import getRatingData
from DataVisi import getLikeData
from DataVisi import getPlayData 
from math import ceil
import datetime

app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

PER_PAGE = 10

class QueryForm(FlaskForm):
    query = StringField('', [validators.Length(min=1)])
    submit = SubmitField('Vikino')
    content = TextAreaField("Text Area")

class RandomButton(FlaskForm):
    submit = SubmitField('λ')

class DataVisualization(FlaskForm):
    submit = SubmitField('回到主页')
                                                                                                                                                    
class Pagination(object):
    def __init__(self, page, per_page, total_count, rank, channel, year, duration):
        self.page = page
        self.rank = rank
        self.channel = channel
        self.year = year
        self.duration = duration
        self.per_page = per_page
        self.total_count = total_count
    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))
    @property
    def has_prev(self):
        return self.page > 1
    @property
    def has_next(self):
        return self.page < self.pages
    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
                                                                                                            
def url_for_other_page(page, rank, channel, year, duration):
    args = request.view_args.copy()
    args['page'] = page
    args['rank'] = rank
    args['channel'] = channel
    args['year'] = year
    args['duration'] = duration
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page
                                                                                                                                            
@app.route('/', methods=['GET', 'POST'])
def index():
    query = None
    form = QueryForm()
    rand = RandomButton()
    visidata = DataVisualization()
    if form.validate_on_submit():
        session['query'] = form.query.data
        return redirect(url_for('search'))
    return render_template('index.html', form=form, rand=rand, visidata=visidata, query=query)

@app.route('/search/', methods=['GET', 'POST'], defaults={'page':1, 'rank':1, 'channel':1, 'year':0, 'duration':1})
@app.route('/search/page/<int:page>', defaults={'rank':1, 'channel':1, 'year':0, 'duration':1}, methods=['GET', 'POST'])
@app.route('/search/page/<int:page>/rank/<int:rank>', defaults={'channel':1, 'year':0, 'duration':1}, methods=['GET', 'POST'])
@app.route('/search/page/<int:page>/rank/<int:rank>/channel/<int:channel>', defaults={'year':0, 'duration':1}, methods=['GET', 'POST'])
@app.route('/search/page/<int:page>/rank/<int:rank>/channel/<int:channel>/year/<int:year>', defaults={'duration':1}, methods=['GET', 'POST'])
@app.route('/search/page/<int:page>/rank/<int:rank>/channel/<int:channel>/year/<int:year>/duration/<int:duration>', methods=['GET', 'POST'])
def search(page, rank, channel, year, duration):
    # get init time
    start_time = datetime.datetime.now()
    form = QueryForm()
    if form.validate_on_submit():
        session['query'] = form.query.data
        # cut query if it's too long
        if len(session['query']) > 50:
            query = session['query'][0:50]
            isLong = True
        else:
            query = session['query']
            isLong = False
        # get result data, _list is the term in query
        _list, retv = getResult(query, rank, channel, year, duration)
        page = 1
    else:
        if len(session['query']) > 50:  
            query = session['query'][0:50]
            isLong = True                  
        else:                              
            query = session['query']       
            isLong = False  
        _list, retv = getResult(query, rank, channel, year, duration)
    # get data counts
    count = len(retv)
    if count == 0:
        found = None
    else:
        found=True
    # get data in that page
    data = retv[(page-1)*10:(page)*10]
    # get index
    for i in xrange(len(data)):
        data[i].append(i)
    pagination = Pagination(page, PER_PAGE, count, rank, channel, year, duration)
    # number of key words
    kcount = len(_list)
    # get end time so that time used can be calculated
    end_time = datetime.datetime.now()
    delta_time = float(str(end_time - start_time).split(':')[-1])
    return render_template('search.html', form=form, \
            query=query, posts=data, pagination=pagination,\
            found=found, _list=_list, count=count, kcount=kcount,\
            delta_time = delta_time, isLong=isLong)        

@app.route('/random', methods=['GET', 'POST'])
def rand():
    rand = RandomButton()
    if rand.validate_on_submit():
        pass
    data = getRandomData()
    for i in xrange(len(data)):
        data[i].append(i) 
    return render_template('random.html', rand=rand, posts=data)

@app.route('/datavisualization', methods=['GET', 'POST'])
def visidata():
    # button
    visidata = DataVisualization()
    if visidata.is_submitted():
        return redirect(url_for('index'))
    data = []
    data.append(getRatingData())
    data.append(getLikeData())
    data.append(getPlayData())
    return render_template('visidata.html', visidata=visidata, posts=data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
                                                                                                                    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
#    app.run(debug=True)
