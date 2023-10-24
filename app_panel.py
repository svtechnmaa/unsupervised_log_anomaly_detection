import hvplot.pandas
import numpy as np
import panel as pn
import pandas as pd
import os
import datetime as dt
import altair as alt
import preprocessing
import BASE_LOG_ANALYSE
import nltk
import asyncio
from multiprocess import Pool
from functools import partial
pn.extension('vega')
pn.extension('tabulator')
alt.data_transformers.disable_max_rows()
nltk.download('wordnet')
from elasticsearch import Elasticsearch
import mysql.connector
from datasource import es_connection, ticket_db
import urllib3
urllib3.disable_warnings()
from pattern_dict import pattern_dict


data = dict()
entropy = dict()
vectorizer = None

# Core function
async def load_data_log_entity(folder, entity_name, hostname):
    data1 = {'timestamp': [], 'message': []}
    for filename in BASE_LOG_ANALYSE.get_file_list_by_filename_filter(folder, entity_name):
        # Get file content - Start
        if '.gz' in filename:
            content = BASE_LOG_ANALYSE.read_gzip_file(filename)
        elif 'pfe' in filename:
            pass
        else:
            with open(filename, 'r', encoding="latin-1") as f_in:
                content = f_in.read()
        # Get file content - End
        # Parsing data to get time and info - Start
        if 'messages' in filename:
            for line in content.split('\n'):
                tokens = line.split(hostname)
                if "logfile turned over due" in line:
                    pass
                else:
                    if len(tokens) == 2:
                        if '<' in tokens[0]:
                            tokens[0] = tokens[0].split()[1]
                        data1['timestamp'].append(tokens[0])
                        data1['message'].append(tokens[1])
        elif 'pfe' in filename:
            pass
        else:
            for line in content.split('\n'):
                tokens = line.split(hostname)
                if "logfile turned over due" in line:
                    pass
                else:
                    if len(tokens) == 2:
                        if '<' in tokens[0]:
                            tokens[0] = tokens[0].split()[1]
                        data1['timestamp'].append(tokens[0])
                        data1['message'].append(tokens[1])
        # Parsing data to get time and info - End
    return pd.DataFrame(data1)

async def training_data(folder, start, end, hostname):
    global entropy, vectorizer, data
    try:
        df = await load_data_log_entity(folder, 'messages*', hostname)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', utc=True)
        df = df.dropna(subset=['timestamp'])
        df.sort_values(by=['timestamp'], inplace=True)
        df['timestamp'] = df['timestamp'].dt.tz_convert(None)
        data['message'] = df
        training_data = {k: v[(v['timestamp'] >= start) & (v['timestamp'] < end)].copy(deep=True) for k, v in data.items()}
        entropy, vectorizer = preprocessing.preprocess_training_data(training_data)
        return "Training done!"
    except Exception as e:
        return "Training error due to: {}".format(e)

def inspect_data(start, end):
    global data
    inspect = {k: v[(v['timestamp'] >= start) & (v['timestamp'] < end)] for k, v in data.items()}['message'].copy()
    return inspect

# async def speed_up(time_filter, data, vectorizer, entropy):
#     data_filter = { k: v[(v['timestamp'] >= str(time_filter[0])) & (v['timestamp'] < str(time_filter[1]))] for k, v in data.items() }
#     s = preprocessing.calculate_score(data_filter, vectorizer, entropy)['message']
#     return {'timestamp': time_filter[0].to_timestamp(), 'score': s}

# async def split_chunks_and_calculate_score(data, start, end, vectorizer, entropy, chunk_size='10s'):
#     period = pd.period_range(start=start, end=end, freq=chunk_size)
#     chunks = []
#     for i in range(len(period) - 1):
#         chunks.append(await speed_up([period[i], period[i + 1]], data=data, vectorizer=vectorizer, entropy=entropy))
#     return chunks

def speed_up(time_filter, data, vectorizer, entropy):
    data_filter = { k: v[(v['timestamp'] >= str(time_filter[0])) & (v['timestamp'] < str(time_filter[1]))] for k, v in data.items() }
    return {'timestamp': time_filter[0].to_timestamp(), 'score': preprocessing.calculate_score(data_filter, vectorizer, entropy)['message']}

def speed_up_split(filtered_data, vectorizer, entropy):
    if len(filtered_data[1]) == 0:
        return {'timestamp': filtered_data[0].to_datetime64(), 'score': 0}
    else:
        return {'timestamp': filtered_data[0].to_datetime64(), 'score': preprocessing.calculate_score({'message': filtered_data[1]}, vectorizer, entropy)['message']}

def split_chunks_and_calculate_score(num_core, data, start, end, vectorizer, entropy, chunk_size='10s'):
    # period = pd.period_range(start=start, end=end, freq=chunk_size)
    # input_args = []
    # for i in range(len(period) - 1):
    #     input_args.append([period[i], period[i + 1]])
    testing = data['message'][(data['message']['timestamp'] >= start) & (data['message']['timestamp'] < end)]
    input_args = [[n, g] for n, g in testing.groupby(pd.Grouper(key='timestamp',freq='10s'))]
    pool = Pool(int(num_core))
    chunks = pool.map(partial(speed_up_split, vectorizer=vectorizer, entropy=entropy), input_args)
    pool.close()
    pool.join()
    return chunks

