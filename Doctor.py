# -*- coding: utf-8 -*-
#Fix para abrir Firefox 47.0+, ejecuta el comando: pip install -U selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
import time, unicodedata, sys, getopt
import random
import os

#pip install Pillow
import PIL
from PIL import Image
#pip install datetime
from datetime import datetime
def main(argv):
    driver = ''
    navegador = ''
    ambiente = ''
    modulo = ''

    #active account
    act_username_chrome = "jenkins_drchrome@mediconecta.com"
    act_username_firefox = "jenkins_drfirefox@mediconecta.com"
    act_username_ie = "jenkins_drie@mediconecta.com"
    act_nacionalidad = "Venezuela"
    act_cedula = "87654321"
    act_birthday = ["1","1","2016"]
    act_birthday_chrome = ["1","1","2016"]
    act_birthday_firefox = ["1","2","2016"]
    act_birthday_ie = ["1","3","2016"]

    password = "dba123"

    #inactive account
    inact_username = "dr_inactivo@mediconecta.com"
    inact_nacionalidad = "Venezuela"
    inact_cedula = "87654322"
    inact_birthday = ["5", "5", "2016"]

    #patients
    IDPacienteDevChrome = 'a0HZ0000007gYqP'   #Pruebas Jenkins Chrome
    IDPacienteDevFirefox = 'a0HZ0000007gYqU'   #Pruebas Jenkins Firefox
    IDPacienteDevIE = 'a0HZ0000007gYqZ'   #Pruebas Jenkins IE

    IDPacienteProdChrome = 'a0HU000000M20fF'   #Pruebas Jenkins Chrome
    IDPacienteProdFirefox = 'a0HU000000M21DL'   #Pruebas Jenkins Firefox
    IDPacienteProdIE = 'a0HU000000M21Du'   #Pruebas Jenkins IE

    try:
      opts, args = getopt.getopt(argv,"d:a:m:")
    except getopt.GetoptError:
        print 'SINTAXIS: doctor.py -d Chrome/Firefox/Ie -a portaldev/testprod/consultas -m Autentica/Login/Atender/AtenderChrome/AtenderFirefox/AtenderIE'
        sys.exit(2)

    for opt, arg in opts:
        if opt in('-h', '--h', '-help', '--help'):
            print 'SINTAXIS: doctor.py -d Chrome/Firefox/Ie -a portaldev/testprod/consultas -m Autentica/Login/Atender/AtenderChrome/AtenderFirefox/AtenderIE'
            sys.exit()

        elif opt in ("-d", "--d"):
            #Setear navegador
            if arg == 'Chrome' or arg == 'Firefox' or arg == 'Ie':
                navegador = arg
            else:
                print 'valores esperados: -d Chrome / Firefox / Ie'
                sys.exit()

        elif opt in ("-a", "--a"):
            #Setear ambiente
            if arg == 'portaldev' or arg == 'testprod' or arg == 'consultas':
                ambiente = arg

                if ambiente == 'portaldev':
                    if navegador == 'Chrome':
                        paciente = IDPacienteDevChrome
                    elif navegador == 'Firefox':
                        paciente = IDPacienteDevFirefox
                    elif navegador == 'Ie':
                        paciente = IDPacienteDevIE
                else:
                    if navegador == 'Chrome':
                        paciente = IDPacienteProdChrome
                    elif navegador == 'Firefox':
                        paciente = IDPacienteProdFirefox
                    elif navegador == 'Ie':
                        paciente = IDPacienteProdIE

            else:
                print 'valores esperados: -a portaldev / testprod / consultas'
                sys.exit()

        elif opt in ("-m", "--m"):
            #Setear modulo
            if arg == 'Autentica' or arg == 'Login' or arg == 'Atender' or arg == 'AtenderChrome' or arg == 'AtenderFirefox' or arg == 'AtenderIE' or arg == 'HistoriaCitas' or arg == "AppHistoriasClientes" or arg == "ProgramarCitaGalenNuevoP" or arg == "DoctorProgramarCitaMinorRegRep":
                modulo = arg
            elif arg == "Pruebas_de_Diagnostico" or arg == "Pruebas_de_Prescripciones" or arg == "Pruebas_de_Examenes" or arg == 'AtenderPacienteConDPE' or arg == "ProgramarCitaGalen" or arg == "ProgramarCitaGalenMinor" or arg == "ProgramarCitaGalenRegMinor" or arg == "DoctorProgramarCitaPaciente":
                modulo = arg
            elif arg == "reAgendarCancelarCita" or arg == "DoctorProgramarCitaMinorCont" or arg == "DatosdelConsultorio" or arg == "ManejoDeSecretarias" or arg == "ManejoDeMonedas" or arg == "ManejoDeConfiguraciones" or arg == "AppAtencionAlCliente" or arg == "AppLogEmails" or arg == 'ManejoDoctores':
                modulo = arg
            else:
                print ('valores esperados: -m Autentica/Login/Atender/HistoriaCitas/Pruebas_de_Diagnostico/Pruebas_de_Prescripciones/Pruebas_de_Examenes/AtenderPacienteConDPE/ProgramarCitaGalen/ProgramarCitaGalenMinor/AppHistoriasClientes/ProgramarCitaGlenNuevoP/ProgramarCitaGalenRegMinor/'
                       'DoctorProgramarCitaMinorRegRep/DoctorProgramarCitaPaciente/reAgendarCancelarCita/DoctorProgramarCitaMinorCont/DatosdelConsultorio/ManejoDeSecretarias/ManejoDeMonedas/ManejoDeConfiguraciones/AppAtencionAlCliente/AppLogEmails'
                )
                sys.exit()
            if ambiente != '':
                if navegador == 'Chrome':
                    driver = webdriver.Chrome()
                    doctor = act_username_chrome
                    act_birthday = act_birthday_chrome

                elif navegador == 'Firefox':
                    driver = webdriver.Firefox()
                    doctor = act_username_firefox
                    act_birthday = act_birthday_firefox

                elif navegador == 'Ie':
                    driver = webdriver.Ie()
                    doctor = act_username_ie
                    act_birthday = act_birthday_ie

                ## COMIENZAN LAS PRUEBAS
                driver.maximize_window()
                driver.implicitly_wait(20)
                #driver.get("http://" + ambiente + ".mediconecta.com/LoginD")

                print "Comenzando Pruebas: " + ambiente + " en " + navegador

                if modulo == 'Autentica':
                    print "Proceso: Solo validar autenticacion correcta"
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Doctor autenticado (" + doctor + ") --> OK"
                    #if "firefox" not in str(driver):
                    assert (log_out(driver) == "exitoso"), "Logout fallido"
                    print " Cerrar sesion (" + doctor + ") --> OK"

                elif modulo == 'Login':
                    print "Proceso: Autenticacion y sus variantes"
                    #print "Recuperar Usuario.."
                    assert (Recuperar_Usuario('Estados Unidos','wrong','6','2','1996', driver, ambiente) == "Fail"), "With wrong info: Recuperar usuario wrong"
                    print " Doctor incorrecto --> OK"

                    assert (Recuperar_Usuario(inact_nacionalidad, inact_cedula, inact_birthday[0], inact_birthday[1], inact_birthday[2], driver, ambiente) == "inactive"),"With inactive info: Recuperar usuario wrong"
                    print " Doctor inactivo --> OK"

                    assert (Recuperar_Usuario(act_nacionalidad, act_cedula, act_birthday[0], act_birthday[1], act_birthday[2], driver, ambiente) == "Success"),"With correct info: Recuperar usuario wrong"
                    print " Doctor correcto (" + doctor + ") --> OK"


                    print "Recuperar Contrasena.."
                    assert (Recuperar_Contrasena('error@mediconecta.com', driver, ambiente) == "Fail"),"With incorrect email: Recuperar contrasena fallida"
                    print " Doctor incorrecto --> OK"

                    assert (Recuperar_Contrasena(inact_username, driver, ambiente) == "Inactive"),"With inactive email: Recuperar contrasena fallida"
                    print " Doctor inactivo --> OK"

                    assert (Recuperar_Contrasena(doctor, driver, ambiente) == "Success"),"With correct email: Recuperar contrasena fallida"
                    print " Doctor correcto (" + doctor + ") --> OK"

                    print "Autenticacion.."
                    #assert (log_in('wrong@mediconecta.com','wrong', driver, ambiente) == "fallido"), "With incorrect login: Autenticacion fallida"
                    print " Doctor incorrecto --> OK"

                    assert (log_in(inact_username, password, driver, ambiente) == "inactivo"), "With inactive account: login failure"
                    print " Doctor inactivo --> OK"

                    assert (log_in(doctor, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Doctor autenticado (" + doctor + ") --> OK"

                    #if "firefox" not in str(driver):
                    assert (log_out(driver) == "exitoso"), "Logout fallido"
                    print " Cerrar sesion (" + doctor + ") --> OK"

                elif modulo == 'CitaODVSee':
                    print "Autenticando paciente: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"
                    print "Proceso: Cita OnDemand VSee"
                    CitaODVSee(driver, ambiente)

                elif modulo == 'Atender':
                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"
                    print "Proceso: AtenderPaciente en " + ambiente
                    AtenderPaciente(paciente, driver)

                elif modulo == "HistoriaCitas":

                    p_driver = webdriver.Chrome()
                    p_driver.maximize_window()
                    p_driver.implicitly_wait(20)

                    print "Autenticando paciente: jenkins_chrome@mediconecta.com"
                    assert (log_in_p("jenkins_chrome@mediconecta.com", "dba123", p_driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"
                    CitaODTokbox(p_driver, ambiente, "si")


                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Historia Citas"
                    historiaCitas(IDPacienteDevChrome, driver)
                    print "Historia Citas --> OK"

                    driver.quit()
                    p_driver.quit()

                elif modulo == "Pruebas_de_Diagnostico":
                    p_driver = webdriver.Chrome()

                    print "Autenticando paciente: Prueba Jenkins Chrome"
                    assert (log_in_p("jenkins_chrome@mediconecta.com", "dba123", p_driver, ambiente)=="exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Cita OnDemand Tokbox"
                    CitaODTokbox(p_driver, ambiente, "si")
                    print "Paciente en sala de espera --> OK"

                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    time.sleep(6)

                    print "Proceso: Atender Paciente"
                    Pruebas_de_Diagnostico('a0HZ0000007gYqP', driver)

                    print " Cita --> OK"
                    time.sleep(3)
                    p_driver.quit()
                    driver.quit()

                elif modulo == "Pruebas_de_Prescripciones":
                    p_driver = webdriver.Chrome()

                    print "Autenticando paciente: Prueba Jenkins Chrome"
                    assert (log_in_p("jenkins_chrome@mediconecta.com", "dba123", p_driver, ambiente)=="exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Cita OnDemand Tokbox"
                    CitaODTokbox(p_driver, ambiente, "si")
                    print "Paciente en sala de espera --> OK"

                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    time.sleep(6)

                    print "Proceso: Atender Paciente"
                    Pruebas_de_Prescripciones('a0HZ0000007gYqP', driver)

                    print " Cita --> OK"
                    time.sleep(3)
                    p_driver.quit()
                    driver.quit()

                elif modulo == "Pruebas_de_Examenes":
                    p_driver = webdriver.Chrome()

                    print "Autenticando paciente: Prueba Jenkins Chrome"
                    assert (log_in_p("jenkins_chrome@mediconecta.com", "dba123", p_driver, ambiente)=="exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Cita OnDemand Tokbox"
                    CitaODTokbox(p_driver, ambiente, "si")
                    print "Paciente en sala de espera --> OK"

                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    time.sleep(6)

                    print "Proceso: Atender Paciente"
                    Pruebas_de_Examenes('a0HZ0000007gYqP', driver)

                    print " Cita --> OK"
                    time.sleep(3)
                    p_driver.quit()
                    driver.quit()

                elif modulo == "AtenderPacienteConDPE":
                    p_driver = webdriver.Chrome()

                    print "Autenticando paciente: Prueba Jenkins Chrome"
                    assert (log_in_p("jenkins_chrome@mediconecta.com", "dba123", p_driver, ambiente)=="exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Cita OnDemand Tokbox"
                    CitaODTokbox(p_driver, ambiente, "si")
                    print "Paciente en sala de espera --> OK"

                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    time.sleep(6)

                    print "Proceso: Atender Paciente con DPE"
                    AtenderPacienteConDPE('a0HZ0000007gYqP', driver)
                    time.sleep(2)

                    print " Cita --> OK"
                    time.sleep(3)
                    p_driver.quit()
                    driver.quit()

                elif modulo == "ProgramarCitaGalen":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCita(driver)
                    print " Cita --> OK"
                    driver.quit

                elif modulo == "ProgramarCitaGalenMinor":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCitaMinor(driver)
                    print " Cita --> OK"
                    driver.quit

                elif modulo == "ProgramarCitaGalenRegMinor":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCitaRegMinor(driver)
                    print " Cita --> OK"
                    driver.quit

                elif modulo == "DoctorProgramarCitaMinorRegRep":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCitaMinorRegRep(driver)
                    print " Cita --> OK"
                    driver.quit

                elif modulo == "DoctorProgramarCitaPaciente":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCitaPaciente(driver)
                    print " Cita --> OK"
                    driver.quit

                elif modulo == "AppHistoriasClientes":
                    p_driver = webdriver.Chrome()

                    print "Autenticando paciente: Prueba Jenkins Chrome"
                    assert (log_in_p("jenkins_chrome@mediconecta.com", "dba123", p_driver, ambiente)=="exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Cita OnDemand Tokbox"
                    CitaODTokbox(p_driver, ambiente, "si")
                    print "Paciente en sala de espera --> OK"

                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    time.sleep(6)

                    print "Proceso: App Historias Clientes"
                    screenshot(driver, "before_cita.jpg")
                    p_driver.find_element_by_id("cphW_ucCita_btnCitaFinalizarPpal").click()
                    time.sleep(2)
                    p_driver.find_element_by_id("cphW_ucCita_btnAceptarFinalizar").click()
                    time.sleep(2)
                    screenshot(driver, "after_cita.jpg")

                    before = Image.open('before_cita.jpg')
                    after = Image.open('after_cita.jpg')
                    if list(before.getdata()) == list(after.getdata()):
                        assert(False), "Did register the cita"
                    else:
                        print "Cita was registered"

                    #### if you wish to remove images from folder, uncomment following lines:###
                    '''
                    os.remove(before_cita.jpg)
                    os.remove(after_cita.jpg)
                    '''

                    print " Cita --> OK"
                    time.sleep(3)
                    p_driver.quit()
                    driver.quit()

                elif modulo == "ProgramarCitaGalenNuevoP":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCitaNuevo(driver)
                    print " Cita --> OK"
                    driver.quit

                elif modulo == "DoctorProgramarCitaMinorCont":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCitaMinorCont(driver)
                    print " Cita --> OK"
                    driver.quit

                elif modulo == "reAgendarCancelarCita":
                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCita(driver)
                    print " Cita --> OK"

                    print "Proceso: reAgendarCita"
                    reAgendarCita(driver)
                    print "reAgendarCita --> OK"

                    print "Proceso: cancelarCita"
                    cancelarCita(driver)
                    print "cancelarCita --> OK"

                    driver.quit

                elif modulo == "DatosdelConsultorio":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DatosdelConsultorio(driver)
                    print " Doctor Programar Cita --> OK"

                elif modulo == "ManejoDeSecretarias":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Manejo de Secretarias"
                    ManejoDeSecretarias(driver)
                    print "Menejo de Secretarias --> OK"

                    driver.quit

                elif modulo == "ManejoDeMonedas":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Manejo de monedas"
                    ManejoDeMonedas(driver)
                    print "Menejo de monedas --> OK"

                    driver.quit

                elif modulo == "ManejoDeConfiguraciones":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Manejo de Configuraciones"
                    ManejoDeConfiguraciones(driver)
                    print "Menejo de Configuraciones --> OK"

                    driver.quit

                elif modulo == "AppAtencionAlCliente":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: App Atencion al Cliente"
                    AppAtencionAlCliente(driver)
                    print "App Atencion al Cliente --> OK"

                    driver.quit

                elif modulo == "AppLogEmails":
                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: App Log Emails"
                    AppLogEmails(driver)
                    print "App Log Emails --> OK"

                    driver.quit

                elif modulo == 'ManejoDoctores':

                    print "Autenticando doctor: " + doctor
                    assert (log_in("jenkins_drchrome@mediconecta.com", "dba123", driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Manejo de Doctores"
                    manejoDoctores(driver)
                    print "Manejo de Doctores --> OK"

                    driver.quit

                print "== Pruebas del doctor finalizadas =="

def log_in(email, pw, driver, ambiente):
    driver.get("http://" + ambiente + ".mediconecta.com/LoginD")
    time.sleep(4)

    assert ("Portal Mediconecta" in driver.title), "Pagina no encontrada"

    driver.find_element_by_id("cphW_txtUsuario").send_keys(email)
    driver.find_element_by_id("cphW_txtPassword").send_keys(pw + Keys.RETURN)
    time.sleep(10)

    if "chrome" not in str(driver):
        time.sleep(6)
        if ambiente == "consultas":
            time.sleep(15)

    if "Terminos" in driver.current_url:
        scroll("cphW_btnAceptar", driver)
        driver.find_element_by_id("cphW_btnAceptar").click()
        print " Aceptar Terminos --> OK"
        time.sleep(3)

    time.sleep(8)
    if "filapacientes" in driver.current_url:
        return "exitoso"
    if "no ha sido activada" in driver.page_source:
        return "inactivo"
    return "fallido"

def log_out(driver):
    scroll_top(driver)
    driver.find_element_by_id("lblUsuario").click() #find log out button
    driver.find_element_by_id("lbCerrar").click() #click on log out
    time.sleep(3)
    if "Ingresa a tu cuenta" in driver.page_source:
        return "exitoso"
    else:
        return "fallido"

    assert("Ingresa a tu cuenta" in driver.page_source), "Failure to log out"

def is_id_in_page(id, driver):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True

def scroll(link_to_be_made_visible, driver):
    time.sleep(2)
    element = driver.find_element_by_id(link_to_be_made_visible)
    driver.execute_script("return arguments[0].scrollIntoView();", element)
    time.sleep(2)

def scroll_top(driver): #scrolls to top of page using log_out botton to identify
    scroll("lblUsuario", driver)

def AtenderPaciente(paciente, driver):
    #if "Fila de Pacientes" in driver.page_source:
    #    driver.find_element_by_link_text("Fila de Pacientes").click()
    #else:
    #    driver.find_element_by_link_text("Patient Queue").click()
    #time.sleep(3)


    if '<a onclick="AtenderPaciente(' and paciente in driver.page_source:
        print " Seleccionando Paciente en Fila"
        botonAtender = driver.execute_script("var trPaciente = document.getElementById('" + paciente + "'); return trPaciente.lastElementChild.lastElementChild;");
        botonAtender.click()
        time.sleep(11)

    else:
        print " No hay pacientes en Fila"
        sys.exit(1)

    #print " Llenando historia medica"
    #Historia_Medica_Dr(driver)
    #print "Proceso PHR --> OK"

    #if "cphW_ucSoap_ucAssesment_ctl00_btnCrear" in driver.page_source:
    #        diagnostico = ["citaTab", "cphW_ucSoap_ucAssesment_ctl00_btnCrear", "s2id_cphW_ucSoap_ucAssesment_ctl00_ucCreate_txtDiagnostico", "cphW_ucSoap_ucAssesment_ctl00_btnCrearDiagnostico", ["cphW_ucSoap_ucAssesment_ctl00_ucCreate_ddlEstatus"]]
    #        #list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl03_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl03_btnEliminarModal"]
    #        testing_different_inputs(diagnostico, 'CEFALEA', '', None, "Definitive", driver)
    #        print " diagnostico --> OK"

    if "GUARDAR Y SALIR" in driver.page_source:
        scroll("cphW_btnGuardarCita", driver)
        driver.find_element_by_id("cphW_btnGuardarCita").click()

        print " Llenando datos de la cita"
        if "cphW_ucSoap_ucSubjective_txtMotivo" in driver.page_source:
            print " Llenando motivo de cita"
            scroll("cphW_ucSoap_ucSubjective_txtMotivo", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_txtMotivo").send_keys("motivo automatizado jenkins")

        if "cphW_ucSoap_ucSubjective_txtHistoria" in driver.page_source:
            print " Llenando historia actual"
            scroll("cphW_ucSoap_ucSubjective_txtHistoria", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_txtHistoria").send_keys("historia actual automatizado jenkins")

        if "cphW_ucSoap_ucSubjective_ddlEva" in driver.page_source:
            print " Llenando dolor eva"
            scroll("cphW_ucSoap_ucSubjective_ddlEva", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_ddlEva").send_keys("1")

        if "cphW_ucSoap_ucObjective_ddlClasificacionRiesgo" in driver.page_source:
            print " Llenando casificacion de riesgo"
            scroll("cphW_ucSoap_ucObjective_ddlClasificacionRiesgo", driver)
            driver.find_element_by_id("cphW_ucSoap_ucObjective_ddlClasificacionRiesgo").send_keys("Bajo")

        if "cphW_ucSoap_ucObjective_ddlTipoConsulta" in driver.page_source:
            print " Llenando tipo de consulta"
            scroll("cphW_ucSoap_ucObjective_ddlTipoConsulta", driver)
            driver.find_element_by_id("cphW_ucSoap_ucObjective_ddlTipoConsulta").send_keys("Nueva consulta")

        if "cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico" in driver.page_source:
            print " Llenando informe medico"
            scroll("cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico").send_keys("informe medico automatizado jenkins")


        print " Guardando cita"
        scroll("cphW_btnGuardarCita", driver)
        driver.find_element_by_id("cphW_btnGuardarCita").click()
        time.sleep(8)

    if "Pudo atender al paciente" in driver.page_source:
        print " Atencion del paciente exitosa"


        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "ButtonSi"))
            )
        except TimeoutException:
            print 'No aparece el boton SI'
            sys.exit(-1)
            driver.quit()
        #finally:

        scroll("ButtonSi", driver)
        driver.find_element_by_id("ButtonSi").click()
        time.sleep(2)


        if driver.find_element_by_id("cphW_btnContinuar"):
        #if "cphW_btnContinuar" in driver.page_source:
            scroll("cphW_btnContinuar", driver)
            driver.find_element_by_id("cphW_btnContinuar").click()
            time.sleep(5)

            if "Resultado de la Cita" in driver.page_source:
                print " Guardando resultado de la cita"
                scroll("hab_ctl00$cphW$ctl02", driver)
                driver.find_element_by_id("hab_ctl00$cphW$ctl02").click()
                time.sleep(5)
                scroll("cphW_btnGuardarCita", driver)
                driver.find_element_by_id("cphW_btnGuardarCita").click()
                time.sleep(5)

            if "Ir a fila de paciente" in driver.page_source:
                print " Redireccionando a Fila de Pacientes"
                time.sleep(5)
                scroll("cphW_btnIrAfiladePaciente", driver)
                driver.find_element_by_id("cphW_btnIrAfiladePaciente").click()

        else:
            print " Boton Continuar no encontrado"

def Historia_Medica_Dr(driver):
    time.sleep(5)
    if 'Acceso directo' in driver.page_source:
        print "PHR Dr En Espanol"

    elif 'Shortcut:' in driver.page_source:
        print "PHR Dr En Ingles"

    alergies = ["cphW_ucHistoriaMedicaDoctor_liAlergias", "cphW_ucHistoriaMedicaDoctor_ctl01_btnCrear", "cphW_ucHistoriaMedicaDoctor_ctl01_ucCreate_txtNombre", "cphW_ucHistoriaMedicaDoctor_ctl01_btnCrearAlergia", None]
    list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl01_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl01_btnEliminarModal"]
    testing_different_inputs(alergies, 'SOMETHING RIGHT Dr', '', list_to_eliminate, None, driver)
    print " Alergia --> OK"
    time.sleep(2)

    ant_patol = ["cphW_ucHistoriaMedicaDoctor_liPatologias", "cphW_ucHistoriaMedicaDoctor_ctl02_btnCrear", "cphW_ucHistoriaMedicaDoctor_ctl02_ucCreate_txtNombre", "cphW_ucHistoriaMedicaDoctor_ctl02_btnCrearAntecedentePatologico", None]
    list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl02_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl02_btnEliminarModal"]
    testing_different_inputs(ant_patol, 'SOMETHING RIGHT Dr', '', list_to_eliminate, None, driver)
    print " Antecedentes Patologicos --> OK"
    time.sleep(2)

    ant_fam = ["cphW_ucHistoriaMedicaDoctor_liAntecedentesFamiliares", "cphW_ucHistoriaMedicaDoctor_ctl03_btnCrear", "cphW_ucHistoriaMedicaDoctor_ctl03_ucCreate_txtNombre", "cphW_ucHistoriaMedicaDoctor_ctl03_btnCrearAntecedenteFamiliar", ["cphW_ucHistoriaMedicaDoctor_ctl03_ucCreate_ddlPariente"]]
    list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl03_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl03_btnEliminarModal"]
    testing_different_inputs(ant_fam, 'SOMETHING RIGHT Dr', '', list_to_eliminate, "Abuela", driver)
    print " Antecedentes Familiares --> OK"
    time.sleep(2)

    dates_to_add = ["cphW_ucHistoriaMedicaDoctor_ctl04_ucCreate_ucFecha_ddlDia", "cphW_ucHistoriaMedicaDoctor_ctl04_ucCreate_ucFecha_ddlMes", "cphW_ucHistoriaMedicaDoctor_ctl04_ucCreate_ucFecha_ddlAnno"]
    ant_qui = ["cphW_ucHistoriaMedicaDoctor_liAntecedentesQuirurgicos", "cphW_ucHistoriaMedicaDoctor_ctl04_btnCrear", "cphW_ucHistoriaMedicaDoctor_ctl04_ucCreate_txtNombre", "cphW_ucHistoriaMedicaDoctor_ctl04_btnCrearAntecedenteQuirurgico", dates_to_add]
    list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl04_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl04_btnEliminarModal"]
    testing_different_inputs(ant_qui, 'SOMETHING RIGHT Dr','',list_to_eliminate, None, driver)
    print " Antecedentes Quirurgicos --> OK"
    time.sleep(2)

    ##ONLY FOR FEMALES
    if is_id_in_page("cphW_ucHistoriaMedicaDoctor_liAntecedentesGinecoObstetricos",driver) == True:
        ant_gin = ["cphW_ucHistoriaMedicaDoctor_liAntecedentesGinecoObstetricos", "cphW_ucHistoriaMedicaDoctor_ctl05_btnCrear", None, "cphW_ucHistoriaMedicaDoctor_ctl05_btnCrearAntecedenteGinecoObstetrico", None]
        list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl05_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl05_btnEliminarModal"]
        testing_different_inputs(ant_gin, 'SOMETHING RIGHT Dr', '', list_to_eliminate, None, driver)
        print " Antecedentes Gineco Obstetricos --> OK"
    time.sleep(2)

    dates_to_add = ["cphW_ucHistoriaMedicaDoctor_ctl06_ucCreate_ucFecha_ddlDia", "cphW_ucHistoriaMedicaDoctor_ctl06_ucCreate_ucFecha_ddlMes", "cphW_ucHistoriaMedicaDoctor_ctl06_ucCreate_ucFecha_ddlAnno"]
    exam = ["cphW_ucHistoriaMedicaDoctor_liExamenes", "cphW_ucHistoriaMedicaDoctor_ctl06_btnCrear", "cphW_ucHistoriaMedicaDoctor_ctl06_ucCreate_txtNombre", "cphW_ucHistoriaMedicaDoctor_ctl06_btnCrearExamen", dates_to_add]
    list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl06_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl06_btnEliminarModal"]
    testing_different_inputs(exam, 'SOMETHING RIGHT Dr', '', list_to_eliminate, None, driver)
    print " Examenes --> OK"
    time.sleep(2)

    end_dates = ["cphW_ucHistoriaMedicaDoctor_ctl07_ucCreate_ucFechaFin_ddlDia", "cphW_ucHistoriaMedicaDoctor_ctl07_ucCreate_ucFechaFin_ddlMes", "cphW_ucHistoriaMedicaDoctor_ctl07_ucCreate_ucFechaFin_ddlAnno"]
    dates_to_add = ["cphW_ucHistoriaMedicaDoctor_ctl07_ucCreate_ucFecha_ddlDia", "cphW_ucHistoriaMedicaDoctor_ctl07_ucCreate_ucFecha_ddlMes", "cphW_ucHistoriaMedicaDoctor_ctl07_ucCreate_ucFecha_ddlAnno"] + end_dates
    list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl07_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl07_btnEliminarModal"]
    hospi = ["cphW_ucHistoriaMedicaDoctor_liHospitalizaciones", "cphW_ucHistoriaMedicaDoctor_ctl07_btnCrear", "cphW_ucHistoriaMedicaDoctor_ctl07_ucCreate_txtNombre", "cphW_ucHistoriaMedicaDoctor_ctl07_btnCrearHospitalizacion", dates_to_add]
    testing_different_inputs(hospi, 'SOMETHING RIGHT Dr', 'something wrong', list_to_eliminate, None, driver)
    print " Hospitalizaciones --> OK"
    time.sleep(2)

    dates_to_add = ["cphW_ucHistoriaMedicaDoctor_ctl08_ucCreate_ucFecha_ddlDia", "cphW_ucHistoriaMedicaDoctor_ctl08_ucCreate_ucFecha_ddlMes", "cphW_ucHistoriaMedicaDoctor_ctl08_ucCreate_ucFecha_ddlAnno"]
    vacu = ["cphW_ucHistoriaMedicaDoctor_liVacunas", "cphW_ucHistoriaMedicaDoctor_ctl08_btnCrear", "cphW_ucHistoriaMedicaDoctor_ctl08_ucCreate_txtNombre", "cphW_ucHistoriaMedicaDoctor_ctl08_btnCrearVacuna", dates_to_add]
    list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl08_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl08_btnEliminarModal"]
    testing_different_inputs(vacu, 'SOMETHING RIGHT Dr', 'something wrong', list_to_eliminate, None, driver)
    print " Vacunas --> OK"
    time.sleep(2)

    habits = ["cphW_ucHistoriaMedicaDoctor_liAntecedentesPersonal", "cphW_ucHistoriaMedicaDoctor_ctl09_btnCrear", None, "cphW_ucHistoriaMedicaDoctor_ctl09_btnCrearAntecedentePersonal", None]
    list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl09_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl09_btnEliminarModal"]
    testing_different_inputs(habits, 'SOMETHING RIGHT Dr', 'something wrong', list_to_eliminate, None, driver)
    print " Habitos y Estilo de Vida --> OK"
    time.sleep(2)

    dates_to_add = ["cphW_ucHistoriaMedicaDoctor_ctl10_ucCreate_ucFecha_ddlDia", "cphW_ucHistoriaMedicaDoctor_ctl10_ucCreate_ucFecha_ddlMes", "cphW_ucHistoriaMedicaDoctor_ctl10_ucCreate_ucFecha_ddlAnno"]
    meds = ["cphW_ucHistoriaMedicaDoctor_liMedicamentos", "cphW_ucHistoriaMedicaDoctor_ctl10_btnCrear", "cphW_ucHistoriaMedicaDoctor_ctl10_ucCreate_txtNombre", "cphW_ucHistoriaMedicaDoctor_ctl10_btnCrearMedicamento",dates_to_add]
    list_to_eliminate = ["cphW_ucHistoriaMedicaDoctor_ctl10_rptTable_btnEliminar_0", "cphW_ucHistoriaMedicaDoctor_ctl10_btnEliminarModal"]
    testing_different_inputs(meds, 'SOMETHING RIGHT Dr', 'something wrong', list_to_eliminate, None, driver)
    print " Medicamentos en Uso --> OK"

def testing_historia_medica(list_needed,input_needed, input_needed_2,driver):

    scroll("ddlPHRdoc", driver)
    driver.find_element_by_id("ddlPHRdoc").click()
    time.sleep(3)
    assert (list_needed[0] in driver.page_source), "Paciente con Acceso Limitado a PHR"
    driver.find_element_by_id(list_needed[0]).click()
    time.sleep(3)
    assert (list_needed[1] in driver.page_source), "Boton Agregar no esta disponible"
    driver.find_element_by_id(list_needed[1]).click()
    #write in all required areas in agregar
    if list_needed[2] != None:
        driver.find_element_by_id(list_needed[2]).send_keys(input_needed)

    if list_needed[4] != None:
        if len(list_needed[4]) == 1:
            time.sleep(4)
            driver.find_element_by_id(list_needed[4][0]).send_keys(input_needed_2)
        if len(list_needed[4]) == 3:
            time.sleep(4)
            driver.find_element_by_id(list_needed[4][0]).send_keys('1')
            time.sleep(4)
            driver.find_element_by_id(list_needed[4][1]).send_keys('1')
            time.sleep(4)
            driver.find_element_by_id(list_needed[4][2]).send_keys('2000')
        if len(list_needed[4]) == 6:
            time.sleep(4)
            driver.find_element_by_id(list_needed[4][0]).send_keys('1')
            time.sleep(4)
            driver.find_element_by_id(list_needed[4][1]).send_keys('1')
            time.sleep(4)
            driver.find_element_by_id(list_needed[4][2]).send_keys('2000')
            time.sleep(4)
            driver.find_element_by_id(list_needed[4][3]).send_keys('1')
            time.sleep(4)
            driver.find_element_by_id(list_needed[4][4]).send_keys('1')
            time.sleep(4)
            driver.find_element_by_id(list_needed[4][5]).send_keys('2000')
    scroll(list_needed[3],driver)
    time.sleep(4)
    driver.find_element_by_id(list_needed[3]).click() #guardar nuevo registro

def eliminar_inputs(list_to_eliminate, driver):
    #eliminar lo que recien agrego
    scroll(list_to_eliminate[0],driver)
    driver.find_element_by_id(list_to_eliminate[0]).click()
    time.sleep(4)
    assert ("que deseas eliminar" in driver.page_source), "Eliminar botton no funciona"
    driver.find_element_by_id(list_to_eliminate[1]).click()
    time.sleep(4)
    assert ("No hay registros" in driver.page_source), "Registro no fue eliminado"

def testing_different_inputs(list_needed,correct,incorrect,list_to_eliminate,extra_input,driver):
    testing_historia_medica(list_needed,correct,extra_input,driver)
    time.sleep(5)
    assert (list_to_eliminate[0] in driver.page_source), "Registro medico added unsuccessfully"
    eliminar_inputs(list_to_eliminate,driver)
    ##tests with a wrong input.. use incorrect when testing_historia_medica

def Recuperar_Usuario(Nacionalidad, Cedula, dia, mes, anno, driver, ambiente):
    driver.get("http://" + ambiente + ".mediconecta.com/LoginD")
    time.sleep(5)
    assert ("Portal Mediconecta" in driver.title), "Pagina no encontrada"
    driver.find_element_by_id("cphW_lnkRecuperarUsuario").click()
    time.sleep(3)
    assert ("Nacionalidad" in driver.page_source), "Recuperar usuario no pide datos necesarios"
    driver.find_element_by_id("cphW_ucRecuperarUsuario_ddlPais_ddlPais").send_keys(Nacionalidad)
    driver.find_element_by_id("cphW_ucRecuperarUsuario_txtCedula").send_keys(Cedula)
    driver.find_element_by_id("cphW_ucRecuperarUsuario_ucFecha_ddlDia").send_keys(dia)
    driver.find_element_by_id("cphW_ucRecuperarUsuario_ucFecha_ddlMes").send_keys(mes)
    driver.find_element_by_id("cphW_ucRecuperarUsuario_ucFecha_ddlAnno").send_keys(anno + Keys.RETURN)
    time.sleep(4)
    if "Te enviamos un correo con tu nombre de usuario" in driver.page_source: #username recovery was successful
        return "Success"
    elif "proporcionada no corresponde" in driver.page_source: #information inputted doesnt correspond to any accound
        return "Fail"
    else: #information inputted corresponds to an account that is inactive
        return "inactive"
    #driver.find_element_by_id("cphW_btnCerrarRecuperarUsuario").click()

def Recuperar_Contrasena(email, driver, ambiente):
    driver.get("http://" + ambiente + ".mediconecta.com/LoginD")
    time.sleep(5)
    assert ("Portal Mediconecta" in driver.title), "Pagina no encontrada"
    driver.find_element_by_id("cphW_lnkRecuperarPassword").click()
    time.sleep(5)
    assert ("Nombre de Usuario" in driver.page_source), "Recuperar contrasena no pide usuario"
    driver.find_element_by_id("cphW_ucRecuperarPassword_txtUsuario").send_keys(email + Keys.RETURN)
    time.sleep(5)
    if "Te enviamos un correo con un" in driver.page_source: #password recovery was successful
        return "Success"
    elif "inactivo" in driver.page_source: #email inputted corresponds to inactive account
        return "Inactive"
    return "Fail" #password recovery was not successful

def log_in_p(email, pw, driver, ambiente):
    driver.get("http://" + ambiente + ".mediconecta.com")
    time.sleep(3)

    if "Login" in driver.title:
        print ' Autenticando Paciente..'
        scroll("cphW_txtUsuario", driver)
        driver.find_element_by_id("cphW_txtUsuario").send_keys(email)
        scroll("cphW_txtPassword", driver)
        driver.find_element_by_id("cphW_txtPassword").send_keys(pw + Keys.RETURN)
        time.sleep(5)

        if "Terminos" in driver.current_url:
            print ' Aceptando terminos..'
            scroll("cphW_btnAceptar", driver)
            driver.find_element_by_id("cphW_btnAceptar").click()
            print " Aceptar Terminos --> OK"
            time.sleep(3)

        if "Solicitud de Citas" in driver.page_source:
            return "exitoso"
        elif "e-visit" in driver.page_source:
            return "exitoso"
        elif "El usuario ingresado" in driver.page_source:
            return "inactivo"
        else:
            return "fallido"
    else:
        sys.exit(-1)

def CitaODTokbox(driver, ambiente, atender):
    time.sleep(5)
    site = 'portal'

    if "INICIAR VIDEO-CONSULTA" in driver.page_source: #if login works
        site = 'hubsalud'
        print " Hub de Salud en Espanol"
    elif "START E-VISIT" in driver.page_source: #if login works
        site = 'hubsalud'
        print " Hub de Salud en Ingles"
    elif "Solicitud de Citas" in driver.page_source: #if login works
        print " Portal en Espanol"
    elif "e-visit" in driver.page_source: #if login works
        print " Portal en Ingles"


    if site == 'hubsalud':
        scroll("cphW_uccitasondemand_btnSolicitarCitaHub", driver)
        driver.find_element_by_id("cphW_uccitasondemand_btnSolicitarCitaHub").click()

        try:
            element = WebDriverWait(driver,20).until(
                EC.presence_of_element_located((By.ID, "cphW_uccitasondemand_btnOnDemandIntermedia"))
            )
        except TimeoutException:
            print "Page not loaded"

        time.sleep(2)
        driver.find_element_by_id("cphW_uccitasondemand_btnOnDemandIntermedia").click()
    else:
        scroll("cphW_uccitasondemand_btnSolicitarCita", driver)
        driver.find_element_by_id("cphW_uccitasondemand_btnSolicitarCita").click()

    time.sleep(6)

    if "cphW_uccitasondemand_ddlDependientes" in driver.page_source:
        element = driver.find_element_by_xpath('//*[(@id = "cphW_uccitasondemand_ddlDependientes")]')
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "a0HZ0000007gYqP":
                option.click()
                time.sleep(1)
                driver.find_element_by_id('cphW_uccitasondemand_btnAceptar').click()
                break
    elif "cphW_uccitasondemand_upCitasOnDemandModalBody" in driver.page_source:
        scroll('cphW_uccitasondemand_rblParaQuien_0',driver)
        driver.find_element_by_id('cphW_uccitasondemand_rblParaQuien_0').click()
        time.sleep(1)
        driver.find_element_by_id('cphW_uccitasondemand_btnContinuarDep').click()
        time.sleep(3)

    print " Solicitar cita --> OK"


    ### Dont really understand why the following is in here, what does it do?###
    ###commented out because it found the if but could not find the id###
    '''
    if "son personales y generan un historial" or "Medical consultations are personal and create a medical history" in driver.page_source:
        scroll("uniform-cphW_uccitasondemand_rblParaQuien_0", driver)
        driver.find_element_by_id("uniform-cphW_uccitasondemand_rblParaQuien_0").click()
        scroll("cphW_uccitasondemand_btnContinuarDep", driver)
        driver.find_element_by_id("cphW_uccitasondemand_btnContinuarDep").click()
        print " Seleccionar Paciente --> OK"
        time.sleep(5)


        if "necesaria para que te pueda atender un Doctor" or "The setup is necessary to be able to talk to the Doctor" in driver.page_source:
            print " ValidacionVC.."
            #time.sleep(3)
            #if "Modulos/Cita/Cita" in driver.current_url:
            if "Tiempo de Espera Estimado" or "Estimated Wait Time" in driver.page_source:
                print " Entrando a Sala de Espera.."
                #time.sleep(3)
                if atender == 'no':
                    print " Finalizando Cita.."
                    scroll("cphW_ucCita_btnCitaFinalizarPpal", driver)
                    driver.find_element_by_id("cphW_ucCita_btnCitaFinalizarPpal").click()
                    time.sleep(3)
                    if "si prefieres te contactamos cuando" or "if you want we will contact you when" in driver.page_source:
                        scroll("cphW_ucCita_btnAceptarFinalizar", driver)
                        driver.find_element_by_id("cphW_ucCita_btnAceptarFinalizar").click()
                    print " Cita --> OK"
                else:
                    print " Paciente esperando ser atendido.."

            else:
                print " Cita no realizada1"
        else:
            print " Cita no realizada2"
    '''

def historiaCitas(paciente, driver):
    if '<a onclick="AtenderPaciente(' and paciente in driver.page_source:
        print " Seleccionando Paciente en Fila"
        botonAtender = driver.execute_script("var trPaciente = document.getElementById('" + paciente + "'); return trPaciente.lastElementChild.lastElementChild;");
        botonAtender.click()
    else:
        print " No hay pacientes en Fila"
        sys.exit(1)

    time.sleep(6)
    print "Chequeando la historia de citas del paciente.."
    print " Drop down selection"
    dropDown = driver.find_element_by_id("ddlPHRdoc")
    dropDown.click()
    time.sleep(1)

    print " Historico Citas selection"
    historiaTab = driver.find_element_by_xpath("//*[@id='cphW_ucHistoriaMedicaDoctor_liHistoricoCitas']/a")
    historiaTab.click()
    assert("dropdown-header menuOption active" in driver.page_source), "Did not go to the right page"
    time.sleep(2)

    print " Ver selection"
    driver.save_screenshot("before.jpg")
    verBtn = driver.find_element_by_css_selector("#cphW_ucHistoriaMedicaDoctor_ctl11_rptTable_btnVer_41 > i")
    verBtn.click()
    time.sleep(5)
    driver.save_screenshot("after.jpg")

    #following is to compare the two screenshots, confirming change
    '''
    before = convert("before.jpg")
    after =  convert("after.jpg")
    baseline = c2d(before, before, mode="same")
    compare = c2d(before, after, mode="same")
    baseline_num = baseline.max()
    new_num = compare.max()
    '''

    before = Image.open('before.jpg')
    after = Image.open('after.jpg')
    if list(before.getdata()) == list(after.getdata()):
        assert(False), "Did not go to the right page"
    else:
        pass

    #### if you wish to remove images from folder, uncomment following lines:###
    '''
    os.remove(before.jpg)
    os.remove(after.jpg)
    '''

    time.sleep(2)

def Pruebas_de_Diagnostico(paciente, driver):

    if '<a onclick="AtenderPaciente(' and paciente in driver.page_source:
        print " Seleccionando Paciente en Fila"
        botonAtender = driver.execute_script("var trPaciente = document.getElementById('" + paciente + "'); return trPaciente.lastElementChild.lastElementChild;");
        botonAtender.click()
        time.sleep(5)
    else:
        print " No hay pacientes en Fila"
        sys.exit(1)

    time.sleep(5)
    if "GUARDAR Y SALIR" not in driver.page_source and "SAVE AND EXIT" not in driver.page_source:
        print "website not loaded yet"
        time.sleep(9)

    if "GUARDAR Y SALIR" in driver.page_source or "SAVE AND EXIT" in driver.page_source:
        scroll("cphW_btnGuardarCita", driver)
        driver.find_element_by_id("cphW_btnGuardarCita").click()

        print " Llenando datos de la cita"
        time.sleep(4)

        if "cphW_ucSoap_ucSubjective_txtMotivo" in driver.page_source:
            print " Llenando motivo de cita"
            scroll("cphW_ucSoap_ucSubjective_txtMotivo", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_txtMotivo").send_keys("motivo automatizado jenkins")

        if "cphW_ucSoap_ucSubjective_txtHistoria" in driver.page_source:
            print " Llenando historia actual"
            scroll("cphW_ucSoap_ucSubjective_txtHistoria", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_txtHistoria").send_keys("historia actual automatizado jenkins")

        if "cphW_ucSoap_ucSubjective_ddlEva" in driver.page_source:
            print " Llenando dolor eva"
            scroll("cphW_ucSoap_ucSubjective_ddlEva", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_ddlEva").send_keys("1")

        if "cphW_ucSoap_ucObjective_ddlClasificacionRiesgo" in driver.page_source:
            print " Llenando casificacion de riesgo"
            scroll("cphW_ucSoap_ucObjective_ddlClasificacionRiesgo", driver)
            driver.find_element_by_id("cphW_ucSoap_ucObjective_ddlClasificacionRiesgo").send_keys("Bajo")

        if "cphW_ucSoap_ucObjective_ddlTipoConsulta" in driver.page_source:
            print " Llenando tipo de consulta"
            scroll("cphW_ucSoap_ucObjective_ddlTipoConsulta", driver)
            driver.find_element_by_id("cphW_ucSoap_ucObjective_ddlTipoConsulta").send_keys("Nueva consulta")

        if "cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico" in driver.page_source:
            print " Llenando informe medico"
            scroll("cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico").send_keys("informe medico automatizado jenkins")

        if "cphW_ucSoap_ucAssesment_ctl00_btnCrear" in driver.page_source:
            print "Agregar Diagnosticos"
            scroll("cphW_ucSoap_ucAssesment_ctl00_btnCrear", driver)
            driver.find_element_by_id("cphW_ucSoap_ucAssesment_ctl00_btnCrear").click()
            assert(u"Nuevo Diagnóstico" in driver.page_source or "New Diagnosis" in page_source), u"Not on the New Diagnosis page"

            scroll("s2id_autogen3", driver)
            driver.find_element_by_xpath("//*[@id='s2id_autogen3']").click()
            driver.find_element_by_xpath("//*[@id='s2id_autogen3']").send_keys("sarampion")
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='s2id_autogen3']").send_keys(Keys.ENTER)

            scroll("cphW_ucSoap_ucAssesment_ctl00_ucCreate_ddlEstatus", driver)
            driver.find_element_by_id("cphW_ucSoap_ucAssesment_ctl00_ucCreate_ddlEstatus").click()
            driver.find_element_by_id("cphW_ucSoap_ucAssesment_ctl00_ucCreate_ddlEstatus").send_keys("p")

            scroll("cphW_ucSoap_ucAssesment_ctl00_btnCrearDiagnostico", driver)
            driver.find_element_by_id("cphW_ucSoap_ucAssesment_ctl00_btnCrearDiagnostico").click()

            assert("SARAMPION" in driver.page_source), "Diagnosis did not save"

            print "Agregar Diagnosticos --> OK"
            time.sleep(5)

        print " Guardando cita"
        scroll("cphW_btnGuardarCita", driver)
        driver.find_element_by_id("cphW_btnGuardarCita").click()
        time.sleep(8)

    if "Pudo atender al paciente" in driver.page_source:
        print " Atencion del paciente exitosa"

        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "ButtonSi"))
            )
        except TimeoutException:
            print 'No aparece el boton SI'
            sys.exit(-1)
            driver.quit()
        #finally:

        scroll("ButtonSi", driver)
        driver.find_element_by_id("ButtonSi").click()
        time.sleep(2)


        if driver.find_element_by_id("cphW_btnContinuar"):
        #if "cphW_btnContinuar" in driver.page_source:
            scroll("cphW_btnContinuar", driver)
            driver.find_element_by_id("cphW_btnContinuar").click()
            time.sleep(5)

            if "Resultado de la Cita" in driver.page_source:
                print " Guardando resultado de la cita"
                scroll("hab_ctl00$cphW$ctl02", driver)
                driver.find_element_by_id("hab_ctl00$cphW$ctl02").click()
                time.sleep(5)
                scroll("cphW_btnGuardarCita", driver)
                driver.find_element_by_id("cphW_btnGuardarCita").click()
                time.sleep(5)
            time.sleep(10)
            if "Ir a fila de paciente" in driver.page_source:
                print " Redireccionando a Fila de Pacientes"
                scroll("cphW_btnIrAfiladePaciente", driver)
                driver.find_element_by_id("cphW_btnIrAfiladePaciente").click()

        else:
            print " Boton Continuar no encontrado"

def Pruebas_de_Prescripciones(paciente, driver):

    if '<a onclick="AtenderPaciente(' and paciente in driver.page_source:
        print " Seleccionando Paciente en Fila"
        botonAtender = driver.execute_script("var trPaciente = document.getElementById('" + paciente + "'); return trPaciente.lastElementChild.lastElementChild;");
        botonAtender.click()
        time.sleep(5)
    else:
        print " No hay pacientes en Fila"
        sys.exit(1)

    time.sleep(5)
    if "GUARDAR Y SALIR" not in driver.page_source and "SAVE AND EXIT" not in driver.page_source:
        print "website not loaded yet"
        time.sleep(9)

    if "GUARDAR Y SALIR" in driver.page_source or "SAVE AND EXIT" in driver.page_source:
        scroll("cphW_btnGuardarCita", driver)
        driver.find_element_by_id("cphW_btnGuardarCita").click()

        print " Llenando datos de la cita"
        time.sleep(4)

        if "cphW_ucSoap_ucSubjective_txtMotivo" in driver.page_source:
            print " Llenando motivo de cita"
            scroll("cphW_ucSoap_ucSubjective_txtMotivo", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_txtMotivo").send_keys("motivo automatizado jenkins")

        if "cphW_ucSoap_ucSubjective_txtHistoria" in driver.page_source:
            print " Llenando historia actual"
            scroll("cphW_ucSoap_ucSubjective_txtHistoria", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_txtHistoria").send_keys("historia actual automatizado jenkins")

        if "cphW_ucSoap_ucSubjective_ddlEva" in driver.page_source:
            print " Llenando dolor eva"
            scroll("cphW_ucSoap_ucSubjective_ddlEva", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_ddlEva").send_keys("1")

        if "cphW_ucSoap_ucObjective_ddlClasificacionRiesgo" in driver.page_source:
            print " Llenando casificacion de riesgo"
            scroll("cphW_ucSoap_ucObjective_ddlClasificacionRiesgo", driver)
            driver.find_element_by_id("cphW_ucSoap_ucObjective_ddlClasificacionRiesgo").send_keys("Bajo")

        if "cphW_ucSoap_ucObjective_ddlTipoConsulta" in driver.page_source:
            print " Llenando tipo de consulta"
            scroll("cphW_ucSoap_ucObjective_ddlTipoConsulta", driver)
            driver.find_element_by_id("cphW_ucSoap_ucObjective_ddlTipoConsulta").send_keys("Nueva consulta")

        if "cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico" in driver.page_source:
            print " Llenando informe medico"
            scroll("cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico").send_keys("informe medico automatizado jenkins")

        if "cphW_ucSoap_ucPlan_ctl00_btnCrear" in driver.page_source:
            print "Agregar Prescripciones"
            scroll("cphW_ucSoap_ucPlan_ctl00_btnCrear", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl00_btnCrear").click()
            assert(u"Nueva Prescripción" in driver.page_source or "New Prescription" in page_source), u"Not on the New Prescription page"

            if "s2id_autogen5" in driver.page_source:
                scroll("s2id_autogen5", driver)
                driver.find_element_by_xpath("//*[@id='s2id_autogen5']").click()
                driver.find_element_by_xpath("//*[@id='s2id_autogen5']").send_keys("escalol")
                time.sleep(1)
                driver.find_element_by_xpath("//*[@id='s2id_autogen5']").send_keys(Keys.ENTER)


                scroll("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion", driver)
                driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion").click()

            elif "s2id_autogen11" in driver.page_source:
                scroll("s2id_autogen11", driver)
                driver.find_element_by_xpath("//*[@id='s2id_autogen11']").click()
                driver.find_element_by_xpath("//*[@id='s2id_autogen11']").send_keys("escalol")
                time.sleep(1)
                driver.find_element_by_xpath("//*[@id='s2id_autogen11']").send_keys(Keys.ENTER)

                scroll("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion", driver)
                driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion").click()

        time.sleep(3)
        assert("ESCALOL" in driver.page_source), "Perscription did not save"
        print "Agregar Prescripciones --> OK"
        time.sleep(3)
        print " Guardando cita"
        scroll("cphW_btnGuardarCita", driver)
        driver.find_element_by_id("cphW_btnGuardarCita").click()
        time.sleep(8)

    if "Pudo atender al paciente" in driver.page_source:
        print " Atencion del paciente exitosa"

        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "ButtonSi"))
            )
        except TimeoutException:
            print 'No aparece el boton SI'
            sys.exit(-1)
            driver.quit()
        #finally:

        scroll("ButtonSi", driver)
        driver.find_element_by_id("ButtonSi").click()
        time.sleep(2)


        if driver.find_element_by_id("cphW_btnContinuar"):
        #if "cphW_btnContinuar" in driver.page_source:
            scroll("cphW_btnContinuar", driver)
            driver.find_element_by_id("cphW_btnContinuar").click()
            time.sleep(5)

            if "Resultado de la Cita" in driver.page_source:
                print " Guardando resultado de la cita"
                scroll("hab_ctl00$cphW$ctl02", driver)
                driver.find_element_by_id("hab_ctl00$cphW$ctl02").click()
                time.sleep(5)
                scroll("cphW_btnGuardarCita", driver)
                driver.find_element_by_id("cphW_btnGuardarCita").click()
                time.sleep(5)

            time.sleep(10)
            if "Ir a fila de paciente" in driver.page_source:
                print " Redireccionando a Fila de Pacientes"
                scroll("cphW_btnIrAfiladePaciente", driver)
                driver.find_element_by_id("cphW_btnIrAfiladePaciente").click()

        else:
            print " Boton Continuar no encontrado"

def Pruebas_de_Examenes(paciente, driver):

    if '<a onclick="AtenderPaciente(' and paciente in driver.page_source:
        print " Seleccionando Paciente en Fila"
        botonAtender = driver.execute_script("var trPaciente = document.getElementById('" + paciente + "'); return trPaciente.lastElementChild.lastElementChild;");
        botonAtender.click()
        time.sleep(5)
    else:
        print " No hay pacientes en Fila"
        sys.exit(1)

    time.sleep(5)
    if "GUARDAR Y SALIR" not in driver.page_source and "SAVE AND EXIT" not in driver.page_source:
        print "website not loaded yet"
        time.sleep(9)

    if "GUARDAR Y SALIR" in driver.page_source or "SAVE AND EXIT" in driver.page_source:
        scroll("cphW_btnGuardarCita", driver)
        driver.find_element_by_id("cphW_btnGuardarCita").click()

        print " Llenando datos de la cita"
        time.sleep(4)

        if "cphW_ucSoap_ucSubjective_txtMotivo" in driver.page_source:
            print " Llenando motivo de cita"
            scroll("cphW_ucSoap_ucSubjective_txtMotivo", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_txtMotivo").send_keys("motivo automatizado jenkins")

        if "cphW_ucSoap_ucSubjective_txtHistoria" in driver.page_source:
            print " Llenando historia actual"
            scroll("cphW_ucSoap_ucSubjective_txtHistoria", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_txtHistoria").send_keys("historia actual automatizado jenkins")

        if "cphW_ucSoap_ucSubjective_ddlEva" in driver.page_source:
            print " Llenando dolor eva"
            scroll("cphW_ucSoap_ucSubjective_ddlEva", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_ddlEva").send_keys("1")

        if "cphW_ucSoap_ucObjective_ddlClasificacionRiesgo" in driver.page_source:
            print " Llenando casificacion de riesgo"
            scroll("cphW_ucSoap_ucObjective_ddlClasificacionRiesgo", driver)
            driver.find_element_by_id("cphW_ucSoap_ucObjective_ddlClasificacionRiesgo").send_keys("Bajo")

        if "cphW_ucSoap_ucObjective_ddlTipoConsulta" in driver.page_source:
            print " Llenando tipo de consulta"
            scroll("cphW_ucSoap_ucObjective_ddlTipoConsulta", driver)
            driver.find_element_by_id("cphW_ucSoap_ucObjective_ddlTipoConsulta").send_keys("Nueva consulta")

        if "cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico" in driver.page_source:
            print " Llenando informe medico"
            scroll("cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico").send_keys("informe medico automatizado jenkins")

        if "cphW_ucSoap_ucPlan_ctl01_btnCrear" in driver.page_source:
            print "Agregar Examenes"
            scroll("cphW_ucSoap_ucPlan_ctl01_btnCrear", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl01_btnCrear").click()
            assert(u"Nuevo Examen" in driver.page_source or "New Lab Test" in page_source), u"Not on the New Lab Test page"

            scroll("cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre", driver)
            driver.find_element_by_xpath("//*[@id='cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre']").click()
            driver.find_element_by_xpath("//*[@id='cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre']").send_keys("TEST1")
            driver.find_element_by_xpath("//*[@id='cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre']").send_keys(Keys.ENTER)

            scroll("cphW_ucSoap_ucPlan_ctl01_btnCrearExamen", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl01_btnCrearExamen").click()

        time.sleep(3)
        assert("TEST1" in driver.page_source), "New lab test did not save"
        print "Agregar Examenes --> OK"
        time.sleep(2)

        print " Guardando cita"
        scroll("cphW_btnGuardarCita", driver)
        driver.find_element_by_id("cphW_btnGuardarCita").click()
        time.sleep(8)

    if "Pudo atender al paciente" in driver.page_source:
        print " Atencion del paciente exitosa"

        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "ButtonSi"))
            )
        except TimeoutException:
            print 'No aparece el boton SI'
            sys.exit(-1)
            driver.quit()
        #finally:

        scroll("ButtonSi", driver)
        driver.find_element_by_id("ButtonSi").click()
        time.sleep(2)


        if driver.find_element_by_id("cphW_btnContinuar"):
        #if "cphW_btnContinuar" in driver.page_source:
            scroll("cphW_btnContinuar", driver)
            driver.find_element_by_id("cphW_btnContinuar").click()
            time.sleep(5)

            if "Resultado de la Cita" in driver.page_source:
                print " Guardando resultado de la cita"
                scroll("hab_ctl00$cphW$ctl02", driver)
                driver.find_element_by_id("hab_ctl00$cphW$ctl02").click()
                time.sleep(5)
                scroll("cphW_btnGuardarCita", driver)
                driver.find_element_by_id("cphW_btnGuardarCita").click()
                time.sleep(5)
            time.sleep(10)
            if "Ir a fila de paciente" in driver.page_source:
                print " Redireccionando a Fila de Pacientes"
                scroll("cphW_btnIrAfiladePaciente", driver)
                driver.find_element_by_id("cphW_btnIrAfiladePaciente").click()

        else:
            print " Boton Continuar no encontrado"

def Diagnostico(driver):
    if "cphW_ucSoap_ucAssesment_ctl00_btnCrear" in driver.page_source:
        print "Agregar Diagnosticos"
        scroll("cphW_ucSoap_ucAssesment_ctl00_btnCrear", driver)
        driver.find_element_by_id("cphW_ucSoap_ucAssesment_ctl00_btnCrear").click()
        assert(u"Nuevo Diagnóstico" in driver.page_source or "New Diagnosis" in page_source), u"Not on the New Diagnosis page"

        scroll("s2id_autogen3", driver)
        #driver.find_element_by_xpath("//*[@id='s2id_autogen3']").click()
        driver.find_element_by_xpath("//*[@id='s2id_autogen3']").send_keys("sarampion")
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='s2id_autogen3']").send_keys(Keys.ENTER)

        time.sleep(2)
        scroll("cphW_ucSoap_ucAssesment_ctl00_ucCreate_ddlEstatus", driver)
        #driver.find_element_by_id("cphW_ucSoap_ucAssesment_ctl00_ucCreate_ddlEstatus").click()
        driver.find_element_by_id("cphW_ucSoap_ucAssesment_ctl00_ucCreate_ddlEstatus").send_keys("p")

        time.sleep(2)
        scroll("cphW_ucSoap_ucAssesment_ctl00_btnCrearDiagnostico", driver)
        driver.find_element_by_id("cphW_ucSoap_ucAssesment_ctl00_btnCrearDiagnostico").click()

        assert("SARAMPION" in driver.page_source), "Diagnosis did not save"

        print "Agregar Diagnosticos --> OK"
        time.sleep(5)
    else:
        print "No 'diagnostico' button found"

def Prescripciones(driver):
    if "cphW_ucSoap_ucPlan_ctl00_btnCrear" in driver.page_source:
        print "Agregar Prescripciones"
        scroll("cphW_ucSoap_ucPlan_ctl00_btnCrear", driver)
        driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl00_btnCrear").click()
        assert(u"Nueva Prescripción" in driver.page_source or "New Prescription" in page_source), u"Not on the New Prescription page"

        if "s2id_autogen5" in driver.page_source:
            scroll("s2id_autogen5", driver)
            #driver.find_element_by_xpath("//*[@id='s2id_autogen5']").click()
            driver.find_element_by_xpath("//*[@id='s2id_autogen5']").send_keys("escalol")
            time.sleep(2)
            driver.find_element_by_xpath("//*[@id='s2id_autogen5']").send_keys(Keys.ENTER)
            time.sleep(2)


            scroll("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion").click()
            assert("ESCALOL" in driver.page_source), "Perscription did not save"

            print "Agregar Prescripciones --> OK"
            time.sleep(5)
        elif "s2id_autogen11" in driver.page_source:
            scroll("s2id_autogen11", driver)
            #driver.find_element_by_xpath("//*[@id='s2id_autogen11']").click()
            driver.find_element_by_xpath("//*[@id='s2id_autogen11']").send_keys("escalol")
            time.sleep(2)
            driver.find_element_by_xpath("//*[@id='s2id_autogen11']").send_keys(Keys.ENTER)
            time.sleep(2)


            scroll("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion").click()
            assert("ESCALOL" in driver.page_source), "Perscription did not save"

            print "Agregar Prescripciones --> OK"
            time.sleep(5)
    else:
        print "No 'Prescripciones' button found"

def Examenes(driver):
    if "cphW_ucSoap_ucPlan_ctl01_btnCrear" in driver.page_source:
        print "Agregar Examenes"
        scroll("cphW_ucSoap_ucPlan_ctl01_btnCrear", driver)
        driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl01_btnCrear").click()
        assert(u"Nuevo Examen" in driver.page_source or "New Lab Test" in page_source), u"Not on the New Lab Test page"

        scroll("cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre", driver)
        #driver.find_element_by_xpath("//*[@id='cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre']").click()
        driver.find_element_by_xpath("//*[@id='cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre']").send_keys("TEST1")
        driver.find_element_by_xpath("//*[@id='cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre']").send_keys(Keys.ENTER)
        time.sleep(3)

        scroll("cphW_ucSoap_ucPlan_ctl01_btnCrearExamen", driver)
        driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl01_btnCrearExamen").click()
        assert("TEST1" in driver.page_source), "New lab test did not save"
        print "Agregar Examenes --> OK"
        time.sleep(5)
    else:
        print "No 'Examenes' button found"

def AtenderPacienteConDPE(paciente, driver):
    if '<a onclick="AtenderPaciente(' and paciente in driver.page_source:
        print " Seleccionando Paciente en Fila"
        botonAtender = driver.execute_script("var trPaciente = document.getElementById('" + paciente + "'); return trPaciente.lastElementChild.lastElementChild;");
        botonAtender.click()
        time.sleep(11)
    else:
        print " No hay pacientes en Fila"
        sys.exit(1)

    if "GUARDAR Y SALIR" in driver.page_source:
        scroll("cphW_btnGuardarCita", driver)
        driver.find_element_by_id("cphW_btnGuardarCita").click()

        print " Llenando datos de la cita"
        if "cphW_ucSoap_ucSubjective_txtMotivo" in driver.page_source:
            print " Llenando motivo de cita"
            scroll("cphW_ucSoap_ucSubjective_txtMotivo", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_txtMotivo").send_keys("motivo automatizado jenkins")

        if "cphW_ucSoap_ucSubjective_txtHistoria" in driver.page_source:
            print " Llenando historia actual"
            scroll("cphW_ucSoap_ucSubjective_txtHistoria", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_txtHistoria").send_keys("historia actual automatizado jenkins")

        if "cphW_ucSoap_ucSubjective_ddlEva" in driver.page_source:
            print " Llenando dolor eva"
            scroll("cphW_ucSoap_ucSubjective_ddlEva", driver)
            driver.find_element_by_id("cphW_ucSoap_ucSubjective_ddlEva").send_keys("1")

        if "cphW_ucSoap_ucObjective_ddlClasificacionRiesgo" in driver.page_source:
            print " Llenando casificacion de riesgo"
            scroll("cphW_ucSoap_ucObjective_ddlClasificacionRiesgo", driver)
            driver.find_element_by_id("cphW_ucSoap_ucObjective_ddlClasificacionRiesgo").send_keys("Bajo")

        if "cphW_ucSoap_ucObjective_ddlTipoConsulta" in driver.page_source:
            print " Llenando tipo de consulta"
            scroll("cphW_ucSoap_ucObjective_ddlTipoConsulta", driver)
            driver.find_element_by_id("cphW_ucSoap_ucObjective_ddlTipoConsulta").send_keys("Nueva consulta")

        if "cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico" in driver.page_source:
            print " Llenando informe medico"
            scroll("cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ucIndicaciones_txtInformeMedico").send_keys("informe medico automatizado jenkins")

        Diagnostico(driver)
        time.sleep(3)
        Prescripciones(driver)
        time.sleep(3)
        Examenes(driver)

        print " Guardando cita"
        scroll("cphW_btnGuardarCita", driver)
        driver.find_element_by_id("cphW_btnGuardarCita").click()
        time.sleep(8)

    if "Pudo atender al paciente" in driver.page_source:
        print " Atencion del paciente exitosa"

        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "ButtonSi"))
            )
        except TimeoutException:
            print 'No aparece el boton SI'
            sys.exit(-1)
            driver.quit()

        scroll("ButtonSi", driver)
        driver.find_element_by_id("ButtonSi").click()
        time.sleep(2)

        if driver.find_element_by_id("cphW_btnContinuar"):
            scroll("cphW_btnContinuar", driver)
            driver.find_element_by_id("cphW_btnContinuar").click()
            time.sleep(5)

            if "Resultado de la Cita" in driver.page_source:
                print " Guardando resultado de la cita"
                scroll("hab_ctl00$cphW$ctl02", driver)
                driver.find_element_by_id("hab_ctl00$cphW$ctl02").click()
                time.sleep(5)
                scroll("cphW_btnGuardarCita", driver)
                driver.find_element_by_id("cphW_btnGuardarCita").click()
                time.sleep(5)

            if "Ir a fila de paciente" in driver.page_source:
                print " Redireccionando a Fila de Pacientes"
                scroll("cphW_btnIrAfiladePaciente", driver)
                driver.find_element_by_id("cphW_btnIrAfiladePaciente").click()

        else:
            print " Boton Continuar no encontrado"

def DoctorProgramarCita(driver):
    time.sleep(5)
    if 'CITAS PROGRAMADAS' in driver.page_source:
        driver.find_element_by_link_text('CITAS PROGRAMADAS').click()
        time.sleep(5)

        scroll("cphW_uccitasprogramadasdr_btnProgramarCita", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_btnProgramarCita").click()
        time.sleep(5)

        if "cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios" in driver.page_source:
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "001Z000000VEOKDIA5":
                    option.click()
                    break

        print "Escogiendo doctor: Demo AS"
        assert("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores" in driver.page_source), "Cannot choose doctor"
        scroll("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores", driver)
        element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "003Z000001LIAF5IAP":
                option.click()
                break

        scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnContinuarEscogerConsulDoc", driver)
        driver.find_element_by_xpath("//*[(@id = 'cphW_uccitasprogramadasdr_btnContinuarEscogerConsulDoc')]").click()
        time.sleep(3)
        print "Cita para un menor de edad? No"
        assert("cphW_uccitasprogramadasdr_btnconfirmarMenor_No" in driver.page_source), "Not on the right page"
        scroll("cphW_uccitasprogramadasdr_btnconfirmarMenor_No", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_btnconfirmarMenor_No").click()
        time.sleep(3)

        print "Escogiendo paciente"
        assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda" in driver.page_source), "Not on the right page_source"
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").click()
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").send_keys("jenkins chrome tokbox")
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").send_keys(Keys.ENTER)
        time.sleep(4)

        if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0" in driver.page_source:
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0").click()
            time.sleep(5)
        else:
            print "no patient was found"

        #getting new time:
        time_of_day = "AM"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        year = current_time[0:4]
        month = current_time[5:7]
        day = current_time[8:10]
        hour = current_time[11:13]
        minuto = current_time[14:16]
        hour = str(int(hour) + 1)
        if int(minuto) > 45:
            minuto = "00"
            hour = str(int(hour) + 1)
        elif int(minuto) < 15:
            minuto = "00"
        else:
            minuto = "30"
        if hour == "25":
            hour = "1"
            time_of_day = "AM"
        if hour == "26":
            hour = "2"
            time_of_day = "AM"
        if int(hour) >= 12 and int(hour) != 24:
            time_of_day = "PM"
        if int(hour) > 12:
            hour = str(int(hour) - 12)

        venezuela_time = str(int(hour) - 1)
        also_v_time = venezuela_time
        if venezuela_time == "0":
            venezuela_time = "12"
            if time_of_day == "PM":
                time_of_day = "AM"
            else:
                time_of_day = "PM"
        if time_of_day == "PM":
            venezuela_time = str(int(venezuela_time) + 12)
        if also_v_time == "12":
            also_v_time = "00"


        assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha" in driver.page_source), "Did not go to the right page"
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").click()
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").send_keys(day + "/" + month + "/" + year)
        driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()
        time.sleep(1)

        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").click()
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").send_keys(hour +':'+ minuto + " " + time_of_day)
        driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()
        time.sleep(1)

        if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta" in driver.page_source:
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys(Keys.BACKSPACE + Keys.BACKSPACE)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys("1")
            time.sleep(1)

        if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas" in driver.page_source:
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas']")
            all_options = element.find_elements_by_tag_name("option")
            currency = None
            for option in all_options:
                if option.get_attribute("value") == "a0nZ00000037vdjIAA":
                    option.click()
                    currency = "USD"
                    print "Pay in USD"
                    break
                elif option.get_attribute("value") == "a0nZ00000037vdeIAA":
                    option.click()
                    currency = "VEF"
                    print "Pay in VEF"
                    break
        assert(currency != None), "No currency found"
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar").click()
        time.sleep(5)

        assert ("cphW_uccitasprogramadasdr_btnProgramarCita" in driver.page_source), "Cita no completada"

        print "Checking if cita was made"
        scroll("uniform-cphW_uccitasprogramadasdr_rblFiltrar", driver)
        driver.find_element_by_id("uniform-cphW_uccitasprogramadasdr_rblFiltrar").click()
        time.sleep(4)

        if "cphW_uccitasprogramadasdr_ddlConsultorios" in driver.page_source:
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlConsultorios']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "001Z000000VEOKDIA5":
                    option.click()
                    break

        time.sleep(5)
        scroll("cphW_uccitasprogramadasdr_ddlDoctores", driver)
        element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlDoctores']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "003Z000001LIAF5IAP":
                option.click()
                break
        time.sleep(6)
        phrase = venezuela_time + ":" + str(minuto) + " - Cita con Pruebas Jenkins Chrome Tokbox"
        also_phrase = also_v_time + ":" + str(minuto) + " - Cita con Pruebas Jenkins Chrome Tokbox"
        assert (phrase in driver.page_source or also_phrase in driver.page_source), "cita no hecha"
        print "Cita made and confirmed"

def DoctorProgramarCitaNuevo(driver):
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    paciente = "Paciente" + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers)
    paciente_apellido = "Smtih" + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers)

    time.sleep(5)
    if 'CITAS PROGRAMADAS' in driver.page_source:
        driver.find_element_by_link_text('CITAS PROGRAMADAS').click()
        time.sleep(5)

        scroll("cphW_uccitasprogramadasdr_btnProgramarCita", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_btnProgramarCita").click()
        time.sleep(5)

        if "cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios" in driver.page_source:
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "001Z000000VEOKDIA5":
                    option.click()
                    break

        print "Escogiendo doctor: Demo AS"
        assert("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores" in driver.page_source), "Cannot choose doctor"
        scroll("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores", driver)
        element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "003Z000001LIAF5IAP":
                option.click()
                break

        scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnContinuarEscogerConsulDoc", driver)
        driver.find_element_by_xpath("//*[(@id = 'cphW_uccitasprogramadasdr_btnContinuarEscogerConsulDoc')]").click()
        time.sleep(3)
        print "Cita para un menor de edad? No"
        assert("cphW_uccitasprogramadasdr_btnconfirmarMenor_No" in driver.page_source), "Not on the right page"
        scroll("cphW_uccitasprogramadasdr_btnconfirmarMenor_No", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_btnconfirmarMenor_No").click()
        time.sleep(3)

        print "Registrando paciente paciente"
        assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda" in driver.page_source), "Not on the right page_source"
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").click()
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").send_keys("no existe")
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").send_keys(Keys.ENTER)
        time.sleep(4)

        assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar" in driver.page_source), "Registrar paciente button did not show up"
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar").click()
        time.sleep(4)

        assert("Nuevo Paciente" in driver.page_source or "New Patient" in driver.page_source), "Not on the right page"

        #first name
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre", driver)
        driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").click()
        driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").send_keys(paciente)

        #last name
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido", driver)
        driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").click()
        driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").send_keys(paciente_apellido)

        #sexo
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo", driver)
        driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").click()
        driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys("M")
        driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys(Keys.ENTER)

        #email
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtCorreoElectronico", driver)
        driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtCorreoElectronico']").click()
        temp_email = paciente + "_" + paciente_apellido + "@mediconecta.com"
        driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtCorreoElectronico']").send_keys(temp_email)
        driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtCorreoElectronico']").send_keys(Keys.ENTER)

        time.sleep(4)
        print "Nuevo paciente registrado"

        #getting new time:
        time_of_day = "AM"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        year = current_time[0:4]
        month = current_time[5:7]
        day = current_time[8:10]
        hour = current_time[11:13]
        minuto = current_time[14:16]
        hour = str(int(hour) + 1)
        if int(minuto) > 45:
            minuto = "00"
            hour = str(int(hour) + 1)
        elif int(minuto) < 15:
            minuto = "00"
        else:
            minuto = "30"
        if hour == "25":
            hour = "1"
            time_of_day = "AM"
        if hour == "26":
            hour = "2"
            time_of_day = "AM"
        if int(hour) >= 12 and int(hour) != 24:
            time_of_day = "PM"
        if int(hour) > 12:
            hour = str(int(hour) - 12)

        venezuela_time = str(int(hour) - 1)
        also_v_time = venezuela_time
        if venezuela_time == "0":
            venezuela_time = "12"
            if time_of_day == "PM":
                time_of_day = "AM"
            else:
                time_of_day = "PM"
        if time_of_day == "PM":
            venezuela_time = str(int(venezuela_time) + 12)
        if also_v_time == "12":
            also_v_time = "00"



        assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha" in driver.page_source), "Did not go to the right page"
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").click()
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").send_keys(day + "/" + month + "/" + year)
        driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()
        time.sleep(1)

        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").click()
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").send_keys(hour +':'+ minuto + " " + time_of_day)
        driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()
        time.sleep(1)

        if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta" in driver.page_source:
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys(Keys.BACKSPACE + Keys.BACKSPACE)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys("1")
            time.sleep(1)

        if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas" in driver.page_source:
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas']")
            all_options = element.find_elements_by_tag_name("option")
            currency = None
            for option in all_options:
                if option.get_attribute("value") == "a0nZ00000037vdjIAA":
                    option.click()
                    currency = "USD"
                    print "Pay in USD"
                    break
                elif option.get_attribute("value") == "a0nZ00000037vdeIAA":
                    option.click()
                    currency = "VEF"
                    print "Pay in VEF"
                    break
        assert(currency != None), "No currency found"
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar").click()
        time.sleep(5)

        assert ("cphW_uccitasprogramadasdr_btnProgramarCita" in driver.page_source), "Cita no completada"

        print "Checking if cita was made"
        scroll("uniform-cphW_uccitasprogramadasdr_rblFiltrar", driver)
        driver.find_element_by_id("uniform-cphW_uccitasprogramadasdr_rblFiltrar").click()
        time.sleep(4)

        if "cphW_uccitasprogramadasdr_ddlConsultorios" in driver.page_source:
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlConsultorios']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "001Z000000VEOKDIA5":
                    option.click()
                    break

        time.sleep(5)
        scroll("cphW_uccitasprogramadasdr_ddlDoctores", driver)
        element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlDoctores']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "003Z000001LIAF5IAP":
                option.click()
                break
        time.sleep(6)
        phrase = venezuela_time + ":" + str(minuto) + " - Cita con " + paciente + " " + paciente_apellido
        also_phrase = also_v_time + ":" + str(minuto) + " - Cita con " + paciente + " " + paciente_apellido
        assert (phrase in driver.page_source or also_phrase in driver.page_source), "cita no hecha"
        print "Cita made and confirmed"

def DoctorProgramarCitaPaciente(driver):
    time.sleep(5)
    if 'CITAS PROGRAMADAS' in driver.page_source:
        driver.find_element_by_link_text('CITAS PROGRAMADAS').click()
        time.sleep(5)

        scroll("cphW_uccitasprogramadasdr_btnProgramarCita", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_btnProgramarCita").click()
        time.sleep(5)

        if "cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios" in driver.page_source:
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "001Z000000VEOKDIA5":
                    option.click()
                    break

        print "Escogiendo doctor: Demo AS"
        assert("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores" in driver.page_source), "Cannot choose doctor"
        scroll("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores", driver)
        element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "003Z000001LIAF5IAP":
                option.click()
                break

        scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnContinuarEscogerConsulDoc", driver)
        driver.find_element_by_xpath("//*[(@id = 'cphW_uccitasprogramadasdr_btnContinuarEscogerConsulDoc')]").click()
        time.sleep(3)
        print "Cita para un menor de edad? No"
        assert("cphW_uccitasprogramadasdr_btnconfirmarMenor_No" in driver.page_source), "Not on the right page"
        scroll("cphW_uccitasprogramadasdr_btnconfirmarMenor_No", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_btnconfirmarMenor_No").click()
        time.sleep(3)

        print "Escogiendo paciente"
        assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda" in driver.page_source), "Not on the right page_source"

        if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0" in driver.page_source:
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0").click()
            time.sleep(5)
        else:
            print "no patient was found"

        #getting new time:
        time_of_day = "AM"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        year = current_time[0:4]
        month = current_time[5:7]
        day = current_time[8:10]
        hour = current_time[11:13]
        minuto = current_time[14:16]
        hour = str(int(hour) + 1)
        if int(minuto) > 45:
            minuto = "00"
            hour = str(int(hour) + 1)
        elif int(minuto) < 15:
            minuto = "00"
        else:
            minuto = "30"
        if hour == "25":
            hour = "1"
            time_of_day = "AM"
        if hour == "26":
            hour = "2"
            time_of_day = "AM"
        if int(hour) >= 12 and int(hour) != 24:
            time_of_day = "PM"
        if int(hour) > 12:
            hour = str(int(hour) - 12)

        venezuela_time = str(int(hour) - 1)
        also_v_time = venezuela_time
        if venezuela_time == "0":
            venezuela_time = "12"
            if time_of_day == "PM":
                time_of_day = "AM"
            else:
                time_of_day = "PM"
        if time_of_day == "PM":
            venezuela_time = str(int(venezuela_time) + 12)
        if also_v_time == "12":
            also_v_time = "00"


        assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha" in driver.page_source), "Did not go to the right page"
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").click()
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").send_keys(day + "/" + month + "/" + year)
        driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()
        time.sleep(1)

        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").click()
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").send_keys(hour +':'+ minuto + " " + time_of_day)
        driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()
        time.sleep(1)

        if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta" in driver.page_source:
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys(Keys.BACKSPACE + Keys.BACKSPACE)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys("1")
            time.sleep(1)

        if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas" in driver.page_source:
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas']")
            all_options = element.find_elements_by_tag_name("option")
            currency = None
            for option in all_options:
                if option.get_attribute("value") == "a0nZ00000037vdjIAA":
                    option.click()
                    currency = "USD"
                    print "Pay in USD"
                    break
                elif option.get_attribute("value") == "a0nZ00000037vdeIAA":
                    option.click()
                    currency = "VEF"
                    print "Pay in VEF"
                    break
        assert(currency != None), "No currency found"
        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar").click()
        time.sleep(5)

        assert ("cphW_uccitasprogramadasdr_btnProgramarCita" in driver.page_source), "Cita no completada"

        print "Checking if cita was made"
        scroll("uniform-cphW_uccitasprogramadasdr_rblFiltrar", driver)
        driver.find_element_by_id("uniform-cphW_uccitasprogramadasdr_rblFiltrar").click()
        time.sleep(4)

        if "cphW_uccitasprogramadasdr_ddlConsultorios" in driver.page_source:
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlConsultorios']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "001Z000000VEOKDIA5":
                    option.click()
                    break

        time.sleep(5)
        scroll("cphW_uccitasprogramadasdr_ddlDoctores", driver)
        element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlDoctores']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "003Z000001LIAF5IAP":
                option.click()
                break
        time.sleep(6)
        phrase = venezuela_time + ":" + str(minuto) + " - Cita con Pruebas Jenkins Chrome Tokbox"
        also_phrase = also_v_time + ":" + str(minuto) + " - Cita con Pruebas Jenkins Chrome Tokbox"
        assert (phrase in driver.page_source or also_phrase in driver.page_source), "cita no hecha"
        print "Cita made and confirmed"

def DoctorProgramarCitaMinor(driver):
        time.sleep(5)
        if 'CITAS PROGRAMADAS' in driver.page_source:
            driver.find_element_by_link_text('CITAS PROGRAMADAS').click()
            time.sleep(5)

            scroll("cphW_uccitasprogramadasdr_btnProgramarCita", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_btnProgramarCita").click()
            time.sleep(5)

            if "cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios']")
                all_options = element.find_elements_by_tag_name("option")
                for option in all_options:
                    if option.get_attribute("value") == "001Z000000VEOKDIA5":
                        option.click()
                        break

            print "Escogiendo doctor: Demo AS"
            assert("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores" in driver.page_source), "Cannot choose doctor"
            scroll("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores", driver)
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "003Z000001LIAF5IAP":
                    option.click()
                    break

            scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnContinuarEscogerConsulDoc", driver)
            driver.find_element_by_xpath("//*[(@id = 'cphW_uccitasprogramadasdr_btnContinuarEscogerConsulDoc')]").click()
            time.sleep(3)

            print "Cita para un menor de edad? Si"
            assert("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si" in driver.page_source), "Not on the right page"
            scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si", driver)
            driver.find_element_by_id("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si").click()
            time.sleep(3)

            print "Escogiendo paciente"
            assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda" in driver.page_source), "Not on the right page_source"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").send_keys("jenkins chrome tokbox")
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").send_keys(Keys.ENTER)
            time.sleep(4)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0" in driver.page_source:
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0", driver)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0").click()
                time.sleep(5)
            else:
                print "no patient was found"

            if "Nuevo Dependiente" in driver.page_source or "New Dependent" in driver.page_source:
                print "registrando dependiente"
                #first name
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").send_keys("Jenkins Jr")
                #last name
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").send_keys("Chrome Jr")
                #sexo
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys("M")
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys(Keys.ENTER)
                #Registrar
                scroll("hab_ctl00$cphW$uccitasprogramadasdr$ucBuscarPacientesCitaDoctor$btnCrearPaciente", driver)
                driver.find_element_by_xpath("//*[@id='hab_ctl00$cphW$uccitasprogramadasdr$ucBuscarPacientesCitaDoctor$btnCrearPaciente']").click()
                print "Nuevo independiente registrado"
                time.sleep(5)
            else:
                print "Escogiendo dependiente"
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0", driver)
                driver.find_element_by_xpath("//*[(@id = 'cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0')]").click()
                time.sleep(5)

            #getting new time:
            time_of_day = "AM"
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            year = current_time[0:4]
            month = current_time[5:7]
            day = current_time[8:10]
            hour = current_time[11:13]
            minuto = current_time[14:16]
            hour = str(int(hour) + 1)
            if int(minuto) > 45:
                minuto = "00"
                hour = str(int(hour) + 1)
            elif int(minuto) < 15:
                minuto = "00"
            else:
                minuto = "30"
            if hour == "25":
                hour = "1"
                time_of_day = "AM"
            if hour == "26":
                hour = "2"
                time_of_day = "AM"
            if int(hour) >= 12 and int(hour) != 24:
                time_of_day = "PM"
            if int(hour) > 12:
                hour = str(int(hour) - 12)

            venezuela_time = str(int(hour) - 1)
            also_v_time = venezuela_time
            if venezuela_time == "0":
                venezuela_time = "12"
                if time_of_day == "PM":
                    time_of_day = "AM"
                else:
                    time_of_day = "PM"
            if time_of_day == "PM":
                venezuela_time = str(int(venezuela_time) + 12)
            if also_v_time == "12":
                also_v_time = "00"

            assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha" in driver.page_source), "Did not go to the right page"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").send_keys(day + "/" + month + "/" + year)
            driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()

            time.sleep(1)

            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").send_keys(hour +':'+ minuto + " " + time_of_day)
            driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()
            time.sleep(1)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta" in driver.page_source:
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta", driver)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").click()
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys(Keys.BACKSPACE + Keys.BACKSPACE)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys("1")
                time.sleep(1)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas']")
                all_options = element.find_elements_by_tag_name("option")
                currency = None
                for option in all_options:
                    if option.get_attribute("value") == "a0nZ00000037vdjIAA":
                        option.click()
                        currency = "USD"
                        print "Pay in USD"
                        break
                    elif option.get_attribute("value") == "a0nZ00000037vdeIAA":
                        option.click()
                        currency = "VEF"
                        print "Pay in VEF"
                        break
            assert(currency != None), "No currency found"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar").click()
            time.sleep(5)

            assert ("cphW_uccitasprogramadasdr_btnProgramarCita" in driver.page_source), "Cita no completada"

            print "Checking if cita was made"
            scroll("uniform-cphW_uccitasprogramadasdr_rblFiltrar", driver)
            driver.find_element_by_id("uniform-cphW_uccitasprogramadasdr_rblFiltrar").click()
            time.sleep(4)

            if "cphW_uccitasprogramadasdr_ddlConsultorios" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlConsultorios']")
                all_options = element.find_elements_by_tag_name("option")
                for option in all_options:
                    if option.get_attribute("value") == "001Z000000VEOKDIA5":
                        option.click()
                        break

            time.sleep(5)
            scroll("cphW_uccitasprogramadasdr_ddlDoctores", driver)
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlDoctores']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "003Z000001LIAF5IAP":
                    option.click()
                    break
            time.sleep(6)
            phrase = venezuela_time + ":" + str(minuto) + " - Cita con Jenkins Jr Chrome Jr"
            also_phrase = also_v_time + ":" + str(minuto) + " - Cita con Jenkins Jr Chrome Jr"
            assert (phrase in driver.page_source or also_phrase in driver.page_source), "cita no hecha"
            print "Cita made and confirmed"

def DoctorProgramarCitaRegMinor(driver):
        time.sleep(5)
        if 'CITAS PROGRAMADAS' in driver.page_source:
            driver.find_element_by_link_text('CITAS PROGRAMADAS').click()
            time.sleep(5)

            scroll("cphW_uccitasprogramadasdr_btnProgramarCita", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_btnProgramarCita").click()
            time.sleep(5)

            if "cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios']")
                all_options = element.find_elements_by_tag_name("option")
                for option in all_options:
                    if option.get_attribute("value") == "001Z000000VEOKDIA5":
                        option.click()
                        break

            print "Escogiendo doctor: Demo AS"
            assert("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores" in driver.page_source), "Cannot choose doctor"
            scroll("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores", driver)
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "003Z000001LIAF5IAP":
                    option.click()
                    break

            scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnContinuarEscogerConsulDoc", driver)
            driver.find_element_by_xpath("//*[(@id = 'cphW_uccitasprogramadasdr_btnContinuarEscogerConsulDoc')]").click()
            time.sleep(3)

            print "Cita para un menor de edad? Si"
            assert("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si" in driver.page_source), "Not on the right page"
            scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si", driver)
            driver.find_element_by_id("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si").click()
            time.sleep(3)

            print "Escogiendo paciente"
            assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda" in driver.page_source), "Not on the right page_source"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").send_keys("jenkins chrome tokbox")
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").send_keys(Keys.ENTER)
            time.sleep(4)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0" in driver.page_source:
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0", driver)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0").click()
                time.sleep(5)
            else:
                print "no patient was found"

            if "Nuevo Dependiente" in driver.page_source or "New Dependent" in driver.page_source or "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar" in driver.page_source:
                numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                paciente = "Dependiente" + random.choice(numbers) + random.choice(numbers) + random.choice(numbers)
                paciente_apellido = random.choice(numbers) + random.choice(numbers) + random.choice(numbers)

                if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar" in driver.page_source:
                    scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar", driver)
                    driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar").click()
                    time.sleep(3)

                print "registrando dependiente"
                #first name
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").send_keys(paciente)
                #last name
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").send_keys(paciente_apellido)
                #sexo
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys("M")
                #driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys(Keys.ENTER)
                #Registrar
                if "hab_ctl00$cphW$uccitasprogramadasdr$ucBuscarPacientesCitaDoctor$btnCrearPaciente" in driver.page_source:
                    scroll("hab_ctl00$cphW$uccitasprogramadasdr$ucBuscarPacientesCitaDoctor$btnCrearPaciente", driver)
                    driver.find_element_by_xpath("//*[@id='hab_ctl00$cphW$uccitasprogramadasdr$ucBuscarPacientesCitaDoctor$btnCrearPaciente']").click()
                    print "Nuevo independiente registrado"
                time.sleep(5)
            else:
                print "No encontro boton para registar dependiente"

            #getting new time:
            time_of_day = "AM"
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            year = current_time[0:4]
            month = current_time[5:7]
            day = current_time[8:10]
            hour = current_time[11:13]
            minuto = current_time[14:16]
            hour = str(int(hour) + 1)
            if int(minuto) > 45:
                minuto = "00"
                hour = str(int(hour) + 1)
            elif int(minuto) < 15:
                minuto = "00"
            else:
                minuto = "30"
            if hour == "25":
                hour = "1"
                time_of_day = "AM"
            if hour == "26":
                hour = "2"
                time_of_day = "AM"
            if int(hour) >= 12 and int(hour) != 24:
                time_of_day = "PM"
            if int(hour) > 12:
                hour = str(int(hour) - 12)

            venezuela_time = str(int(hour) - 1)
            also_v_time = venezuela_time
            if venezuela_time == "0":
                venezuela_time = "12"
                if time_of_day == "PM":
                    time_of_day = "AM"
                else:
                    time_of_day = "PM"
            if time_of_day == "PM":
                venezuela_time = str(int(venezuela_time) + 12)
            if also_v_time == "12":
                also_v_time = "00"

            assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha" in driver.page_source), "Did not go to the right page"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").send_keys(day + "/" + month + "/" + year)
            driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()

            time.sleep(1)

            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").send_keys(hour +':'+ minuto + " " + time_of_day)
            driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()
            time.sleep(1)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta" in driver.page_source:
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta", driver)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").click()
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys(Keys.BACKSPACE + Keys.BACKSPACE)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys("1")
                time.sleep(1)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas']")
                all_options = element.find_elements_by_tag_name("option")
                currency = None
                for option in all_options:
                    if option.get_attribute("value") == "a0nZ00000037vdjIAA":
                        option.click()
                        currency = "USD"
                        print "Pay in USD"
                        break
                    elif option.get_attribute("value") == "a0nZ00000037vdeIAA":
                        option.click()
                        currency = "VEF"
                        print "Pay in VEF"
                        break
            assert(currency != None), "No currency found"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar").click()
            time.sleep(5)

            assert ("cphW_uccitasprogramadasdr_btnProgramarCita" in driver.page_source), "Cita no completada"

            print "Checking if cita was made"
            scroll("uniform-cphW_uccitasprogramadasdr_rblFiltrar", driver)
            driver.find_element_by_id("uniform-cphW_uccitasprogramadasdr_rblFiltrar").click()
            time.sleep(4)

            if "cphW_uccitasprogramadasdr_ddlConsultorios" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlConsultorios']")
                all_options = element.find_elements_by_tag_name("option")
                for option in all_options:
                    if option.get_attribute("value") == "001Z000000VEOKDIA5":
                        option.click()
                        break

            time.sleep(5)
            scroll("cphW_uccitasprogramadasdr_ddlDoctores", driver)
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlDoctores']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "003Z000001LIAF5IAP":
                    option.click()
                    break
            time.sleep(6)
            phrase = venezuela_time + ":" + str(minuto) + " - Cita con " + paciente + " " + paciente_apellido
            also_phrase = also_v_time + ":" + str(minuto) + " - Cita con " + paciente + " " + paciente_apellido
            assert (phrase in driver.page_source or also_phrase in driver.page_source), "cita no hecha"
            print "Cita made and confirmed"

def DoctorProgramarCitaMinorRegRep(driver):
        time.sleep(5)
        if 'CITAS PROGRAMADAS' in driver.page_source:
            driver.find_element_by_link_text('CITAS PROGRAMADAS').click()
            time.sleep(5)

            scroll("cphW_uccitasprogramadasdr_btnProgramarCita", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_btnProgramarCita").click()
            time.sleep(5)

            if "cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios']")
                all_options = element.find_elements_by_tag_name("option")
                for option in all_options:
                    if option.get_attribute("value") == "001Z000000VEOKDIA5":
                        option.click()
                        break

            print "Escogiendo doctor: Demo AS"
            assert("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores" in driver.page_source), "Cannot choose doctor"
            scroll("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores", driver)
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "003Z000001LIAF5IAP":
                    option.click()
                    break

            scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnContinuarEscogerConsulDoc", driver)
            driver.find_element_by_xpath("//*[(@id = 'cphW_uccitasprogramadasdr_btnContinuarEscogerConsulDoc')]").click()
            time.sleep(3)

            print "Cita para un menor de edad? Si"
            assert("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si" in driver.page_source), "Not on the right page"
            scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si", driver)
            driver.find_element_by_id("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si").click()
            time.sleep(3)

            assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda" in driver.page_source), "Not on the right page_source"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").send_keys("no existe")
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_txtBusqueda").send_keys(Keys.ENTER)
            time.sleep(4)

            numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            paciente = "Paciente" + random.choice(numbers) + random.choice(numbers) + random.choice(numbers)
            paciente_apellido = random.choice(numbers) + random.choice(numbers) + random.choice(numbers)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar" in driver.page_source:
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar", driver)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar").click()
                time.sleep(3)

            print "registrando representante"
            #first name
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre", driver)
            driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").click()
            driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").send_keys(paciente)
            #last name
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido", driver)
            driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").click()
            driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").send_keys(paciente_apellido)
            #sexo
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo", driver)
            driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").click()
            driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys("M")
            driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys(Keys.ENTER)
            #email
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtCorreoElectronico", driver)
            driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtCorreoElectronico']").click()
            driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtCorreoElectronico']").send_keys(paciente+ "." + paciente_apellido + "@mediconecta.com")
            driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtCorreoElectronico']").send_keys(Keys.ENTER)
            time.sleep(3)
            print "Registrando nuevo dependiente "

            if "Nuevo Dependiente" in driver.page_source or "New Dependent" in driver.page_source or "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_btnIrInvitar" in driver.page_source:
                numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                dependiente = "Dependiente" + random.choice(numbers) + random.choice(numbers) + random.choice(numbers)
                dependiente_apellido = random.choice(numbers) + random.choice(numbers) + random.choice(numbers)

                print "registrando dependiente"
                #first name
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").send_keys(dependiente)
                #last name
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").send_keys(dependiente_apellido)
                #sexo
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys("M")
                #Registrar
                scroll("hab_ctl00$cphW$uccitasprogramadasdr$ucBuscarPacientesCitaDoctor$btnCrearPaciente", driver)
                driver.find_element_by_xpath("//*[@id='hab_ctl00$cphW$uccitasprogramadasdr$ucBuscarPacientesCitaDoctor$btnCrearPaciente']").click()
                print "Nuevo dependiente registrado"
                time.sleep(5)
            else:
                print "Not on the right page"

            #getting new time:
            time_of_day = "AM"
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            year = current_time[0:4]
            month = current_time[5:7]
            day = current_time[8:10]
            hour = current_time[11:13]
            minuto = current_time[14:16]
            hour = str(int(hour) + 1)
            if int(minuto) > 45:
                minuto = "00"
                hour = str(int(hour) + 1)
            elif int(minuto) < 15:
                minuto = "00"
            else:
                minuto = "30"
            if hour == "25":
                hour = "1"
                time_of_day = "AM"
            if hour == "26":
                hour = "2"
                time_of_day = "AM"
            if int(hour) >= 12 and int(hour) != 24:
                time_of_day = "PM"
            if int(hour) > 12:
                hour = str(int(hour) - 12)

            venezuela_time = str(int(hour) - 1)
            also_v_time = venezuela_time
            if venezuela_time == "0":
                venezuela_time = "12"
                if time_of_day == "PM":
                    time_of_day = "AM"
                else:
                    time_of_day = "PM"
            if time_of_day == "PM":
                venezuela_time = str(int(venezuela_time) + 12)
            if also_v_time == "12":
                also_v_time = "00"

            assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha" in driver.page_source), "Did not go to the right page"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").send_keys(day + "/" + month + "/" + year)
            driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()

            time.sleep(1)

            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").send_keys(hour +':'+ minuto + " " + time_of_day)
            driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()
            time.sleep(1)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta" in driver.page_source:
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta", driver)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").click()
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys(Keys.BACKSPACE + Keys.BACKSPACE)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys("1")
                time.sleep(1)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas']")
                all_options = element.find_elements_by_tag_name("option")
                currency = None
                for option in all_options:
                    if option.get_attribute("value") == "a0nZ00000037vdjIAA":
                        option.click()
                        currency = "USD"
                        print "Pay in USD"
                        break
                    elif option.get_attribute("value") == "a0nZ00000037vdeIAA":
                        option.click()
                        currency = "VEF"
                        print "Pay in VEF"
                        break
            assert(currency != None), "No currency found"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar").click()
            time.sleep(5)

            assert ("cphW_uccitasprogramadasdr_btnProgramarCita" in driver.page_source), "Cita no completada"

            print "Checking if cita was made"
            scroll("uniform-cphW_uccitasprogramadasdr_rblFiltrar", driver)
            driver.find_element_by_id("uniform-cphW_uccitasprogramadasdr_rblFiltrar").click()
            time.sleep(4)

            if "cphW_uccitasprogramadasdr_ddlConsultorios" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlConsultorios']")
                all_options = element.find_elements_by_tag_name("option")
                for option in all_options:
                    if option.get_attribute("value") == "001Z000000VEOKDIA5":
                        option.click()
                        break

            time.sleep(5)
            scroll("cphW_uccitasprogramadasdr_ddlDoctores", driver)
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlDoctores']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "003Z000001LIAF5IAP":
                    option.click()
                    break
            time.sleep(6)
            phrase = venezuela_time + ":" + str(minuto) + " - Cita con " + dependiente + " " + dependiente_apellido
            also_phrase = also_v_time + ":" + str(minuto) + " - Cita con " + dependiente + " " + dependiente_apellido
            assert (phrase in driver.page_source or also_phrase in driver.page_source), "cita no hecha"
            print "Cita made and confirmed"

def DoctorProgramarCitaMinorCont(driver):
        time.sleep(5)
        if 'CITAS PROGRAMADAS' in driver.page_source:
            driver.find_element_by_link_text('CITAS PROGRAMADAS').click()
            time.sleep(5)

            scroll("cphW_uccitasprogramadasdr_btnProgramarCita", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_btnProgramarCita").click()
            time.sleep(5)

            if "cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Consultorios']")
                all_options = element.find_elements_by_tag_name("option")
                for option in all_options:
                    if option.get_attribute("value") == "001Z000000VEOKDIA5":
                        option.click()
                        break

            print "Escogiendo doctor: Demo AS"
            assert("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores" in driver.page_source), "Cannot choose doctor"
            scroll("cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores", driver)
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlModalEscogerConsulDoc_Doctores']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "003Z000001LIAF5IAP":
                    option.click()
                    break

            scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnContinuarEscogerConsulDoc", driver)
            driver.find_element_by_xpath("//*[(@id = 'cphW_uccitasprogramadasdr_btnContinuarEscogerConsulDoc')]").click()
            time.sleep(3)

            print "Cita para un menor de edad? Si"
            assert("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si" in driver.page_source), "Not on the right page"
            scroll("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si", driver)
            driver.find_element_by_id("hab_ctl00$cphW$uccitasprogramadasdr$btnconfirmarMenor_Si").click()
            time.sleep(3)

            print "Escogiendo paciente"

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0" in driver.page_source:
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0", driver)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0").click()
                time.sleep(5)
            else:
                print "no patient was found"

            if "Nuevo Dependiente" in driver.page_source or "New Dependent" in driver.page_source:
                print "registrando dependiente"
                #first name
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtNombre']").send_keys("Jenkins Jr")
                #last name
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_txtApellido']").send_keys("Chrome Jr")
                #sexo
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo", driver)
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").click()
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys("M")
                driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucRegistroPacienteDr_ddlSexo']").send_keys(Keys.ENTER)
                #Registrar
                scroll("hab_ctl00$cphW$uccitasprogramadasdr$ucBuscarPacientesCitaDoctor$btnCrearPaciente", driver)
                driver.find_element_by_xpath("//*[@id='hab_ctl00$cphW$uccitasprogramadasdr$ucBuscarPacientesCitaDoctor$btnCrearPaciente']").click()
                print "Nuevo independiente registrado"
                time.sleep(5)
            else:
                print "Escogiendo dependiente"
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0", driver)
                driver.find_element_by_xpath("//*[(@id = 'cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_rptTable_btnEscoger_0')]").click()
                time.sleep(5)

            #getting new time:
            time_of_day = "AM"
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            year = current_time[0:4]
            month = current_time[5:7]
            day = current_time[8:10]
            hour = current_time[11:13]
            minuto = current_time[14:16]
            hour = str(int(hour) + 1)
            if int(minuto) > 45:
                minuto = "00"
                hour = str(int(hour) + 1)
            elif int(minuto) < 15:
                minuto = "00"
            else:
                minuto = "30"
            if hour == "25":
                hour = "1"
                time_of_day = "AM"
            if hour == "26":
                hour = "2"
                time_of_day = "AM"
            if int(hour) >= 12 and int(hour) != 24:
                time_of_day = "PM"
            if int(hour) > 12:
                hour = str(int(hour) - 12)

            venezuela_time = str(int(hour) - 1)
            also_v_time = venezuela_time
            if venezuela_time == "0":
                venezuela_time = "12"
                if time_of_day == "PM":
                    time_of_day = "AM"
                else:
                    time_of_day = "PM"
            if time_of_day == "PM":
                venezuela_time = str(int(venezuela_time) + 12)
            if also_v_time == "12":
                also_v_time = "00"

            assert("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha" in driver.page_source), "Did not go to the right page"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").send_keys(day + "/" + month + "/" + year)
            driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()

            time.sleep(1)

            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").send_keys(hour +':'+ minuto + " " + time_of_day)
            driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_divDdlConsultorio"]/label').click()
            time.sleep(1)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta" in driver.page_source:
                scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta", driver)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").click()
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys(Keys.BACKSPACE + Keys.BACKSPACE)
                driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtPrecioConsulta").send_keys("1")
                time.sleep(1)

            if "cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_ddlMonedas']")
                all_options = element.find_elements_by_tag_name("option")
                currency = None
                for option in all_options:
                    if option.get_attribute("value") == "a0nZ00000037vdjIAA":
                        option.click()
                        currency = "USD"
                        print "Pay in USD"
                        break
                    elif option.get_attribute("value") == "a0nZ00000037vdeIAA":
                        option.click()
                        currency = "VEF"
                        print "Pay in VEF"
                        break
            assert(currency != None), "No currency found"
            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_btnProgramar").click()
            time.sleep(5)

            assert ("cphW_uccitasprogramadasdr_btnProgramarCita" in driver.page_source), "Cita no completada"

            print "Checking if cita was made"
            scroll("uniform-cphW_uccitasprogramadasdr_rblFiltrar", driver)
            driver.find_element_by_id("uniform-cphW_uccitasprogramadasdr_rblFiltrar").click()
            time.sleep(4)

            if "cphW_uccitasprogramadasdr_ddlConsultorios" in driver.page_source:
                element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlConsultorios']")
                all_options = element.find_elements_by_tag_name("option")
                for option in all_options:
                    if option.get_attribute("value") == "001Z000000VEOKDIA5":
                        option.click()
                        break

            time.sleep(5)
            scroll("cphW_uccitasprogramadasdr_ddlDoctores", driver)
            element = driver.find_element_by_xpath("//*[@id='cphW_uccitasprogramadasdr_ddlDoctores']")
            all_options = element.find_elements_by_tag_name("option")
            for option in all_options:
                if option.get_attribute("value") == "003Z000001LIAF5IAP":
                    option.click()
                    break
            time.sleep(6)
            phrase = venezuela_time + ":" + str(minuto) + " - Cita con Jenkins Jr Chrome Jr"
            also_phrase = also_v_time + ":" + str(minuto) + " - Cita con Jenkins Jr Chrome Jr"
            assert (phrase in driver.page_source or also_phrase in driver.page_source), "cita no hecha"
            print "Cita made and confirmed"

