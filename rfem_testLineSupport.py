from contextlib import ContextDecorator

from RFEM.initModel import Model
from RFEM import connectionGlobals
from RFEM.suds_requests import RequestsTransport

from suds.client import Client
import requests
import sys
import os

baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print("basename:    ", baseName)
print("dirname:     ", dirName)

sys.path.append(dirName + r"/../..")

from RFEM.initModel import Model, Calculate_all
from RFEM.BasicObjects.node import Node
import xlwings as xw
import pandas as pd
from RFEM.enums import (
    CaseObjectType,
)
from RFEM.Results.resultTables import ResultTables
from MY_RFEM.getResults import getResultsLinesSupport, getResultsPerMember
class connect_model(ContextDecorator): 
    # https://github.com/dlubal-software/RFEM_Python_Client/discussions/385
    def __init__(self, model_name:str, delete_all_results:bool = False): 
        self._model_name = model_name
        self._delete_all_results = delete_all_results

    def __enter__(self): 
        if connectionGlobals.connected: 

            modelPath =  connectionGlobals.client.service.get_active_model()
            modelPort = modelPath[-5:-1]

            adapter = requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=1)
            connectionGlobals.session.mount('http://', adapter)
            trans = RequestsTransport(connectionGlobals.session)

            cModel = Client(
                url=f'{connectionGlobals.url}:{modelPort}/wsdl',
                transport=trans, 
                location = f'{connectionGlobals.url}:{modelPort}', 
                cache=connectionGlobals.ca, 
                timeout=360, 
            )
            #cModel.service.delete_all_results() # added since no new calculations were started otherwise
            self._model = Model
            self._model.clientModel = cModel
            self._model.clientModelDct[self._model_name] = cModel
        else: 
            self._model = Model(new_model=False, model_name=self._model_name)
        print('Begin modification ...')
        if self._delete_all_results:
            self._service.delete_all_results()
        self._service.begin_modification()
        return self._model

    def __exit__(self, exc_type, exc, exc_tb): 
        print('Finished modification ... ')
        self._service.finish_modification()
        self._service.close_connection()
        print('Disconnected from server')

    @property
    def _service(self): 
        return self._model.clientModel.service
    

    


if __name__ == "__main__":
    with connect_model("lineHinges", delete_all_results=False) as model:
        #dic = ResultTables.LinesSupportForces(loading_type=CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION, loading_no=1,object_no=1)
        dic = getResultsLinesSupport(loading_type=CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION, loading_no=1)
        df=pd.DataFrame(dic)
        print(df)
        df.to_pickle("test5.pkl")