def testing_data(start, end):
    global entropy, vectorizer, data
    score_chunks = split_chunks_and_calculate_score(4, data, start, end, vectorizer, entropy)
    score = pd.DataFrame(score_chunks)
    testing = {k: v[(v['timestamp'] >= start) & (v['timestamp'] < end)] for k, v in data.items()}['message']
    if len(testing) == 0:
        alert.object = "There is no data in testing time"
        alert.param.trigger("object")
    grouped = testing.groupby(pd.Grouper(key='timestamp', axis=0, freq='H')).count()
    grouped = grouped.reset_index()
    grouped.columns = ['timestamp', 'count']
    # testing['timestamp'] = testing['timestamp'].dt.tz_convert(None)
    return score, grouped, testing

def get_path_value():
    query_params = pn.state.session_args
    if 'path' in query_params:
        return query_params['path'][0].decode('utf-8')
    else:
        return ''

def check_kb(folder, start, end, hostname, list_file):
    # Get list file
    list_log_file = []
    for filter_name in list_file:
        list_log_file += BASE_LOG_ANALYSE.get_file_list_by_filename_filter(folder, filter_name)
    
    # Filter file by time
    filter_list_log = []
    for log_file in list_log_file:
        modification_time = os.path.getmtime(log_file)
        if modification_time >= start.timestamp():
            filter_list_log.append(log_file)
    # Check KB
    print("Find KB in: {}".format(filter_list_log))
    pool = Pool(4)
    chunks = pool.map(partial(BASE_LOG_ANALYSE.analysing_log_single_process, host_name=hostname, pattern_dict=pattern_dict), filter_list_log)
    pool.close()
    pool.join()
    return chunks

# UI component
junos_hostname = pn.widgets.TextInput(name="Host name")
alert = pn.pane.Alert("", width=300)
path = pn.widgets.TextAreaInput(name='Log path', placeholder='Enter a string here...', value=os.getcwd(), height=100)
path.value = get_path_value()
hostname = pn.widgets.TextInput(name='Hostname', placeholder='Enter a string here...', value=junos_hostname)
training_period = pn.widgets.DatetimeRangePicker(name="Training period")
train_but = pn.widgets.Button(name='Train', sizing_mode='stretch_width')
testing_period = pn.widgets.DatetimeRangePicker(name="Testing period")
threshold = pn.widgets.IntSlider(name='Threshold', start=4, end=10, step=1, value=5)
test_but = pn.widgets.Button(name='Test', sizing_mode='scale_width')
loading = pn.indicators.LoadingSpinner(width=20, height=20, value=False, visible=False)

def load_display(x):
    if(x=='on'):
        loading.value=True
        loading.visible=True
    if(x=='off'):
        loading.value=False
        loading.visible=False
# Sidebar
sidebar = pn.layout.WidgetBox(
    path,
    hostname,
    training_period,
    train_but,
    alert,
    testing_period,
    threshold,
    test_but,
    max_width=350,
    sizing_mode='stretch_both'
)
template = pn.template.MaterialTemplate(
    title='Syslog Analysis',
    sidebar=sidebar,
    busy_indicator=loading
)
# Main
# Action
brush = alt.selection_interval(
    name="brush",
    encodings=["x"],
    on="[mousedown[event.altKey], mouseup] > mousemove",
    translate="[mousedown[event.altKey], mouseup] > mousemove!",
    zoom="wheel![event.altKey]",
)

interaction = alt.selection_interval(
    bind="scales",
    on="[mousedown[event.shiftKey], mouseup] > mousemove",
    translate="[mousedown[event.shiftKey], mouseup] > mousemove!",
    zoom="wheel![event.shiftKey]",
)

# Component
empty_score = pd.DataFrame({'timestamp': [], 'score': []})
score_chart = alt.Chart(empty_score).mark_line().encode(
    x='timestamp',
    y='score',
    tooltip=['timestamp', 'score']
).properties(
    width=600,
    height=360
).add_params(
    brush,
    interaction
)

score_panel = pn.pane.Vega(score_chart, margin=5)
empty_log_count = pd.DataFrame({'timestamp': [], 'count': []})
log_count_chart = alt.Chart(empty_log_count).mark_line().encode(
    x='timestamp',
    y='count',
    tooltip=['timestamp', 'count']
).properties(
    width=600,
    height=360
).interactive()

log_count_panel = pn.pane.Vega(log_count_chart, margin=5)
error = pn.widgets.Tabulator(sizing_mode="stretch_both", margin=5, page_size=5, pagination='remote')
show_log = pn.widgets.Tabulator(styles={"font-size": "10px"}, sizing_mode="stretch_both", margin=5, pagination=None)
# Ticket tab

def load_index_name(es_connection):
    try:
        es = Elasticsearch(
            [{"host": es_connection["host"], "port": es_connection["port"]}],
            http_auth=(es_connection["user"], es_connection["password"]),
            use_ssl=True, verify_certs=False, ssl_show_warn=False
        )
        return list(es.indices.get_alias(index="*").keys())
    except Exception as err:
        return []