def screenshot(driver, file_name):
    assert ("cphW_ucPacientesEnFila_btnSolicitarCitaHub" in driver.page_source), "Not on right page"
    scroll("cphW_ucPacientesEnFila_btnSolicitarCitaHub", driver)
    driver.find_element_by_id("cphW_ucPacientesEnFila_btnSolicitarCitaHub").click()
    time.sleep(4)
    driver.save_screenshot(file_name)
    time.sleep(1)
    driver.find_elements_by_tag_name("button")[-1].click()

def reAgendarCita(driver):
    time.sleep(3)
    assert 'Citas Programadas' in driver.title, 'Not in Cita Programadas'

    driver.find_element_by_xpath('//*[@id="lnk-reprogramar"]/i').click()

    time.sleep(2)
    assert 'cphW_uccitasprogramadasdr_lblTituloReprogramar' in driver.page_source, 'Reprogram diologue did not pop up'


    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    year = current_time[0:4]
    month = str(int(current_time[5:7]))
    day = str(int(current_time[8:10]) + 1)


    fechaBox = driver.find_element_by_id('cphW_uccitasprogramadasdr_ucSolicitudCitaDr_txtFecha')
    fechaBox.clear()
    fechaBox.send_keys(day + "/" + month + "/" + year +Keys.RETURN)

    time.sleep(2)
    timeBox = driver.find_element_by_id('cphW_uccitasprogramadasdr_ucSolicitudCitaDr_txtHora')
    timeBox.clear()
    timeBox.send_keys('9:00 AM')

    time.sleep(2)

    submit = driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_btnReprogramaCita"]')
    submit.click()
    time.sleep(2)
    submit.click()

    print " Making sure cita was changed"

    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="div-CalendarioCitas"]/div[2]/div[1]/div/div[2]/button[3]').click()


    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="div-CalendarioCitas"]/div[2]/div[1]/div/div[1]/button[3]').click()

    assert '08:00 - 08:45' in  driver.page_source, 'Cita not changed'

