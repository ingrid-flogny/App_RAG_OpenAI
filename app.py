from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from src.callbacks.callbacks_gpt35 import callbacks_gtp35
from src.styles import STYLE_DRAG_AND_DROP_GPT35, STYLE_HEADER_CARDS, STYLE_BUTTON

app = Dash(__name__,
    suppress_callback_exceptions=True,
    external_stylesheets = [dbc.themes.BOOTSTRAP],
       )

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='RAG GPT 3.5 turbo',
                children=[
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Base documentaire", style=STYLE_HEADER_CARDS),
                                dcc.Upload(id='upload_data_gpt35',
                                           children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                                           style=STYLE_DRAG_AND_DROP_GPT35,
                                           #multiple=True
                               ),
                                dbc.Alert("Document uploaded",
                                          id="alert_upload_doc_gpt35_ok",
                                          is_open=False,
                                          duration=4000),
                                html.Button(children="Valider",
                                            id= "validate_embedding_gpt35",
                                            style = STYLE_BUTTON,
                                            #width={'size': 8, 'offset': 0}
                                            ),
                                dbc.Alert("Embedding préparé",
                                          id="alert_embedding_gpt35_ok",
                                          is_open=False,
                                          duration=4000)
                            ])
                        ], width= {'size': 6, 'offset': 0}
                        ),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Question / Réponse", style=STYLE_HEADER_CARDS),
                                html.Br(),
                                html.H5("Question :"),
                                dcc.Textarea(
                                        id='textarea_question_gpt35',
                                        placeholder = 'Ask a question about the document',
                                        value='',
                                        style={'width': '90%', 'height': 200},
                                    ),
                                html.Button(children="Ask",
                                            id="ask_question_gpt35",
                                            style=STYLE_BUTTON,
                                            # width={'size': 8, 'offset': 0}
                                            ),
                                html.Hr(),
                                html.H5("Réponse :"),
                                html.H3(children='', id='answer_gpt35')
                            ])
                        ])
                    ])
                ]
        ),
    ])
])


callbacks_gtp35(app)

if __name__ == '__main__':
    app.run(debug=True, port=8051)