index = pn.widgets.AutocompleteInput(name="Index name", options=load_index_name(es_connection))
hostname.link(junos_hostname, value='value')
tag_name = pn.widgets.TextInput(name="Tag name")
ticket_time = pn.widgets.DatetimeRangePicker(name="Error time")
customer = pn.widgets.Select(name="Customer", options=['viettel', 'metfone', 'unitel', 'movitel', 'nnpt', 'mobifone', 'cmc', 'natcom', 'ftel'])
tag_optional = pn.widgets.TextInput(name="Optional tag")
description = pn.widgets.TextAreaInput(name="Description", height=200)
save_but = pn.widgets.Button(name="Save")
alert2 = pn.pane.Alert("")
ticket_tab = pn.Column(
    index,
    junos_hostname,
    tag_name,
    ticket_time,
    customer,
    tag_optional,
    description,
    save_but,
    alert2,
    width=800
)
# Check KB tab
filter_file = pn.widgets.CheckBoxGroup(
    name='Log files', options=['chassisd*', 'config-changes*', 'interactive-commands*', 'jam_chassisd*', 'message*', 'security*'],
    value=['chassisd*', 'config-changes*', 'interactive-commands*', 'jam_chassisd*', 'message*', 'security*'],
    inline=True
)
check_kb_but = pn.widgets.Button(name="Check")
show_kb = pn.widgets.Tabulator(styles={"font-size": "10px"}, sizing_mode="stretch_both", margin=5, pagination=None)
kb_tab = pn.Column(
    pn.Row(filter_file, check_kb_but),
    show_kb
)
# Code logic
async def train_but_click(event):
    print("train button click")
    load_display('on')
    await asyncio.sleep(1)
    alert.object = ""
    alert.param.trigger("object")
    result = await training_data(path.value, str(training_period.value[0]), str(training_period.value[1]), hostname.value)
    alert.object = result
    alert.param.trigger("object")
    load_display('off')

def test_but_click(event):
    print("test button click")
    load_display('on')
    st = dt.datetime.now()
    score, count, test_data = testing_data(str(testing_period.value[0]), str(testing_period.value[1]))
    print(dt.datetime.now() - st)
    score_chart.data = score.copy()
    score_panel.param.trigger('object')
    log_count_chart.data = count
    log_count_panel.param.trigger('object')
    error.value = score[score['score'] > threshold.value]
    show_log.value = test_data
    load_display('off')

async def save_but_click(event):
    try:
        cnx = mysql.connector.connect(
            host=ticket_db["host"],
            port=ticket_db["port"],
            user=ticket_db["user"],
            password=ticket_db["password"],
            database="ticket"
        )
        cursor = cnx.cursor()
        query = """
        INSERT INTO ticket (index_name, junos_hostname, tag_name, start_time, stop_time, customer, tag_optional, description)
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
        """.format(index.value, junos_hostname.value, tag_name.value, str(ticket_time.value[0]), str(ticket_time.value[1]),
        customer.value, tag_optional.value, description.value)
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
        alert2.alert_type = "success"
        alert2.object = "Save successful"
    except:
        alert2.alert_type = "danger"
        alert2.object = "Save error"

train_but.on_click(train_but_click)
test_but.on_click(test_but_click)
save_but.on_click(save_but_click)


def callback_error(target, event):
   target.value = score_chart.data[score_chart.data['score'] > event.new]

threshold.link(error, callbacks={'value': callback_error})

def filtered_score(selection):
    if not selection:
        pass
    else:
        s = dt.datetime.utcfromtimestamp(selection['timestamp'][0]/1000)
        e = dt.datetime.utcfromtimestamp(selection['timestamp'][1]/1000)
        show_log.value = inspect_data(str(s), str(e))
        filter_score = score_chart.data[(score_chart.data['timestamp'] >= str(s)) & (score_chart.data['timestamp'] < str(e))].copy()
        error.value = filter_score[filter_score['score'] > threshold.value]

pn.bind(filtered_score, score_panel.selection.param.brush, watch=True)
def check_kb_click(event):
    load_display('on')
    kb = check_kb(path.value, testing_period.value[0], testing_period.value[1], hostname.value, filter_file.value)
    print(kb)
    load_display('off')

check_kb_but.on_click(check_kb_click)
# Append a layout to the main area, to demonstrate the list-like API
template.main.append(
    pn.Tabs(
        ('Analysis', pn.GridBox(ncols=2, nrows=2,
                        objects=[
                            pn.Column(pn.pane.Markdown("# Score panel"), score_panel),
                            pn.Column(pn.pane.Markdown("# Possible error"), error, sizing_mode="stretch_both"),
                            pn.Column(pn.pane.Markdown("# Total document count per hour"), log_count_panel),
                            pn.Column(pn.pane.Markdown("# Raw log"), show_log, sizing_mode="stretch_both")], 
                        sizing_mode="stretch_both"
        )),
        ('Save ticket', ticket_tab),
        ('Check KB', kb_tab)
    )
)

template.servable()