def cancelarCita(driver):
    time.sleep(3)
    assert 'Citas Programadas' in driver.title, 'Not in Cita Programadas'

    diaButton = driver.find_element_by_xpath('//*[@id="div-CalendarioCitas"]/div[2]/div[1]/div/div[2]/button[3]')
    diaButton.click()

    time.sleep(2)
    hoyButton = driver.find_element_by_xpath('//*[@id="div-CalendarioCitas"]/div[2]/div[1]/div/div[1]/button[2]')
    hoyButton.click()

    time.sleep(2)
    siguenteButton = driver.find_element_by_xpath('//*[@id="div-CalendarioCitas"]/div[2]/div[1]/div/div[1]/button[3]')
    siguenteButton.click()

    time.sleep(2)
    removeButton = driver.find_element_by_xpath('//*[@id="lnk-cancelar"]/i')
    removeButton.click()

    time.sleep(2)
    assert 'Estas seguro que deseas' in driver.page_source, 'Not asked if im sure'

    siButton  = driver.find_element_by_xpath('//*[@id="cphW_uccitasprogramadasdr_btnCancelarCita"]')
    siButton.click()

    time.sleep(3)

    assert '08:00 - 08:45' not in driver.page_source

def DatosdelConsultorio(driver):
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "wrapper-dropdown-5", " " ))]').click()
    time.sleep(1)
    driver.find_element_by_id("liMicuenta").click()
    time.sleep(3)
    print "Entrando a Datos del Consultorio"
    scroll("cphW_ucmicuentadoctor_liDatosConsultorio", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_liDatosConsultorio").click()
    time.sleep(1)

    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ddlConsultorios")]')
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "001Z000000VEOKDIA5":
            option.click()
            break

    scroll("cphW_ucmicuentadoctor_ucDatosConsultorio_lnkEditarDatosConsultorio", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ucDatosConsultorio_lnkEditarDatosConsultorio").click()
    time.sleep(3)
    print "Editar informacion"
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    numero_de_telephono = random.choice(numbers) + random.choice(numbers) + random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)

    scroll("cphW_ucmicuentadoctor_ucDatosConsultorio_ucRegistrarConsultorioEditar_txtTelefono", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ucDatosConsultorio_ucRegistrarConsultorioEditar_txtTelefono").click()
    driver.find_element_by_id("cphW_ucmicuentadoctor_ucDatosConsultorio_ucRegistrarConsultorioEditar_txtTelefono").clear()
    driver.find_element_by_id("cphW_ucmicuentadoctor_ucDatosConsultorio_ucRegistrarConsultorioEditar_txtTelefono").send_keys(numero_de_telephono + Keys.TAB)
    time.sleep(2)

    scroll("cphW_ucmicuentadoctor_ucDatosConsultorio_btnGuardarDatosConsultorio", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ucDatosConsultorio_btnGuardarDatosConsultorio").click()
    time.sleep(4)

    assert(numero_de_telephono in driver.page_source), "No se guardo"
    time.sleep(1)

def ManejoDeSecretarias(driver):
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "wrapper-dropdown-5", " " ))]').click()
    time.sleep(1)
    driver.find_element_by_id("liMicuenta").click()
    time.sleep(3)
    scroll("cphW_ucmicuentadoctor_liSecretarias", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_liSecretarias").click()
    time.sleep(1)

    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ddlConsultorios")]')
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "001Z000000VEOKDIA5":
            option.click()
            break

    print " Verificando que Secre3 Pruebas no esta en el consultorio"
    if "Secre3 Pruebas" in driver.page_source:
        if "cphW_ucmicuentadoctor_ctl34_rptTable_btnEliminar_5" in driver.page_source:
            print "Se encontro Secre3 Pruebas, Eliminando..."
            driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_rptTable_btnEliminar_5").click()
            scroll("cphW_ucmicuentadoctor_ctl34_rptTable_btnEliminar_5", driver)
            driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_btnEliminarSecretaria").click()
        elif "cphW_ucmicuentadoctor_ctl34_rptTable_btnEliminar_6" in driver.page_source:
            print "Se encontro Secre3 Pruebas, Eliminando..."
            driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_rptTable_btnEliminar_5").click()
            scroll("cphW_ucmicuentadoctor_ctl34_rptTable_btnEliminar_5", driver)
            driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_btnEliminarSecretaria").click()
        time.sleep(5)
    else:
        print " Secre3 Pruebas no esta en el consultorio"

    driver.refresh()
    scroll("cphW_ucmicuentadoctor_liSecretarias", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_liSecretarias").click()
    time.sleep(1)

    assert("Secre3 Pruebas" not in driver.page_source), " Secre3 Pruebas no debe estar en el consultorio"

    scroll("cphW_ucmicuentadoctor_ctl34_btnBuscar", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_btnBuscar").click()
    time.sleep(3)

    print "Registar secretaria"
    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_txtBusqueda", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ctl06_txtBusqueda").click()
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ctl06_txtBusqueda").send_keys("NO EXISTE")
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ctl06_btnBuscarSecretaria").click()

    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_btnRegistrar", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ctl06_btnRegistrar").click()

    #datos:
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    numero_de_telephono = random.choice(numbers) + random.choice(numbers) + random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)
    paciente = "Secretaria" + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers)
    paciente_apellido = random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers)
    cedula = random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers)+ random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers) + random.choice(numbers)
    correo_e = paciente + "." + paciente_apellido + "@mediconecta.com"

    #first name
    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_txtNombre", driver)
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_txtNombre']").send_keys(paciente)
    #last name
    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_txtApellido", driver)
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_txtApellido']").send_keys(paciente_apellido)
    #Nacionalidad
    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ddlNacionalidad")]')
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "Venezuela":
            option.click()
            break
    #Cedula
    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_txtCedula", driver)
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_txtCedula']").send_keys(cedula)
    #fecha de nacimiento
    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ucFecha_ddlDia", driver)
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ucFecha_ddlDia']").click()
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ucFecha_ddlDia']").send_keys("1" + Keys.ENTER)
    #scroll("cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ucFecha_ddlMes", driver)
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ucFecha_ddlMes']").click()
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ucFecha_ddlMes']").send_keys("1" + Keys.ENTER)
    #scroll("cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ucFecha_ddlAnno", driver)
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ucFecha_ddlAnno']").click()
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ucFecha_ddlAnno']").send_keys("1" + Keys.ENTER)
    #sexo
    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ddlSexo", driver)
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_ddlSexo']").send_keys("M" + Keys.ENTER)
    #telephono
    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_txtCelular", driver)
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_txtCelular']").send_keys(numero_de_telephono)
    #correo electronico
    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_txtEmail", driver)
    driver.find_element_by_xpath("//*[@id='cphW_ucmicuentadoctor_ctl34_ctl06_ucDatosSecretaria_txtEmail']").send_keys(correo_e + Keys.ENTER)

    time.sleep(5)
    assert("Secre4 Taria" in driver.page_source), "no se registro"


    print "Testing Agregar Secretaria"
    scroll("cphW_ucmicuentadoctor_ctl34_btnBuscar", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_btnBuscar").click()
    time.sleep(3)

    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_txtBusqueda", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ctl06_txtBusqueda").click()
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ctl06_txtBusqueda").send_keys("Secre3 Pruebas")
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ctl06_btnBuscarSecretaria").click()

    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_rptTable_btnAgregarSecretaria_0", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ctl06_rptTable_btnAgregarSecretaria_0").click()
    time.sleep(1)
    scroll("cphW_ucmicuentadoctor_ctl34_ctl06_btnAsociarSecretaria", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ctl06_btnAsociarSecretaria").click()
    time.sleep(3)
    assert("Secre3" in driver.page_source), "No agrego secretaria"

    if "cphW_ucmicuentadoctor_ctl34_rptTable_btnVer_6" in driver.page_source:
        print "Editar datos de secretaria y Ver datos"
        scroll("cphW_ucmicuentadoctor_ctl34_rptTable_btnVer_6", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_rptTable_btnVer_6").click()
        time.sleep(3)
        driver.save_screenshot("ver_before.jpg")
        driver.find_element_by_id("hab_ctl00$cphW$ucmicuentadoctor$ctl34$ctl08").click()
        time.sleep(1)

        scroll("cphW_ucmicuentadoctor_ctl34_rptTable_btnEditar_6", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_rptTable_btnEditar_6").click()
        time.sleep(2)
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        numero_de_telephono = random.choice(numbers) + random.choice(numbers) + random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)
        scroll("cphW_ucmicuentadoctor_ctl34_ucDatosSecretaria_txtCelular", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ucDatosSecretaria_txtCelular").click()
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ucDatosSecretaria_txtCelular").clear()
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ucDatosSecretaria_txtCelular").send_keys(numero_de_telephono + Keys.ENTER)
        time.sleep(4)

        scroll("cphW_ucmicuentadoctor_ctl34_rptTable_btnVer_6", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_rptTable_btnVer_6").click()
        time.sleep(3)
        driver.save_screenshot("ver_after.jpg")
        driver.find_element_by_id("hab_ctl00$cphW$ucmicuentadoctor$ctl34$ctl08").click()
        time.sleep(1)

        before = Image.open('ver_before.jpg')
        after = Image.open('ver_after.jpg')
        if list(before.getdata()) == list(after.getdata()):
            assert(False), "Did not go to the right page"
        else:
            pass

        #### if you wish to remove images from folder, uncomment following lines:###
        '''
        os.remove(ver_before.jpg)
        os.remove(ver_after.jpg)
        '''

        print "Eliminar secretaria"
        scroll("cphW_ucmicuentadoctor_ctl34_rptTable_btnEliminar_6", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_rptTable_btnEliminar_6").click()
        scroll("cphW_ucmicuentadoctor_ctl34_btnEliminarSecretaria", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_btnEliminarSecretaria").click()
        time.sleep(4)
    elif "cphW_ucmicuentadoctor_ctl34_rptTable_btnVer_5" in driver.page_source:
        print "Editar datos de secretaria y Ver datos"
        scroll("cphW_ucmicuentadoctor_ctl34_rptTable_btnVer_5", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_rptTable_btnVer_5").click()
        time.sleep(3)
        driver.save_screenshot("ver_before.jpg")
        driver.find_element_by_id("hab_ctl00$cphW$ucmicuentadoctor$ctl34$ctl08").click()
        time.sleep(1)

        scroll("cphW_ucmicuentadoctor_ctl34_rptTable_btnEditar_5", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_rptTable_btnEditar_5").click()
        time.sleep(2)
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        numero_de_telephono = random.choice(numbers) + random.choice(numbers) + random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)+ random.choice(numbers)
        scroll("cphW_ucmicuentadoctor_ctl34_ucDatosSecretaria_txtCelular", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ucDatosSecretaria_txtCelular").click()
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ucDatosSecretaria_txtCelular").clear()
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_ucDatosSecretaria_txtCelular").send_keys(numero_de_telephono + Keys.ENTER)
        time.sleep(4)

        scroll("cphW_ucmicuentadoctor_ctl34_rptTable_btnVer_5", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_rptTable_btnVer_5").click()
        time.sleep(3)
        driver.save_screenshot("ver_after.jpg")
        driver.find_element_by_id("hab_ctl00$cphW$ucmicuentadoctor$ctl34$ctl08").click()
        time.sleep(1)

        before = Image.open('ver_before.jpg')
        after = Image.open('ver_after.jpg')
        if list(before.getdata()) == list(after.getdata()):
            assert(False), "Did not go to the right page"
        else:
            pass

        #### if you wish to remove images from folder, uncomment following lines:###
        '''
        os.remove(ver_before.jpg)
        os.remove(ver_after.jpg)
        '''

        print "Eliminar secretaria"
        scroll("cphW_ucmicuentadoctor_ctl34_rptTable_btnEliminar_5", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_rptTable_btnEliminar_5").click()
        scroll("cphW_ucmicuentadoctor_ctl34_btnEliminarSecretaria", driver)
        driver.find_element_by_id("cphW_ucmicuentadoctor_ctl34_btnEliminarSecretaria").click()
        time.sleep(4)

def ManejoDeMonedas(driver):
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "wrapper-dropdown-5", " " ))]').click()
    time.sleep(1)
    driver.find_element_by_id("liMicuenta").click()
    time.sleep(3)
    scroll("cphW_ucmicuentadoctor_liDoctores", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_liDoctores").click()
    time.sleep(1)

    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ddlConsultorios")]')
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "001Z000000VEOKDIA5":
            option.click()
            break

    print "Entrando a manejo de monedas"
    scroll("cphW_ucmicuentadoctor_ctl32_rptTable_btnMonedas_0", driver)
    driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_rptTable_btnMonedas_0').click()
    time.sleep(2)
    print "Agregando nuevo moneda"
    scroll("cphW_ucmicuentadoctor_ctl32_ctl06_btnCrear", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_btnCrear").click()
    time.sleep(3)

    '''
    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ctl32_ctl06_ucCreate_ddlMoneda")]')
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "USD":
            option.click()
            break
    '''
    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ctl32_ctl06_ucCreate_ddlMoneda")]').click()
    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ctl32_ctl06_ucCreate_ddlMoneda")]').send_keys(Keys.DOWN + Keys.ENTER)



    scroll("cphW_ucmicuentadoctor_ctl32_ctl06_ucCreate_txtPrecioConsulta", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_ucCreate_txtPrecioConsulta").send_keys("3")

    scroll("cphW_ucmicuentadoctor_ctl32_ctl06_btnCrearMoneda", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_btnCrearMoneda").click()
    time.sleep(3)

    if "cphW_ucmicuentadoctor_ctl32_ctl06_btnCrearMoneda" in driver.page_source:
        assert(False), "No hay mas monedas para agregar"

    print "Verificando los botones 'ver' y 'editar'"
    scroll("cphW_ucmicuentadoctor_ctl32_ctl06_rptTable_btnVer_1", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_rptTable_btnVer_1").click()
    time.sleep(3)
    driver.save_screenshot("mm_ver_before.jpg")

    scroll("hab_ctl00$cphW$ucmicuentadoctor$ctl32$ctl06$ctl13", driver)
    driver.find_element_by_id("hab_ctl00$cphW$ucmicuentadoctor$ctl32$ctl06$ctl13").click()
    time.sleep(3)

    scroll('cphW_ucmicuentadoctor_ctl32_ctl06_rptTable_btnEditar_1', driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_rptTable_btnEditar_1").click()
    time.sleep(3)

    scroll("cphW_ucmicuentadoctor_ctl32_ctl06_ucRU_txtPrecioConsulta", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_ucRU_txtPrecioConsulta").clear()
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_ucRU_txtPrecioConsulta").send_keys("5")

    scroll("cphW_ucmicuentadoctor_ctl32_ctl06_btnEditarMoneda", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_btnEditarMoneda").click()
    time.sleep(2)

    scroll("cphW_ucmicuentadoctor_ctl32_ctl06_rptTable_btnVer_1", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_rptTable_btnVer_1").click()
    time.sleep(3)
    driver.save_screenshot("mm_ver_after.jpg")

    before = Image.open('mm_ver_before.jpg')
    after = Image.open('mm_ver_after.jpg')
    if list(before.getdata()) == list(after.getdata()):
        assert(False), "Edits did not save"
    else:
        pass

    #### if you wish to remove images from folder, uncomment following lines:###
    '''
    os.remove(mm_ver_before.jpg)
    os.remove(mm_ver_after.jpg)
    '''

    scroll("hab_ctl00$cphW$ucmicuentadoctor$ctl32$ctl06$ctl13", driver)
    driver.find_element_by_id("hab_ctl00$cphW$ucmicuentadoctor$ctl32$ctl06$ctl13").click()
    time.sleep(2)

    print "Eliminado moneda"
    scroll("cphW_ucmicuentadoctor_ctl32_ctl06_rptTable_btnEliminar_1",driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_rptTable_btnEliminar_1").click()
    time.sleep(1)
    scroll("cphW_ucmicuentadoctor_ctl32_ctl06_btnEliminarModal", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ctl06_btnEliminarModal").click()
    time.sleep(4)

def ManejoDeConfiguraciones(driver):
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "wrapper-dropdown-5", " " ))]').click()
    time.sleep(1)
    driver.find_element_by_id("liMicuenta").click()
    time.sleep(3)
    scroll("cphW_ucmicuentadoctor_liDoctores", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_liDoctores").click()
    time.sleep(1)

    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ddlConsultorios")]')
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "001Z000000VEOKDIA5":
            option.click()
            break

    print "Entrando a manejo de configuraciones"
    scroll("cphW_ucmicuentadoctor_ctl32_rptTable_btnConfiguracion_5", driver)
    driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_rptTable_btnConfiguracion_5').click()
    time.sleep(5)

    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ctl32_ucConfiguracion_ddlAvisosPacienteEnFila")]')
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "CorreoElectronico":
            option.click()
            break

    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ctl32_ucConfiguracion_ddlCorreosCitasProgramadas")]')
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "Secretaria":
            option.click()
            break

    scroll("cphW_ucmicuentadoctor_ctl32_ucConfiguracion_btnGuardar", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ucConfiguracion_btnGuardar").click()
    time.sleep(3)

    scroll("cphW_ucmicuentadoctor_ctl32_rptTable_btnConfiguracion_5", driver)
    driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_rptTable_btnConfiguracion_5').click()
    time.sleep(5)
    driver.save_screenshot("mc_ver_before.jpg")


    print "Verificando los editos a manejo de configuraciones"
    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ctl32_ucConfiguracion_ddlAvisosPacienteEnFila")]')
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "MensajeTexto":
            option.click()
            break

    element = driver.find_element_by_xpath('//*[(@id = "cphW_ucmicuentadoctor_ctl32_ucConfiguracion_ddlCorreosCitasProgramadas")]')
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "Doctor":
            option.click()
            break

    scroll("cphW_ucmicuentadoctor_ctl32_ucConfiguracion_btnGuardar", driver)
    driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_ucConfiguracion_btnGuardar").click()
    time.sleep(3)

    scroll("cphW_ucmicuentadoctor_ctl32_rptTable_btnConfiguracion_5", driver)
    driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_rptTable_btnConfiguracion_5').click()
    time.sleep(5)
    driver.save_screenshot("mc_ver_after.jpg")

    before = Image.open('mc_ver_before.jpg')
    after = Image.open('mc_ver_after.jpg')
    if list(before.getdata()) == list(after.getdata()):
        assert(False), "Edits did not save"
    else:
        pass

    #### if you wish to remove images from folder, uncomment following lines:###
    '''
    os.remove(mc_ver_before.jpg)
    os.remove(mc_ver_after.jpg)
    '''

def AppAtencionAlCliente(driver):
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "icon-AtencionAlCliente", " " ))]').click()
    time.sleep(2)
    print "Buscando cliente Jenkins Chrome"
    scroll("cphW_ucBuscarPacienteTelefono_txtBusqueda", driver)
    driver.find_element_by_id("cphW_ucBuscarPacienteTelefono_txtBusqueda").send_keys("1231234" + Keys.ENTER)
    time.sleep(2)

    assert("Pruebas Jenkins Chrome Tokbox" in driver.page_source), "No encontro paciente"
    print "Paciente Jenkins Chrome encontrado"
    time.sleep(5)

def AppLogEmails(driver):
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "icon-LogEmails", " " ))]').click()
    time.sleep(5)

    print "Checking 'Dashboard' tab"
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "k-input", " " ))]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "k-textbox", " " ))]').send_keys("Paciente_Resumen_Cita")
    #driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "k-textbox", " " ))]').send_keys("Correo_Inicial_Saludsa_Corporativos")
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "k-textbox", " " ))]').send_keys(Keys.ENTER)
    time.sleep(3)

    element = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[1]/div[1]/span')
    driver.execute_script("return arguments[0].scrollIntoView();", element)
    time.sleep(1)

    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "processed", " " ))]').click()
    time.sleep(2)
    driver.save_screenshot("Procesados.jpg")

    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "delivered", " " ))]').click()
    time.sleep(2)
    driver.save_screenshot("Entregados.jpg")

    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "open", " " ))]').click()
    time.sleep(2)
    driver.save_screenshot("Abiertos.jpg")

    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "click", " " ))]').click()
    time.sleep(2)
    driver.save_screenshot("Clicks.jpg")

    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "bounce", " " ))]').click()
    time.sleep(2)
    driver.save_screenshot("Rebotes.jpg")

    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "spamreport", " " ))]').click()
    time.sleep(2)
    driver.save_screenshot("Spam.jpg")

    Procesados = Image.open("Procesados.jpg")
    Entregados = Image.open("Entregados.jpg")
    Abiertos = Image.open("Abiertos.jpg")
    Clicks = Image.open("Clicks.jpg")
    Rebotes = Image.open("Rebotes.jpg")
    Spam = Image.open("Spam.jpg")

    driver.refresh()

    if list(Procesados.getdata()) == list(Entregados.getdata()):
        assert(False), "Did not go to the right page"
    if list(Procesados.getdata()) == list(Abiertos.getdata()):
        assert(False), "Did not go to the right page"
    if list(Procesados.getdata()) == list(Clicks.getdata()):
        assert(False), "Did not go to the right page"
    if list(Procesados.getdata()) == list(Rebotes.getdata()):
        assert(False), "Did not go to the right page"
    if list(Procesados.getdata()) == list(Spam.getdata()):
        assert(False), "Did not go to the right page"
    if list(Entregados.getdata()) == list(Abiertos.getdata()):
        assert(False), "Did not go to the right page"
    if list(Entregados.getdata()) == list(Clicks.getdata()):
        assert(False), "Did not go to the right page"
    if list(Entregados.getdata()) == list(Rebotes.getdata()):
        assert(False), "Did not go to the right page"
    if list(Entregados.getdata()) == list(Spam.getdata()):
        assert(False), "Did not go to the right page"
    if list(Abiertos.getdata()) == list(Clicks.getdata()):
        assert(False), "Did not go to the right page"
    if list(Abiertos.getdata()) == list(Rebotes.getdata()):
        assert(False), "Did not go to the right page"
    if list(Abiertos.getdata()) == list(Spam.getdata()):
        assert(False), "Did not go to the right page"
    if list(Clicks.getdata()) == list(Rebotes.getdata()):
        assert(False), "Did not go to the right page"
    if list(Clicks.getdata()) == list(Spam.getdata()):
        assert(False), "Did not go to the right page"
    if list(Rebotes.getdata()) == list(Spam.getdata()):
        assert(False), "Did not go to the right page"

    #### if you wish to remove images from folder, uncomment following lines:###
    '''
    os.remove(Procesados.jpg)
    os.remove(Entregados.jpg)
    os.remove(Abiertos.jpg)
    os.remove(Clicks.jpg)
    os.remove(Rebotes.jpg)
    os.remove(Spam.jpg)
    '''

    print "Checking the 'Mensajes' tab"
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "icon-envelope", " " ))]').click()
    time.sleep(2)
    driver.save_screenshot("Original.jpg")
    print " Checking email filter"
    #email
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/div/input').send_keys("us1@mediconecta.com")
    time.sleep(2)

    #Search and Erase buttons vvvv
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/button[1]').click()
    time.sleep(3)
    driver.save_screenshot("Email.jpg")
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/button[2]').click()
    time.sleep(2)
    #Search and Erase buttons ^^^^

    print " Checking date filter"
    #dates
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/span[1]/span/input').send_keys("11/20/2016")
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/span[3]/span/input').send_keys("12/24/2016")
    time.sleep(2)

    #Search and Erase buttons vvvv
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/button[1]').click()
    time.sleep(3)
    driver.save_screenshot("Dates.jpg")
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/button[2]').click()
    time.sleep(2)
    #Search and Erase buttons ^^^^

    print " Checking category filter"
    #categoria
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[1]/div[3]/div/span/span').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[10]/div/span/input').send_keys("Contacto_Cambio_Login")
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[10]/div/span/input').send_keys(Keys.ENTER)
    time.sleep(2)

    #Search and Erase buttons vvvv
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/button[1]').click()
    time.sleep(3)
    driver.save_screenshot("Categoria.jpg")
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/button[2]').click()
    time.sleep(2)
    #Search and Erase buttons ^^^^

    print " Checking event filter"
    #Evento
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[1]/div[4]/div/span/span').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[9]/div/span/input').send_keys('Eliminados')
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[9]/div/span/input').send_keys(Keys.ENTER)

    time.sleep(3)

    #Search and Erase buttons vvvv
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/button[1]').click()
    time.sleep(3)
    driver.save_screenshot("Evento.jpg")
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/button[2]').click()
    time.sleep(2)
    #Search and Erase buttons ^^^^

    Original = Image.open("Original.jpg")
    Email = Image.open("Email.jpg")
    Dates = Image.open("Dates.jpg")
    Categoria = Image.open("Categoria.jpg")
    Evento = Image.open("Evento.jpg")

    if list(Original.getdata()) == list(Email.getdata()):
        assert(False), "Email search did not filter results"
    if list(Original.getdata()) == list(Dates.getdata()):
        assert(False), "Dates search did not filter results"
    if list(Original.getdata()) == list(Categoria.getdata()):
        assert(False), "Categoria search did not filter results"
    if list(Original.getdata()) == list(Evento.getdata()):
        assert(False), "Evento search did not filter results"

    #### if you wish to remove images from folder, uncomment following lines:###
    '''
    os.remove(Original.jpg)
    os.remove(Email.jpg)
    os.remove(Dates.jpg)
    os.remove(Categoria.jpg)
    os.remove(Evento.jpg)
    '''

    time.sleep(4)

