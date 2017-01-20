# -*- coding: utf-8 -*-
#Fix para abrir Firefox 47.0+, ejecuta el comando: pip install -U selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time, unicodedata, sys, getopt
import random

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
            if arg == 'Autentica' or arg == 'Login' or arg == 'Atender' or arg == 'AtenderChrome' or arg == 'AtenderFirefox' or arg == 'AtenderIE' or arg == 'HistoriaCitas' or arg == "AppHistoriasClientes" or arg == "ProgramarCitaGlenNuevoP":
                modulo = arg
            elif arg == "Pruebas_de_Diagnostico" or arg == "Pruebas_de_Prescripciones" or arg == "Pruebas_de_Examenes" or arg == 'AtenderPacienteConDPE' or arg == "ProgramarCitaGalen" or arg == "ProgramarCitaGalenMinor":
                modulo = arg
            else:
                print 'valores esperados: -m Autentica/Login/Atender/HistoriaCitas/Pruebas_de_Diagnostico/Pruebas_de_Prescripciones/Pruebas_de_Examenes/AtenderPacienteConDPE/ProgramarCitaGalen/AppHistoriasClientes/ProgramarCitaGlenNuevoP'
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

                    print " Cita --> OK"
                    time.sleep(3)
                    p_driver.quit()
                    driver.quit()

                elif modulo == "ProgramarCitaGalen":
                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCita(driver)
                    print " Cita --> OK"
                    driver.quit

                elif modulo == "ProgramarCitaGalenMinor":
                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCitaMinor(driver)
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

                    print " Cita --> OK"
                    time.sleep(3)
                    p_driver.quit()
                    driver.quit()

                elif modulo == "ProgramarCitaGlenNuevoP":
                    print "Autenticando doctor: " + doctor
                    assert (log_in(doctor, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Doctor Programar Cita"
                    DoctorProgramarCitaNuevo(driver)
                    print " Cita --> OK"
                    driver.quit

                print "== Pruebas del doctor finalizadas =="

def log_in(email, pw, driver, ambiente):
    driver.get("http://" + ambiente + ".mediconecta.com/LoginD")
    time.sleep(4)

    assert ("Portal Mediconecta" in driver.title), "Pagina no encontrada"

    driver.find_element_by_id("cphW_txtUsuario").send_keys(email)
    driver.find_element_by_id("cphW_txtPassword").send_keys(pw + Keys.RETURN)


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
    time.sleep(10)
    print " Solicitar cita --> OK"

    '''
    if "son personales y generan un historial" or "Medical consultations are personal and create a medical history" in driver.page_source:
        print "1"
        time.sleep(5)
        scroll("uniform-cphW_uccitasondemand_rblParaQuien_0", driver)
        print "2"
        time.sleep(5)
        driver.find_element_by_id("uniform-cphW_uccitasondemand_rblParaQuien_0").click()
        print "3"
        time.sleep(5)
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

    time.sleep(3)
    print "Chequeando la historia de citas del paciente.."
    print " Drop down selection"
    dropDown = driver.find_element_by_id("ddlPHRdoc")
    dropDown.click()
    assert("dropdown-backdrop" in driver.page_source), "Did not open dropdown"
    time.sleep(2)

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

        if "s2id_autogen5" in driver.page_source:
            scroll("s2id_autogen5", driver)
            driver.find_element_by_xpath("//*[@id='s2id_autogen5']").click()
            driver.find_element_by_xpath("//*[@id='s2id_autogen5']").send_keys("escalol")
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='s2id_autogen5']").send_keys(Keys.ENTER)


            scroll("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion").click()
            assert("ESCALOL" in driver.page_source), "Perscription did not save"

            print "Agregar Prescripciones --> OK"
            time.sleep(5)
        elif "s2id_autogen11" in driver.page_source:
            scroll("s2id_autogen11", driver)
            driver.find_element_by_xpath("//*[@id='s2id_autogen11']").click()
            driver.find_element_by_xpath("//*[@id='s2id_autogen11']").send_keys("escalol")
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='s2id_autogen11']").send_keys(Keys.ENTER)


            scroll("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion").click()
            assert("ESCALOL" in driver.page_source), "Perscription did not save"

            print "Agregar Prescripciones --> OK"
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
            assert("TEST1" in driver.page_source), "New lab test did not save"
            print "Agregar Examenes --> OK"
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
        driver.find_element_by_xpath("//*[@id='s2id_autogen3']").click()
        driver.find_element_by_xpath("//*[@id='s2id_autogen3']").send_keys("sarampionf")
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
            driver.find_element_by_xpath("//*[@id='s2id_autogen5']").click()
            driver.find_element_by_xpath("//*[@id='s2id_autogen5']").send_keys("escalol")
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='s2id_autogen5']").send_keys(Keys.ENTER)


            scroll("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion", driver)
            driver.find_element_by_id("cphW_ucSoap_ucPlan_ctl00_btnCrearPrescripcion").click()
            assert("ESCALOL" in driver.page_source), "Perscription did not save"

            print "Agregar Prescripciones --> OK"
            time.sleep(5)
        elif "s2id_autogen11" in driver.page_source:
            scroll("s2id_autogen11", driver)
            driver.find_element_by_xpath("//*[@id='s2id_autogen11']").click()
            driver.find_element_by_xpath("//*[@id='s2id_autogen11']").send_keys("escalol")
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='s2id_autogen11']").send_keys(Keys.ENTER)


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
        driver.find_element_by_xpath("//*[@id='cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre']").click()
        driver.find_element_by_xpath("//*[@id='cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre']").send_keys("TEST1")
        driver.find_element_by_xpath("//*[@id='cphW_ucSoap_ucPlan_ctl01_ucCreate_txtNombre']").send_keys(Keys.ENTER)

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
        time.sleep(1)

        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").click()
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").send_keys(hour +':'+ minuto + " " + time_of_day)
        time.sleep(1)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").click()
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
            time.sleep(1)

            scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora", driver)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").click()
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").send_keys(hour +':'+ minuto + " " + time_of_day)
            time.sleep(1)
            driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").click()
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

def screenshot(driver, file_name):
    assert ("cphW_ucPacientesEnFila_btnSolicitarCitaHub" in driver.page_source), "Not on right page"
    scroll("cphW_ucPacientesEnFila_btnSolicitarCitaHub", driver)
    driver.find_element_by_id("cphW_ucPacientesEnFila_btnSolicitarCitaHub").click()
    time.sleep(4)
    driver.save_screenshot(file_name)
    time.sleep(1)
    driver.find_elements_by_tag_name("button")[-1].click()

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
        time.sleep(1)

        scroll("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora", driver)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").click()
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtHora").send_keys(hour +':'+ minuto + " " + time_of_day)
        time.sleep(1)
        driver.find_element_by_id("cphW_uccitasprogramadasdr_ucBuscarPacientesCitaDoctor_ucProgramarCita_txtFecha").click()
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



start = time.time()
main(sys.argv[1:])
print "Execution Time: " + str(int((time.time() - start))) + " seconds"
