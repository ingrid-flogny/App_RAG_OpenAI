from dash.dependencies import Input, Output, State
import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from config import OPENAI_API_KEY
from dash.exceptions import PreventUpdate
import base64


def callbacks_gtp35(app):

    # Drag document -> save the document
    @app.callback(
        Output("alert_upload_doc_gpt35_ok", "is_open"),
        Input('upload_data_gpt35', 'contents'),
        State("upload_data_gpt35", "filename"),
        prevent_initial_call=True
    )
    def save_documents_uploaded(contents, filename):
        if contents:
            doc_folder = os.path.abspath(r'./data')
            temp_pdf_path = os.path.join(doc_folder, f"{filename}")

            # Convert the base64 encoded content to bytes
            content_type, content_string = contents.split(',')
            decoded_doc = base64.b64decode(content_string)

            with open(temp_pdf_path, 'wb') as f:
                f.write(decoded_doc)
            return True

        else:
            raise PreventUpdate

    # Valider upload -> Création embedding
    @app.callback(
        Output("alert_embedding_gpt35_ok", "is_open"),
        Input("validate_embedding_gpt35", "n_clicks")
    )
    def prepare_embedding_gpt35(n_clicks):
        if n_clicks:
            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
            doc_path = os.path.abspath(r'./data')
            documents = SimpleDirectoryReader(doc_path).load_data()
            index = VectorStoreIndex.from_documents(documents)
            index.storage_context.persist()
            return True
        else :
            raise PreventUpdate

    # Question -> Réponse
    @app.callback(
        Output("answer_gpt35", "children"),
        Input("ask_question_gpt35", "n_clicks"),
        State("textarea_question_gpt35", "value")
    )
    def answer_question_gpt35(n_clicks, question_txt):
        if n_clicks:
            # rebuild storage context
            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
            storage_context = StorageContext.from_defaults(persist_dir="./storage")
            index = load_index_from_storage(storage_context)
            # query
            query_engine = index.as_query_engine()
            response = query_engine.query(question_txt)
            print("response", response)
            return str(response)
        else:
            raise PreventUpdate
