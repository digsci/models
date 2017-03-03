from bokeh.layouts import row, column
from bokeh.models import Slider, Button, Div
from bokeh.models.callbacks import CustomJS
from bokeh.plotting import figure, curdoc, ColumnDataSource
import os
import sys
import copy
import requests
import json

CATCHMENT = sys.argv[1]
TOPMODEL_HOST='localhost'
TOPMODEL_PORT=8000

def getRain(catchment):
    return catchment['rain']

def getQobs(catchment):
    return catchment['Qobs']

def getCatchmentData(catchment_file):
    # Load catchment data and return values
    with open(catchment_file) as data_file:
        return json.load(data_file)

def getTopModel(catchment_data):
    # call topmodel service and return values
    r = requests.post('http://%s:%d/topmodel' % (TOPMODEL_HOST, TOPMODEL_PORT), json=catchment_data)
    return r.json()

catchment_data = getCatchmentData(CATCHMENT)
working_copy_catchment_data = copy.deepcopy(catchment_data)

rain_x = range(10000) 
rain_y = getRain(catchment_data)

rain_fig = figure(
  plot_width=800, 
  plot_height=350,
  x_axis_label='Timestamp [15 mins]',
  y_axis_label='m / 15 min',
  title='Rain Observations',
  toolbar_location="above"
)
rain_obs = rain_fig.circle(rain_x,rain_y, color='#55DDE0',size=3)

qobs_x = range(10000)
qobs_y = getQobs(catchment_data)

model_x = range(10000)
model_y = getTopModel(catchment_data)

model_fig = figure(
  plot_width=800, 
  plot_height=350,
  x_axis_label='Timestamp [15 mins]',
  y_axis_label='m / 15 min',
  title='Catchment Discharge',
  toolbar_location="above"
)
qobs = model_fig.circle(qobs_x,qobs_y, color='#504077', size=3, legend="Observations")
model = model_fig.circle(model_x,model_y, color='#DD7373', size=3, legend="Predictions")

def slider_cb(attr, old, new):
  working_copy_catchment_data['parameters'][0] = (qs0_slider.value * 4e-5) / 100 
  working_copy_catchment_data['parameters'][1] = lnTe_slider.value 
  working_copy_catchment_data['parameters'][2] = m_slider.value 
  working_copy_catchment_data['parameters'][3] = Sr0_slider.value 
  working_copy_catchment_data['parameters'][4] = Srmax_slider.value 
  working_copy_catchment_data['parameters'][5] = td_slider.value 
  working_copy_catchment_data['parameters'][7] = vr_slider.value 
  working_copy_catchment_data['parameters'][8] = k0_slider.value 
  working_copy_catchment_data['parameters'][9] = CD_slider.value 
  y = getTopModel(working_copy_catchment_data)
  model.data_source.data["y"] = y

# This data source is just used to communicate / trigger the real callback
source = ColumnDataSource(data=dict(value=[]))
source.on_change('data', slider_cb)

init_value = int((3.167914e-05 / 4e-5) * 100)
qs0_slider = Slider(start=1, end=100, value=init_value, step=0.1,
        title="Initial subsurface flow / unit area [% 0 - 4e-5 m]", 
        callback_policy="throttle", callback_throttle=300)
qs0_slider.callback = CustomJS(args=dict(source=source), code="""
  source.data = { value: [cb_obj.value] }
""")

lnTe_slider = Slider(start=-2, end=1, value=-5.990615e-01, step=.1,
                    title="Log of the areal average of T0 [m2/h]", callback_policy="throttle", callback_throttle=300)
lnTe_slider.callback = CustomJS(args=dict(source=source), code="""
  source.data = { value: [cb_obj.value] }
""")

m_slider = Slider(start=0, end=0.2, value=2.129723e-02, step=.01,
                    title="Decline of transmissivity in soil profile", callback_policy="throttle", callback_throttle=300)
m_slider.callback = CustomJS(args=dict(source=source), code="""
  source.data = { value: [cb_obj.value] }
""")

Sr0_slider = Slider(start=0, end=0.02, value=2.626373e-03, step=0.001,
        title="Initial root zone storage deficit [m]", 
        callback_policy="throttle", callback_throttle=300)
Sr0_slider.callback = CustomJS(args=dict(source=source), code="""
  source.data = { value: [cb_obj.value] }
""")

Srmax_slider = Slider(start=0, end=2, value=8.683245e-01, step=.1,
                    title="Maximum root zone storage deficit", callback_policy="throttle", callback_throttle=300)
Srmax_slider.callback = CustomJS(args=dict(source=source), code="""
  source.data = { value: [cb_obj.value] }
""")

td_slider = Slider(start=0, end=3, value=2.850000e+00, step=.1,
                    title="Unsaturated zone time delay [h/m]", callback_policy="throttle", callback_throttle=300)
td_slider.callback = CustomJS(args=dict(source=source), code="""
  source.data = { value: [cb_obj.value] }
""")

vr_slider = Slider(start=100, end=2500, value=1.199171e+03, step=1,
                    title="Channel flow inside catchment [m/h]", callback_policy="throttle", callback_throttle=300)
vr_slider.callback = CustomJS(args=dict(source=source), code="""
  source.data = { value: [cb_obj.value] }
""")

k0_slider = Slider(start=0, end=0.01, value=9.361053e-03, step=.001,
                    title="Surface hydraulic conductivity [m/h]", callback_policy="throttle", callback_throttle=300)
k0_slider.callback = CustomJS(args=dict(source=source), code="""
  source.data = { value: [cb_obj.value] }
""")

CD_slider = Slider(start=0, end=5, value=7.235573e-01, step=0.1,
        title="Capillary drive [Morel-Seytoux and Khanhi]", 
        callback_policy="throttle", callback_throttle=300)
CD_slider.callback = CustomJS(args=dict(source=source), code="""
  source.data = { value: [cb_obj.value] }
""")

def reset_button_cb():
  y = getTopModel(catchment_data)
  model.data_source.data["y"] = y
  qs0_slider.value = int((catchment_data['parameters'][0] / 4e-5) * 100)
  lnTe_slider.value = catchment_data['parameters'][1] 
  m_slider.value = catchment_data['parameters'][2] 
  Sr0_slider.value = catchment_data['parameters'][3] 
  Srmax_slider.value = catchment_data['parameters'][4] 
  td_slider.value = catchment_data['parameters'][5] 
  vr_slider.value = catchment_data['parameters'][7] 
  k0_slider.value = catchment_data['parameters'][8] 
  CD_slider.value = catchment_data['parameters'][9] 

reset_button = Button(label="Reset", width=30)
reset_button.on_click(reset_button_cb)

header_txt = "<h2>%s - TopModel Predictions</h2>" % os.path.splitext(CATCHMENT)[0]
header_div = Div(text=header_txt, width=450)

curdoc().add_root(column(header_div,rain_fig,model_fig,row(qs0_slider,lnTe_slider,m_slider,reset_button),row(Sr0_slider,Srmax_slider,td_slider),row(vr_slider,k0_slider,CD_slider)))
curdoc().title = "%s - TopModel Predictions" % os.path.splitext(CATCHMENT)[0]

