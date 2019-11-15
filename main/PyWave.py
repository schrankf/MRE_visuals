#!/usr/bin/env python3

# packages
from main.Data import Data
import numpy as np
import plotly as py
import plotly.graph_objects as go
import plotly.io as pio
# plotly offline mode
py.offline.init_notebook_mode(connected=True)
# change render to browser
pio.renderers.default = "browser"


class PyWave:
    """"
    Main class PyWave:
    Animate wave field around plot.ly
    """

    def __init__(self):
        """
        Constructor
        """
        self.data = None

    def get_data(self, wave_file, mag_file, mask_file, n=32, pm=-1):
        """
        """
        self.data = Data.from_txt(wave_file, mag_file, mask_file, n, pm)

    def plot(self):
        """
        Main plot method
        :return:
        """
        assert self.data is not None, 'No data loaded'

        # set n-frames
        frames = [go.Frame(data=go.Surface(z=np.real(self.data.waves[:, :, idx]),
                                           surfacecolor=self.data.magnitude,
                                           colorscale='Gray',
                                           cmin=np.nanmin(self.data.magnitude) + 20,
                                           cmax=np.nanmin(self.data.magnitude) - 20,
                                           hovertemplate="Wave amplitude: %{z}m",
                                           hoverlabel=dict(),
                                           showscale=False,
                                           lighting=dict(ambient=1)),
                           name=str(idx))
                  for idx in range(0, self.data.steps)]

        # set first image
        trace = go.Surface(z=np.real(self.data.waves[:, :, 1]),
                           surfacecolor=self.data.magnitude,
                           colorscale='Gray',
                           cmin=np.nanmin(self.data.magnitude) + 20,
                           cmax=np.nanmin(self.data.magnitude) - 20,
                           hovertemplate="Wave amplitude: %{z}m",
                           hoverlabel=dict(),
                           showscale=False,
                           lighting=dict(ambient=1))

        # update figure with frames and trace
        fig = go.Figure(frames=frames)
        fig.add_trace(trace)

        # transition function
        def frame_args(duration):
            return dict(frame=dict(duration=duration, redraw=True),
                        mode="immediate",
                        fromcurrent=True,
                        transition=dict(duration=duration, easing="elastic"))

        # buttons
        menu = dict(type="buttons",
                    x=0.1,
                    y=0,
                    pad=dict(r=10, t=70),
                    direction='left',
                    buttons=[dict(label="&#9654;",
                                  method="animate",
                                  args=[None, frame_args(1)]),
                              dict(label="&#9724;",
                                   method="animate",
                                   args=[None, frame_args(0)])],
                    font=dict(family='Arial', size=12, color='black'))

        # sliders
        # sliders = dict(pad=dict(b=10, t=60),
        #                len=0.9,
        #                x=0.1,
        #                y=0,
        #                steps=[dict(args=[[f.name], frame_args(1)],
        #                            label=str(k),
        #                            method="animate") for k, f in enumerate(fig.frames)])

        # set layout
        def get_range(ftr=2.):
            ran_min, ran_max = np.nanmin(np.real(self.data.waves)), np.nanmax(np.real(self.data.waves))
            return [ran_min * ftr, ran_max * ftr]

        fig.update_layout(title=dict(text='<b>MRE Wave field</b>',
                                     font=dict(family='Arial', size=16, color='white')),
                          showlegend=False,
                          width=800,
                          height=800,
                          font=dict(family='Arial', size=12, color='black'),
                          plot_bgcolor='rgba(0,0,0,1)',
                          paper_bgcolor='rgba(0,0,0,1)',
                          scene=dict(zaxis=dict(range=get_range(), autorange=False,
                                                visible=False),
                                     xaxis=dict(visible=False),
                                     yaxis=dict(visible=False),
                                     aspectratio=dict(x=1, y=1, z=1),
                                     ),
                          autosize=False,
                          # sliders=[sliders],
                          updatemenus=[menu])

        fig.show()

    def export_plot(self):
        pass
