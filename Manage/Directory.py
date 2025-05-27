from pathlib import Path


class CompDirectory:
    def __init__(self):
        self.__root = Path.cwd()
        self.__output_doc = self.__root.joinpath('Outputs')
        self.__url = 'https://ww3.sunat.gob.pe/cl-ti-itmrconsmulruc/jrmS00Alias'
        self.__input = self.__output_doc.joinpath('Rucs.txt')
        self.__output = self.__output_doc.joinpath('Consulta_Ruc.txt')

    def get_output_doc(self):
        return self.__output_doc

    def get_url(self):
        return self.__url

    def get_input(self):
        return self.__input

    def get_output(self):
        return self.__output