def manejoDoctores(driver):
    time.sleep(3)

    dropDownName = driver.find_element_by_xpath('//*[@id="upLoginMaster"]/div/div')
    dropDownName.click()
    time.sleep(2)
    miCuenta = driver.find_element_by_xpath('//*[@id="lbMiCuenta"]/span')
    miCuenta.click()

    time.sleep(5)
    assert 'Mi Cuenta' in driver.title, 'Not taken to Mi Cuenta'

    doctores = driver.find_element_by_xpath('//*[@id="cphW_ucmicuentadoctor_liDoctores"]/a/span')
    doctores.click()
    time.sleep(3)


    print " Eliminando doctor.."

    """
    page2 = driver.find_element_by_xpath('//*[@id="listado-Doctores_paginate"]/ul/li[3]/a')
    page2.click()
    time.sleep(3)
    """

    trashCan = driver.find_element_by_xpath('//*[@id="cphW_ucmicuentadoctor_ctl32_rptTable_btnEliminar_5"]/i')
    trashCan.click()
    time.sleep(4)
    si = driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_btnEliminarDoctor")
    si.click()

    time.sleep(3)
    driver.refresh()

    try:
        Alert(driver).accept()
        time.sleep(6)
    except:
        pass

    time.sleep(3)
    doctores = driver.find_element_by_xpath('//*[@id="cphW_ucmicuentadoctor_liDoctores"]/a/span')
    doctores.click()
    time.sleep(3)

    assert "Demo AS" not in driver.page_source, "Doctor not deleted"

    print " Agregando doctor.."
    agregarDoctor = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_btnBuscar')
    agregarDoctor.click()
    time.sleep(4)

    buscar = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_txtBusqueda')
    buscar.send_keys('Demo AS')
    time.sleep(3)
    enter = driver.find_element_by_xpath('//*[@id="cphW_ucmicuentadoctor_ctl32_ctl08_btnBuscarDoctor"]/i')
    enter.click()
    time.sleep(3)

    agregar = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_rptTable_btnAgregarDoctor_0')
    agregar.click()
    time.sleep(3)
    si = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_btnAsociarDoctor')
    si.click()
    time.sleep(3)

    assert "Demo AS" in driver.page_source, "Doctor not added"


    print " Registrando doctor nuevo.."
    time.sleep(3)
    agregarDoctor = driver.find_element_by_xpath('//*[@id="cphW_ucmicuentadoctor_ctl32_btnBuscar"]/span')
    agregarDoctor.click()
    time.sleep(4)

    numbers = range(1000)
    number = numbers[random.randint(0,1000)]
    nombre = "AAAAA" + str(number)
    apellido = "Doctor" + str(number)

    buscar = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_txtBusqueda')
    buscar.send_keys(nombre + " " + apellido)
    time.sleep(3)
    enter = driver.find_element_by_xpath('//*[@id="cphW_ucmicuentadoctor_ctl32_ctl08_btnBuscarDoctor"]/i')
    enter.click()
    time.sleep(3)

    registarar = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_btnRegistrar')
    registarar.click()
    time.sleep(5)

    name = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_txtNombre')
    name.send_keys(nombre)

    last = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_txtApellido')
    last.send_keys(apellido)


    nat = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_ddlNacionalidad')
    nat.send_keys('Est' + Keys.RETURN)

    cedula = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_txtCedula')
    cedula.send_keys('56374857')

    dia = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_ucFecha_ddlDia')
    dia.send_keys('1' + Keys.RETURN)

    mes = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_ucFecha_ddlMes')
    mes.send_keys('1' + Keys.RETURN)

    yr = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_ucFecha_ddlAnno')
    yr.send_keys('2017' + Keys.RETURN)

    sexo = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_ddlSexo')
    sexo.send_keys('m' + Keys.RETURN)

    phone = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_txtCelular')
    phone.send_keys('3053053055')

    email = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_txtEmail')
    email.send_keys(nombre + apellido + "@mediconecta.com")

    title = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_txtTituloUniversitario')
    title.send_keys('Test Doctor')

    university = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_txtUniversidad')
    university.send_keys('Test University')

    specialty = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_txtEspecialidades')
    specialty.send_keys('Dentista' + Keys.RETURN)

    regNum = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_txtCodigoMedico')
    regNum.send_keys('123456789')

    otherNum = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_ucDatosDoctor_txtCodigoMedico2')
    otherNum.send_keys('123456789876543321')

    enter = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ctl08_btnRegistrarDoctor')
    enter.click()

    time.sleep(3)
    assert nombre in driver.page_source, 'New Doctor not registered'


    print " Editando informacion de doctor nuevo.."

    time.sleep(6)
    ver = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_rptTable_btnVer_15')
    ver.click()

    time.sleep(3)
    driver.save_screenshot('doctor1.jpg')
    time.sleep(2)

    cerrar = driver.find_element_by_xpath('//*[@id="hab_ctl00$cphW$ucmicuentadoctor$ctl32$ctl10"]/input')
    cerrar.click()
    time.sleep(2)

    editar = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_rptTable_btnEditar_15')
    editar.click()
    time.sleep(2)

    u = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ucDatosDoctor_txtTituloUniversitario')
    u.clear()
    u.send_keys('Doctor Test')

    university = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_ucDatosDoctor_txtUniversidad')
    university.clear()
    university.send_keys("Universidad Testing" + str(number) + Keys.RETURN)

    time.sleep(3)
    driver.refresh()
    try:
        Alert(driver).accept()
        time.sleep(6)
    except:
        pass
    time.sleep(3)
    doctores = driver.find_element_by_xpath('//*[@id="cphW_ucmicuentadoctor_liDoctores"]/a/span')
    doctores.click()
    time.sleep(3)


    ver = driver.find_element_by_id('cphW_ucmicuentadoctor_ctl32_rptTable_btnVer_15')
    ver.click()
    time.sleep(5)

    driver.save_screenshot('doctor2.jpg')

    cerrar = driver.find_element_by_xpath('//*[@id="hab_ctl00$cphW$ucmicuentadoctor$ctl32$ctl10"]/input')
    cerrar.click()
    time.sleep(2)

    img1 = Image.open('doctor1.jpg')
    img2 = Image.open('doctor2.jpg')

    if list(img1.getdata()) == list(img2.getdata()):
        assert False, "No changes occured after editing"



    print " Eliminando doctor nuevo.."

    time.sleep(3)
    trashCan = driver.find_element_by_xpath('//*[@id="cphW_ucmicuentadoctor_ctl32_rptTable_btnEliminar_15"]/i')
    trashCan.click()
    time.sleep(4)
    si = driver.find_element_by_id("cphW_ucmicuentadoctor_ctl32_btnEliminarDoctor")
    si.click()
    time.sleep(3)

start = time.time()
main(sys.argv[1:])
print "Execution Time: " + str(int((time.time() - start))) + " seconds"
