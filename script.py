# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 07:03:45 2016

@author: vanessatovar
"""
import pandas as pd

"""
Leer el archivo csv
"""

data = pd.read_csv("data.csv")

"""
Eliminar las columnas que no considero necesarias
"""

columns_to_drop = ['Ha.cambiado.usted.de.dirección.',
                   'De.ser.afirmativo..indique.el.motivo', 
                   'Si.reprobó.una.o.más.materias.indique.el.motivo',
                   'Procedencia',
                   'X.Contrajo.Matrimonio.',
                   'En.caso.afirmativo.señale..año.de.la.solicitud..institución.y.motivo',
                   'En.caso.de.ser.afirmativo..indique.tipo.de.actividad.y.su.frecuencia',
                   'Sugerencias.y.recomendaciones.para.mejorar.nuestra.atención']
                   
data = data[[col for col in data.columns if col not in columns_to_drop]]

"""
Renombrar las columnas para manejarlas mejor
"""

data.columns=['Indice',
              'PeriodoAcademico',
              'Cedula',
              'Nacimiento',
              'Edad',
              'EstadoCivil',
              'Sexo',
              'Escuela',
              'AnoIngreso',
              'ModalidadIngreso',
              'SemestreCursa',
              'InscritasAnterior',
              'AprobadasAnterior',
              'RetiradasAnterior',
              'ReprobadasAnterior',
              'PromedioPonderado',
              'Eficiencia',
              'InscritasCurso',
              'Realizando',
              'CuantasVeces',
              'LugarReside',
              'PersonasVive',
              'TipoVivienda',
              'MontoAlquila',
              'DireccionAlquila',
              'BeneficioOtro',
              'RealizandoActividad',
              'MontoBeca',
              'IngresoResponsable',
              'IngresoAmigos',
              'IngresoActividades',
              'IngresoTotal',
              'EgresoAlimentacion',
              'EgresoTransporte',
              'EgresosMedicos',
              'EgresosOdontologicos',
              'EgresosPersonales',
              'EgresosResidencia',
              'EgresosEstudio',
              'EgresosRecreacion',
              'EgresosOtros',
              'TotalEgresos',
              'ResponsableEconomico',
              'CargaFamiliar',
              'IngresoMensual',
              'OtrosIngresos',
              'TotalIngresos',
              'ResponsableVivienda',
              'ResponsableAlimentacion',
              'ResponsableTransporte',
              'ResponsableMedicos',
              'ResponsableOdontologicos',
              'ResponsableEducativos',
              'ResponsableServivios',
              'ResponsableCondominio',
              'ResponsableOtros',
              'ResponsableTotalEgresos',
              'OpinionUsuarios'
              ]
                        
"""
Separar Periodo Academico
Los voy a separa en 2 columnas una para el año y el otro para el periodo
"""

nuevo=data.PeriodoAcademico
nuevo=nuevo.str.lower()
tamano=len(nuevo)

esta1=nuevo.str.contains('14',na=False)
esta2=nuevo.str.contains('15',na=False)
searchfor = ['ii', 'seg','2s','2do']
esta3=nuevo.str.contains(('|'.join(searchfor)),na=False)
searchfor2 = ['pri','1s','s1,i']
esta4=nuevo.str.contains(('|'.join(searchfor2)),na=False)

ano= ['NaN']*len(nuevo)

periodo= ['NaN']*len(nuevo)

row=0

while (row < tamano):
    if esta1[row] and esta3[row]:                                              
        periodo[row]='2'
        ano[row]='2014'
    if esta2[row] and esta3[row]:
        periodo[row]='2'
        ano[row]='2015'
    if esta1[row] and esta4[row]:
        periodo[row]='1'
        ano[row]='2014'
    if esta2[row] and esta4[row]: 
        periodo[row]='1'
        ano[row]='2015'
    if (esta1[row]==False and esta2[row]==False) and esta4[row]:
        periodo[row]='1'
        ano[row]='NaN'
    if (esta1[row]==False and esta2[row]==False) and esta3[row]:
        periodo[row]='2'
        ano[row]='NaN'
    if (esta3[row]==False and esta4[row]==False) and esta1[row]:
        periodo[row]='NaN'
        ano[row]='2014'
    if (esta3[row]==False and esta4[row]==False) and esta2[row]:
        periodo[row]='NaN'
        ano[row]='2015' 
    if esta3[row]==False and esta4[row]==False and esta1[row]==False and esta2[row]==False:
        periodo[row]='NaN'
        ano[row]='NaN'
    row=row+1         
    
"""
Separar la fecha en 3 columnas diferentes Dia Mes y AñoNac
"""

nuevo2=data.Nacimiento
dianac= ['NaN']*len(nuevo)
mesnac= ['NaN']*len(nuevo)
anonac= ['NaN']*len(nuevo)

row=0

while (row < tamano):
    if '/' in nuevo2[row]:
        dianac[row],mesnac[row],ano2=nuevo2[row].split('/')
        if len(ano2)==2:
            anonac[row]='19'+ano2
        else:
            anonac[row]=ano2
    if '-' in nuevo2[row]:
        dianac[row],mesnac[row],ano2=nuevo2[row].split('-')
        if len(ano2)==2:
            anonac[row]='19'+ano2
        else:
            anonac[row]=ano2
    if (' ' in nuevo2[row]) and '/' not in nuevo2[row]:
        dianac[row],mesnac[row],ano2=nuevo2[row].split(' ')
        if len(ano2)==2:
            anonac[row]='19'+ano2
        else:
            anonac[row]=ano2
    if '/' not in nuevo2[row] and '-' not in nuevo2[row] and (' ' not in nuevo2[row]):
        completa=[]
        palabra=nuevo2[row]
        n=2
        completa=[palabra[i:i+n] for i in range(0, len(palabra), n)]
        dianac[row]=completa[0]
        mesnac[row]=completa[1]
        anonac[row]=completa[2]
    row=row+1

"""
Arreglar la columna edad solo dejando el numero
"""
nuevo3=data.Edad
nuevo3=nuevo3.str.lower()
edad= ['NaN']*len(nuevo)

row=0
while (row < tamano):
    if 'a' in nuevo3[row]:
        num=filter(str.isdigit, nuevo3[row])
        edad[row]=num
    else:
        edad[row]=nuevo3[row]
    row=row+1

"""
Cambiar el Sexo Femenino 1 Masculino 0
"""

sexo=data.Sexo
sexo=sexo.replace(['Femenino','Masculino'],['1','0'])


"""
Arreglar Promedio para que todos sean floats
"""
nuevo=data.PromedioPonderado
promedio= ['NaN']*len(nuevo)

row=0
while (row < tamano):
    palabra=str(nuevo[row])
    if not(palabra.index('.')==1) or not(palabra.index('.')==2):
        removed = palabra.replace(".", "")
        punto=removed[:2] + '.' + removed[2:]
        promedio[row]=punto
    else:
        promedio[row]=nuevo[row]
    row=row+1

"""
Arreglar eficiencia para que todos sean floats
"""
nuevo=data.Eficiencia
eficiencia= ['NaN']*len(nuevo)

row=0
while (row < tamano):
    palabra=str(nuevo[row])
    if palabra.index('.')==1:
        eficiencia[row]=palabra
    else:
        removed = palabra.replace(".", "")
        punto= '0.' + removed
        eficiencia[row]=punto
    row=row+1

"""
Verificar que toda la suma de ingreso del alumno sea la indicada
"""
beneficio=data.BeneficioOtro
beneficio=beneficio.str.lower()

realizando=data.RealizandoActividad
realizando=realizando.str.lower()

beca=data.MontoBeca
beca=beca.fillna(0)

responsable=data.IngresoResponsable
responsable=responsable.fillna(0)

amigos=data.IngresoAmigos
amigos=amigos.fillna(0)

actividades=data.IngresoActividades
actividades=actividades.fillna(0)

total=data.IngresoTotal
total=total.fillna(0)
             
ingresototal= ['NaN']*len(nuevo)

row=0
while (row < tamano):
    if ('s' in beneficio[row]) or ('s' in realizando[row]):
        if actividades[0]==0:
            realizando[row]='si'
    sub=beca[row]+responsable[row]+amigos[row]+actividades[row]
    if sub > total[row]:
        total[row]=sub
    ingresototal[row]=total[row] 
    row=row+1

"""
Verificar que toda la suma de egreso del alumno sea la indicada
"""

alquila=data.MontoAlquila
alquila=alquila.fillna(0)

alimentacion=data.EgresoAlimentacion
alimentacion=alimentacion.fillna(0)

transporte=data.EgresoTransporte
transporte=transporte.fillna(0)

medicos=data.EgresosMedicos
medicos=medicos.fillna(0)

odontologicos=data.EgresosOdontologicos
odontologicos=odontologicos.fillna(0)

personales=data.EgresosPersonales
personales=personales.fillna(0)

residencia=data.EgresosResidencia
residencia=residencia.fillna(0)

estudio=data.EgresosEstudio
estudio=estudio.fillna(0)

recreacion=data.EgresosRecreacion
recreacion=recreacion.fillna(0)

otros=data.EgresosOtros
otros=otros.fillna(0)

totale=data.TotalEgresos
totale=totale.fillna(0)

egresototal= ['NaN']*len(nuevo)

row=0
while (row < tamano):
    if alquila[row]>residencia[row]:
        residencia[row]=alquila[row]
    if type(residencia[row]) is str:
        residencia[row]=filter(str.isdigit, residencia[row])
    residencia[row]=int(residencia[row])
    sub=alimentacion[row]+transporte[row]+medicos[row]+odontologicos[row]+personales[row]+residencia[row]+estudio[row]+recreacion[row]+otros[row] 
    if sub > totale[row]:
        totale[row]=sub
    egresototal[row]=totale[row] 
    row=row+1
 
"""
Verificar que toda la suma de ingreso del responsable sea la indicada
"""
mensual=data.IngresoMensual
mensual=mensual.fillna(0)

otrosi=data.OtrosIngresos
otrosi=otrosi.fillna(0)

totalr=data.TotalIngresos
totalr=totalr.fillna(0)

ringresototal= ['NaN']*len(nuevo)

row=0
while (row < tamano):
    if 'b' in mensual[row]:
        rest=filter(str.isdigit, mensual[row])      
        mensual[row]=rest
    if ',' in mensual[row]:       
        myString=mensual[row]
        prueba= [pos for pos, char in enumerate(myString) if char == ',']
        if len(prueba)>1:
            seg=prueba[1]
            completa=mensual[row]
            myString = completa[:seg] + "." + completa[seg+1:]
            removed = myString.replace(",", "")
        sep = ','
        rest = myString.split(sep, 1)[0]
        mensual[row]=rest
    if '.' in mensual[row]:
        algo=mensual[row]
        sep = '.'
        rest = algo.split(sep, 1)[0]
        mensual[row]=rest
    mensual[row]=int(mensual[row])
    otrosi[row]=str(otrosi[row])
    if 'b' in otrosi[row] :
        rest=filter(str.isdigit, otrosi[row])       
        otrosi[row]=rest
    if ',' in otrosi[row]:       
        myString=otrosi[row]
        prueba= [pos for pos, char in enumerate(myString) if char == ',']
        if len(prueba)>1:
            seg=prueba[1]
            completa=otrosi[row]
            myString = completa[:seg] + "." + completa[seg+1:]
            removed = myString.replace(",", "")
        sep = ','
        rest = myString.split(sep, 1)[0]
        otrosi[row]=rest
    if '.' in otrosi[row]:
        algo=otrosi[row]
        sep = '.'
        rest = algo.split(sep, 1)[0]
        otrosi[row]=rest
    if 'N' in otrosi[row]:
        otrosi[row]='0'
    otrosi[row]=int(otrosi[row])
    sub=mensual[row]+otrosi[row]
    if 'b' in totalr[row]: 
        rest=filter(str.isdigit, totalr[row])      
        totalr[row]=rest
    if ',' in totalr[row]:      
        myString=totalr[row]
        prueba= [pos for pos, char in enumerate(myString) if char == ',']
        if len(prueba)>1:
            seg=prueba[1]
            completa=totalr[row]
            myString = completa[:seg] + "." + completa[seg+1:]
            removed = myString.replace(",", "")
        sep = ','
        rest = myString.split(sep, 1)[0]
        totalr[row]=rest
    if '.' in totalr[row]:
        algo=totalr[row]
        sep = '.'
        rest = algo.split(sep, 1)[0]
        totalr[row]=rest
    totalr[row]=int(totalr[row])
    if sub > totalr[row]:
        totalr[row]=sub
    ringresototal[row]=totalr[row]
    row=row+1

"""
Verificar que toda la suma de egreso del responsable sea la indicada
"""
vivienda=data.ResponsableVivienda
vivienda=vivienda.fillna(0)

alimentacion=data.ResponsableAlimentacion
alimentacion=alimentacion.fillna(0)

transporte=data.ResponsableTransporte
transporte=transporte.fillna(0)

medicos=data.ResponsableMedicos
medicos=medicos.fillna(0)

odontologicos=data.ResponsableOdontologicos
odontologicos=odontologicos.fillna(0)

educativos=data.ResponsableEducativos
educativos=educativos.fillna(0) #float

servicios=data.ResponsableServivios
servicios=servicios.fillna(0)

condominio=data.ResponsableCondominio
condominio=condominio.fillna(0)

otroser=data.ResponsableOtros
otroser=otroser.fillna(0) #float

totaler=data.ResponsableTotalEgresos
totaler=totaler.fillna(0)

regresototal= ['NaN']*len(nuevo)
   
row=0
while (row < tamano):
    vivienda[row]=str(vivienda[row])
    medicos[row]=str(medicos[row])
    odontologicos[row]=str(odontologicos[row])
    condominio[row]=str(condominio[row])
    servicios[row]=str(servicios[row])
    if 'c' in vivienda[row]:
        vivienda[row]='0.0'
    if ',' in vivienda[row]:       
        myString=vivienda[row]
        prueba= [pos for pos, char in enumerate(myString) if char == ',']
        if len(prueba)>1:
            seg=prueba[1]
            completa=vivienda[row]
            myString = completa[:seg] + "." + completa[seg+1:]
            removed = myString.replace(",", "") 
        sep = ','
        rest = myString.split(sep, 1)[0]
        vivienda[row]=rest
    vivienda[row]=float(vivienda[row])
    if 'b' in alimentacion[row] :
        rest=filter(str.isdigit, alimentacion[row])        
        alimentacion[row]=rest
    alimentacion[row]=float(alimentacion[row])
    if 'b' in transporte[row] :
        rest=filter(str.isdigit, transporte[row])        
        transporte[row]=rest
    transporte[row]=float(transporte[row])
    if 'b' in medicos[row] :
        rest=filter(str.isdigit, medicos[row])        
        medicos[row]=rest
    medicos[row]=float(medicos[row])
    if 'o' in odontologicos[row]:
        odontologicos[row]='0.0'
    odontologicos[row]=float(odontologicos[row])
    educativos[row]=float(educativos[row])
    if 'b' in servicios[row] :
        rest=filter(str.isdigit, servicios[row])        
        servicios[row]=rest
    servicios[row]=float(servicios[row])
    if 'b' in condominio[row] :
        rest=filter(str.isdigit, condominio[row])        
        condominio[row]=rest
    condominio[row]=float(condominio[row])
    otroser[row]=float(otroser[row])
    if '.' in totaler[row]:       
        myString=totaler[row]
        prueba= [pos for pos, char in enumerate(myString) if char == '.']
        if len(prueba)>1:
            seg=prueba[0]
            completa=totaler[row]
            myString = completa[:seg] + "," + completa[seg+1:]
            removed = myString.replace(",", "")
            totaler[row]=removed  
    if '+' in totaler[row] :
        rest=filter(str.isdigit, totaler[row])        
        totaler[row]=rest
    if 'b' in totaler[row] :
        rest=filter(str.isdigit, totaler[row])        
        totaler[row]=rest
    if ',' in totaler[row]:
        removed = myString.replace(",", "")
        totaler[row]=removed
    totaler[row]=float(totaler[row])
    sub=vivienda[row]+alimentacion[row]+transporte[row]+medicos[row]+odontologicos[row]+educativos[row]+servicios[row]+condominio[row]+otroser[row]
    if sub > totaler[row]:
        totaler[row]=sub
    regresototal[row]=totaler[row]
    row=row+1

"""
Creacion del DataFrame e Insertar en el csv
"""

columnas={'Período': periodo,
          'Año Académico': ano,
          'Cédula': data.Cedula,
          'Día Nacimiento':dianac,
          'Mes Nacimiento':mesnac,
          'Año Nacimiento':anonac,
          'Edad':edad,
          'Estado Civil': data.EstadoCivil,
          'Sexo': sexo,
          'Escuela': data.Escuela,
          'Año de Ingreso': data.AnoIngreso,
          'Modalidad de Ingreso': data.ModalidadIngreso,
          'Semestre Cursado ':data.SemestreCursa,
          'Inscritas Anterior':data.InscritasAnterior,
          'Aprobadas Anterior': data.AprobadasAnterior,
          'Retiradas Anterior': data.RetiradasAnterior,
          'Reprobadas Anterior': data.RetiradasAnterior,
          'Promedio Ponderado': promedio,
          'Eficiencia': eficiencia,
          'Inscritas en Curso': data.InscritasCurso,
          'Realizando (Tesis/Pasantias)': data.Realizando,
          'Dirección': data.LugarReside,
          'Personas con quien Vive': data.PersonasVive,
          'Tipo de Vivienda':data.TipoVivienda,
          'Ingreso Total': ingresototal,
          'Total Egresos': egresototal,
          'Responsable Económico': data.ResponsableEconomico,
          'Total Ingresos Responsable':ringresototal,
          'Total Egresos Responsable':regresototal,
          'Opinion de losUsuarios': data.OpinionUsuarios
          }
       
entrega=pd.DataFrame(columnas, columns=['Período','Año Académico','Cédula','Día Nacimiento','Mes Nacimiento','Año Nacimiento','Edad','Estado Civil','Sexo','Escuela', 'Año de Ingreso','Modalidad de Ingreso','Semestre Cursado ','Inscritas Anterior','Aprobadas Anterior','Retiradas Anterior','Reprobadas Anterior','Promedio Ponderado','Eficiencia','Inscritas en Curso','Realizando (Tesis/Pasantias)','Dirección', 'Personas con quien Vive','Tipo de Vivienda','Ingreso Total','Total Egresos','Responsable Económico','Total Ingresos Responsable','Total Egresos Responsable','Opinion de losUsuarios'])    
    
entrega.to_csv('minable.csv',index = False)
