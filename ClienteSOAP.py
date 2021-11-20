from suds.client import Client
url='http://172.16.1.125:8080/WSSIE/SIEService?wsdl'
cliente=Client(url)
if __name__=='__main__':
    print(cliente)
    alumno=cliente.service.consultarAlumno(noControl='14010001')
    print(alumno)