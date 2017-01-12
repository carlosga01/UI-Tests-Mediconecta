# -*- coding: utf-8 -*-
#Fix para abrir Firefox 47.0+, ejecuta el comando: pip install -U selenium
#http://chromedriver.storage.googleapis.com/index.html
#http://www.slimjet.com/chrome/google-chrome-old-version.php
#discard local changes --> git reset --hard

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.alert import Alert
import unicodedata, sys, getopt, time
import random

def main(argv):
    driver = ''
    navegador = ''
    ambiente = ''
    modulo = ''
    paciente = ''
    pacienteID = ''

    full_username = 'jenkins_full@mediconecta.com' #Pruebas de PHR y Especialistas
    username_chrome = "jenkins_chrome@mediconecta.com"
    username_chrome_vsee = "jenkins_chrome_vsee@mediconecta.com"
    username_firefox = "jenkins_firefox@mediconecta.com"
    username_firefox_vsee = "jenkins_firefox_vsee@mediconecta.com"
    username_ie = "jenkins_ie@mediconecta.com"
    username_ie_vsee = "jenkins_ie_vsee@mediconecta.com"
    external_id = 'jenkins_sso'
    password = "dba123"

    #active account
    act_nacionalidad = "Venezuela"
    act_cedula = "87654321"
    act_birthday = ["1","1","2016"]
    act_birthday_chrome = ["1","1","2016"]
    act_birthday_firefox = ["1","2","2016"]
    act_birthday_ie = ["1","3","2016"]

    #active doctor account
    dr_act_username_chrome = "jenkins_drchrome@mediconecta.com"
    dr_act_username_firefox = "jenkins_drfirefox@mediconecta.com"
    dr_act_username_ie = "jenkins_drie@mediconecta.com"
    dr_act_nacionalidad = "Venezuela"
    dr_act_cedula = "87654321"
    dr_act_birthday = ["1","1","2016"]
    dr_act_birthday_chrome = ["1","1","2016"]
    dr_act_birthday_firefox = ["1","2","2016"]
    dr_act_birthday_ie = ["1","3","2016"]

    #patient ID's for doctor
    IDPacienteDevChrome = 'a0HZ0000007gYqP'   #Pruebas Jenkins Chrome
    IDPacienteDevFirefox = 'a0HZ0000007gYqU'   #Pruebas Jenkins Firefox
    IDPacienteDevIE = 'a0HZ0000007gYqZ'   #Pruebas Jenkins IE

    IDPacienteProdChrome = 'a0HU000000M20fF'   #Pruebas Jenkins Chrome
    IDPacienteProdFirefox = 'a0HU000000M21DL'   #Pruebas Jenkins Firefox
    IDPacienteProdIE = 'a0HU000000M21Du'   #Pruebas Jenkins IE

    dr_password = "dba123"

    #inactive account
    inact_username = "inactivo@mediconecta.com"
    inact_nacionalidad = "Venezuela"
    inact_cedula = "87654322"
    inact_birthday = ["5", "5", "2016"]


    try:
      opts, args = getopt.getopt(argv,"d:a:m:")
    except getopt.GetoptError:
        print 'SINTAXIS: paciente.py -d Chrome/Firefox/Ie -a portaldev/testprod/consultas -m Autentica/Login/CitaODVsee/CitaODTokbox/CitaODTokboxAtender/Phr/MiCuenta/SSO/ForzarCache'
        sys.exit(2)

    for opt, arg in opts:
        if opt in('-h', '--h', '-help', '--help'):
            print 'SINTAXIS: paciente.py -d Chrome/Firefox/Ie -a portaldev/testprod/consultas -m Autentica/Login/CitaODVsee/CitaODTokbox/CitaODTokboxAtender/Phr/MiCuenta/SSO/ForzarCache'
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
            if arg == 'portaldev' or arg == 'testprod' or arg == 'consultas' or arg == 'mercantilseguros' or arg == 'mercantilsegurosdev':
                ambiente = arg

                if ambiente == 'portaldev':
                    if navegador == 'Chrome':
                        pacienteID = IDPacienteDevChrome
                    elif navegador == 'Firefox':
                        pacienteID = IDPacienteDevFirefox
                    elif navegador == 'Ie':
                        pacienteID = IDPacienteDevIE
                else:
                    if navegador == 'Chrome':
                        pacienteID = IDPacienteProdChrome
                    elif navegador == 'Firefox':
                        pacienteID = IDPacienteProdFirefox
                    elif navegador == 'Ie':
                        pacienteID = IDPacienteProdIE

            else:
                print 'valores esperados: -a portaldev / testprod / consultas / mercantilseguros / mercantilsegurosdev'
                sys.exit()


        elif opt in ("-m", "--m"):
            #Setear modulo
            if arg == 'Login' or arg == 'ForzarCache' or arg == 'Autentica' or arg == 'CitaODVSee' or arg == 'CitaODVSeeGeneral' or arg == 'CitaODTokbox' or arg == 'ProgramarCitaGeneral' or arg == 'CitaODTokboxEsp' or arg == 'ProgramarCitaEspecial':
                modulo = arg
            elif arg == 'CitaODTokboxGeneral' or arg == 'CitaODTokboxAtender' or arg == 'Phr' or arg == 'MiCuenta' or arg == 'SSO' or arg == 'AppMisCitas' or arg == 'AtenderCitaProgramada' or arg == 'OpcionesSinEspecialidades':
                modulo = arg
            else:
                print 'valores esperados: -m Autentica/Login/CitaODVSee/CitaODVSeeGeneral/CitaODTokbox/CitaODTokboxAtender/CitaODTokboxGeneral/Phr/MiCuenta/SSO/ForzarCache/ProgramarCitaGeneral/ProgramarCitaEspecial/CitaODTokboxEsp/AppMisCitas/AtenderCitaProgramada/OpcionesSinEspecialidades'
                sys.exit()

            if ambiente != '':
                if navegador == 'Chrome':
                    driver = webdriver.Chrome()
                    act_birthday = act_birthday_chrome
                    if modulo == 'CitaODTokbox' or modulo == 'CitaODTokboxAtender' or modulo == 'CitaODTokboxGeneral' or modulo == 'ProgramarCitaGeneral' or modulo == 'ProgramarCitaEspecial' or modulo == 'CitaODTokboxEsp' or modulo == 'AtenderCitaProgramada':
                        paciente = username_chrome
                    else:
                        paciente = username_chrome_vsee

                elif navegador == 'Firefox':
                    driver = webdriver.Firefox()
                    act_birthday = act_birthday_firefox
                    if modulo == 'CitaODTokbox' or modulo == 'CitaODTokboxAtender' or modulo == 'CitaODTokboxGeneral' or modulo == 'ProgramarCitaGeneral' or modulo == 'ProgramarCitaEspecial' or modulo == 'CitaODTokboxEsp' or modulo == 'AtenderCitaProgramada':
                        paciente = username_firefox
                    else:
                        paciente = username_firefox_vsee

                elif navegador == 'Ie':
                    driver = webdriver.Ie()
                    act_birthday = act_birthday_ie
                    if modulo == 'CitaODTokbox' or modulo == 'CitaODTokboxAtender' or modulo == 'CitaODTokboxGeneral' or modulo == 'ProgramarCitaGeneral' or modulo == 'ProgramarCitaEspecial'or modulo == 'CitaODTokboxEsp' or modulo == 'AtenderCitaProgramada':
                        paciente = username_ie
                    else:
                        paciente = username_ie_vsee


                ## COMIENZAN LAS PRUEBAS
                #driver.set_window_size(800,600)
                driver.maximize_window()
                driver.implicitly_wait(20)
                #driver.get("http://" + ambiente + ".mediconecta.com")

                print "Comenzando Pruebas: " + ambiente + " en " + navegador


                if modulo == 'ForzarCache':
                    print "Proceso: ForzandoCache"
                    forzar_cache(driver, ambiente)
                    #assert (log_in(paciente, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    #print " Paciente autenticado (" + paciente + ") --> OK"

                elif modulo == 'Autentica':
                    print "Proceso: Solo validar autenticacion correcta"
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Paciente autenticado (" + paciente + ") --> OK"
                    #if "firefox" not in str(driver):
                    assert (log_out(driver) == "exitoso"), "Logout fallido"
                    print " Cerrar sesion (" + paciente + ") --> OK"

                elif modulo == 'Login':
                    print "Proceso: Autenticacion y sus variantes"
                    print "Recuperar Usuario.."
                    assert (Recuperar_Usuario(act_nacionalidad, act_cedula, act_birthday[0], act_birthday[1], act_birthday[2], driver, ambiente) == "exitoso"),"With correct info: Recuperar usuario wrong"
                    print " Paciente correcto (" + paciente + ") --> OK"
                    assert (Recuperar_Usuario(inact_nacionalidad, inact_cedula, inact_birthday[0], inact_birthday[1], inact_birthday[2], driver, ambiente) == "inactivo"),"With inactive info: Recuperar usuario wrong"
                    print " Paciente inactivo --> OK"
                    assert (Recuperar_Usuario('Estados Unidos','wrong','6','2','1996', driver, ambiente) == "fallido"), "With wrong info: Recuperar usuario wrong"
                    print " Paciente incorrecto --> OK"

                    print "Recuperar Contrasena.."
                    assert (Recuperar_Contrasena(paciente, driver, ambiente) == "exitoso"), "With correct email: Recuperar contrasena fallida"
                    print " Paciente correcto (" + paciente + ") --> OK"
                    #assert (Recuperar_Contrasena(paciente, driver, ambiente) == "Inactive"), "With inactive email: Recuperar contrasena fallida"
                    #print " Paciente inactivo --> OK"
                    assert (Recuperar_Contrasena('error@mediconecta.com', driver, ambiente) == "fallido"), "With incorrect email: Recuperar contrasena fallida"
                    print " Paciente incorrecto --> OK"

                    print "Autenticacion.."
                    assert (log_in('wrong@mediconecta.com','wrong', driver, ambiente) == "fallido"), "With incorrect login: Autenticacion fallida"
                    print " Paciente incorrecto --> OK"
                    #assert (log_in(paciente, password, driver, ambiente) == "inactivo"), "With inactive account: login failure"
                    #print " Paciente inactivo --> OK"
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Paciente autenticado (" + paciente + ") --> OK"

                    #if "firefox" not in str(driver):
                    assert (log_out(driver) == "exitoso"), "Logout fallido"
                    print " Cerrar sesion (" + paciente + ") --> OK"

                elif modulo == 'SSO':
                    print "Proceso: Validar autenticacion SSO"
                    assert (sso(external_id, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Paciente autenticado (" + external_id + ") --> OK"
                    #if "firefox" not in str(driver):
                    assert (log_out(driver) == "exitoso"), "Logout fallido"
                    print " Cerrar sesion (" + external_id + ") --> OK"

                elif modulo == 'Phr':
                    print "Autenticando paciente: " + paciente
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"
                    print "Proceso: PHR"
                    Historia_Medica(driver)
                    print "Proceso PHR --> OK"

                elif modulo == 'MiCuenta':
                    print "Autenticando paciente: " + paciente
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"
                    print "CambiarSexo"
                    Editar_Sexo("Masculino", driver)
                    print " Sexo cambiado (Masculino) --> OK"
                    Editar_Sexo("Femenino", driver)
                    print " Sexo cambiado (Femenino) --> OK"

                    print "CambiarIdioma"
                    Cambiar_Idioma(driver)
                    print " Cambio de idioma --> OK"

                    ##if old password inputted is wrong
                    #assert (Cambiar_Contrasena('notgood','irrelevant', driver) == "Cambio de contrasena no paso"),"Cambio de contrasena con inputs incorrectos fallo"
                    #driver.find_element_by_id("hab_ctl00$cphW$ucmicuenta$ctl20").click()
                    #print " CambiarContrasena - clave actual incorrecta (" + paciente + ") --> OK"

                    #driver.find_element_by_link_text("Mi Cuenta").click()
                    #assert (Cambiar_Contrasena(act_pw,'newtesting', driver) == "Cambio de contrasena paso"), "Cambio de contrasena con inputs correctos fallo"
                    #driver.find_element_by_id("hab_ctl00$cphW$ucmicuenta$ctl20").click()
                    #print " CambiarContrasena - clave correcta (" + paciente + ") --> OK"

                    #log_out()
                    #print " Cerrar sesion para probar nueva clave (" + paciente + ")"
                    #log_in(paciente,'newtesting')
                    #driver.find_element_by_link_text("Mi Cuenta").click()
                    #Cambiar_Contrasena('newtesting',act_pw)

                    #print "CambiarContrasena (" + paciente + ") --> OK"

                    #if "firefox" not in str(driver):
                    assert (log_out(driver) == "exitoso"), "Logout fallido"
                    print " Cerrar sesion (" + paciente + ") --> OK"

                elif modulo == 'CitaODVSee':
                    print "Autenticando paciente: " + paciente
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"
                    print "Proceso: Cita OnDemand VSee"
                    CitaODVSee(driver, ambiente)

                elif modulo == 'CitaODVSeeGeneral':

                    print "Autenticando paciente: " + paciente
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    #print "Autenticando doctor: " + dr_act_username_chrome
                    #assert (log_in_dr(dr_act_username_chrome, dr_password, dr_driver, ambiente) == "exitoso")
                    #print " Autenticacion --> OK"

                    print "Proceso: Cita OnDemand VSee"
                    CitaODVSee(driver, ambiente)

                    time.sleep(2)

                    #print "Proceso: Atender Paciente"
                    #AtenderPaciente(pacienteID, dr_driver)

                    #print "Proceso: Logging out doctor"
                    time.sleep(2)

                    #log_out(dr_driver)
                    #print " Logout doctor --> OK"
                    dr_driver.quit()

                    #print "Proceso: Llenando Encuesta"
                    #FillEncuesta(driver, 3)
                    #print " Encuesta --> OK"

                    #print "Processo: Logging out paciente"
                    #time.sleep(2)
                    #log_out(driver)
                    #print " Logout paciente --> OK"
                    driver.quit()

                elif modulo == 'CitaODTokbox':
                    print "Autenticando paciente: " + paciente
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"
                    print "Proceso: Cita OnDemand Tokbox"
                    CitaODTokbox(driver, ambiente, "no")

                elif modulo == 'CitaODTokboxAtender':
                    print "Autenticando paciente: " + paciente
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"
                    print "Proceso: Cita OnDemand Tokbox"
                    CitaODTokbox(driver, ambiente, "si")

                elif modulo == 'CitaODTokboxGeneral':

                    print "Autenticando paciente: " + paciente
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Cita OnDemand Tokbox"
                    CitaODTokbox(driver, ambiente, "si")
                    print "Paciente en sala de espera --> OK"

                    dr_driver = webdriver.Chrome()
                    dr_driver.maximize_window()
                    dr_driver.implicitly_wait(20)

                    print "Autenticando doctor: " + dr_act_username_chrome
                    assert (log_in_dr(dr_act_username_chrome, dr_password, dr_driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    time.sleep(5)

                    print "Proceso: Atender Paciente"
                    AtenderPaciente(pacienteID, dr_driver)

                    print " Cita --> OK"

                    time.sleep(3)

                    dr_driver.quit()

                    print "Proceso: Llenando Encuesta"
                    option = random.randint(1,5)
                    FillEncuesta(driver, option)
                    print " Encuesta llenada --> OK"

                    time.sleep(3)
                    driver.quit()

                elif modulo == 'ProgramarCitaGeneral':

                    print "Autenticando paciente:" + paciente
                    assert(log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Programar Cita General"
                    programarCitaGeneral(driver)
                    print "Programar Cita General --> OK"

                elif modulo == 'ProgramarCitaEspecial':
                    print "Autenticando paciente:" + paciente
                    assert(log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    options = ['Nutrición', 'Pediatría','Psicología']
                    choice = random.randint(0,len(options)-1)

                    especialista = options[choice]
                    #especialista = ""

                    print "Cita de: " + especialista

                    print "Proceso: Programar Cita con Especialista"
                    programarCitaEspecial(driver, especialista)
                    print "Programar Cita con Especialista --> OK"

                    driver.quit()

                elif modulo == 'CitaODTokboxEsp':
                    print "Autenticando paciente: " + paciente
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    options = ['Nutrición','Psicología']
                    choice = random.randint(0,len(options)-1)

                    #especialista = options[choice]

                    especialista = "Psicología"

                    print "Proceso: Cita OnDemand con Especialista Tokbox"
                    citaODTokboxEsp(driver, especialista)
                    print " Paciente en sala de espera --> OK"

                    dr_driver = webdriver.Chrome()
                    dr_driver.maximize_window()
                    dr_driver.implicitly_wait(20)

                    print "Autenticando doctor: " + dr_act_username_chrome
                    assert (log_in_dr(dr_act_username_chrome, dr_password, dr_driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    time.sleep(5)

                    print "Proceso: Atender Paciente"
                    AtenderPaciente(pacienteID, dr_driver)
                    print " Cita --> OK"

                    time.sleep(3)

                    dr_driver.quit()

                    print "Proceso: Llenando Encuesta"
                    option = random.randint(1,5)
                    FillEncuesta(driver, option)
                    print " Encuesta llenada --> OK"

                    time.sleep(3)
                    driver.quit()

                elif modulo == 'AtenderCitaProgramada':
                    print "Autenticando paciente:" + paciente
                    assert(log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Ir a la cita programada"
                    atenderCitaProgramada(driver)
                    print " Paciente esperando por el doctor"

                    dr_driver = webdriver.Chrome()
                    dr_driver.maximize_window()
                    dr_driver.implicitly_wait(20)

                    print "Autenticando doctor:" + dr_act_username_chrome
                    assert (log_in_dr(dr_act_username_chrome, dr_password, dr_driver, ambiente) == "exitoso"), "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    time.sleep(5)

                    print "Proceso: Atender Paciente Programado"
                    #TO BE IMPLEMENTED
                    AtenderPaciente(pacienteID, dr_driver)
                    print " Cita --> OK"

                    time.sleep(3)
                    dr_driver.quit()

                    print "Proceso: Llenando Encuesta"
                    option = random.randint(1,5)
                    FillEncuesta(driver, option)
                    print " Encuesta llenada --> OK"
                    time.sleep(3)
                    driver.quit()

                elif modulo == 'AppMisCitas':
                    print "Autenticando paciente: " + paciente
                    assert (log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Processo: Testing App Mis Citas"
                    AppMisCitas(driver)
                    print "App Mis Citas --> OK"

                elif modulo == 'OpcionesSinEspecialidades':
                    print "Autenticando paciente:" + paciente
                    assert(log_in(paciente, password, driver, ambiente) == "exitoso") , "With correct login: Autenticacion fallida"
                    print " Autenticacion --> OK"

                    print "Proceso: Opciones Sin Especialidades"
                    OpcionesSinEspecialidades(driver)
                    print "Opciones Sin Especialidades --> OK"

                    driver.quit()


                print "== Pruebas del paciente finalizadas =="

def forzar_cache(driver, ambiente):
    driver.get("http://" + ambiente + ".mediconecta.com/Tareas?ForzarCache=1")
    print "Se establece tiempo de espera 60 segundos"
    time.sleep(60)

def log_in(email, pw, driver, ambiente):
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

def log_out(driver):
    scroll_top(driver)
    driver.find_element_by_id("lblUsuario").click()
    driver.find_element_by_id("lbCerrar").click()
    time.sleep(3)
    if "Ingresa a tu cuenta" or "Mercantil Seguros" in driver.page_source:
        return "exitoso"
    else:
        return "fallido"

def sso(external_id, driver, ambiente):
    lid = 'ckb5jgJDEFz2D9QmOfqoII4aqzyFDFnq2xIXC8qGrI1rBPfQ4wLUE2%2ffSsOMVxAat1%2bS4nojeBRYWz4lhIZ7WhYMLmA1E1YjnABVz%2bWMr9rtlkJB1p3EUG3uxc%2fcrB3vi7cRPoCugKx1E9KpTLB4QJVCFagDm0gunThuBwGcRTY%3d'

    driver.get("http://" + ambiente + ".mediconecta.com/Login.aspx?Partner=MercantilSeguros&LID=" + lid)
    time.sleep(3)

    if "Terminos" in driver.current_url:
        scroll("cphW_btnAceptar", driver)
        driver.find_element_by_id("cphW_btnAceptar").click()
        print " Aceptar Terminos --> OK"
        time.sleep(3)


    #imgSplash = driver.find_element_by_id('dialogintro')
    #if imgSplash != '':
    #    imgSplash.click()
    #    time.sleep(2)


    #if "dialogintro" in driver.page_source:
    #    driver.find_element_by_id("dialogintro").click()


    if "Solicitud de Citas" in driver.page_source: #if login works
        return "exitoso"
    if "e-visit" in driver.page_source: #if login works
        return "exitoso"
    if "El usuario ingresado" in driver.page_source: #if inactive notice pops up
        return "inactivo"
    return "fallido" #if log in doesnt work

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

def Recuperar_Usuario(Nacionalidad, Cedula, dia, mes, anno, driver, ambiente):
    driver.get("http://" + ambiente + ".mediconecta.com")
    time.sleep(3)

    if "Login" in driver.title:
        print ' Abriendo modal RecuperarUsuario..'
        scroll("cphW_lnkRecuperarUsuario", driver)
        driver.find_element_by_id("cphW_lnkRecuperarUsuario").click()
        time.sleep(3)

        if "Nacionalidad" in driver.page_source:
            #assert ("Nacionalidad" in driver.page_source), "Recuperar usuario no pide datos necesarios"
            scroll("cphW_ucRecuperarUsuario_ddlPais_ddlPais", driver)
            driver.find_element_by_id("cphW_ucRecuperarUsuario_ddlPais_ddlPais").send_keys(Nacionalidad)
            scroll("cphW_ucRecuperarUsuario_txtCedula", driver)
            driver.find_element_by_id("cphW_ucRecuperarUsuario_txtCedula").send_keys(Cedula)
            scroll("cphW_ucRecuperarUsuario_ucFecha_ddlDia", driver)
            driver.find_element_by_id("cphW_ucRecuperarUsuario_ucFecha_ddlDia").send_keys(dia)
            scroll("cphW_ucRecuperarUsuario_ucFecha_ddlMes", driver)
            driver.find_element_by_id("cphW_ucRecuperarUsuario_ucFecha_ddlMes").send_keys(mes)
            scroll("cphW_ucRecuperarUsuario_ucFecha_ddlAnno", driver)
            driver.find_element_by_id("cphW_ucRecuperarUsuario_ucFecha_ddlAnno").send_keys(anno + Keys.RETURN)
            time.sleep(4)
            if "Te enviamos un correo" in driver.page_source:
                return "exitoso"
            elif "proporcionada no corresponde" in driver.page_source:
                return "fallido"
            else:
                return "inactivo"
        else:
            print ' No encontrado modal RecuperarUsuario'
            sys.exit(-1)
    else:
        print ' Pagina no encontrada'
        sys.exit(-1)

def Recuperar_Contrasena(email, driver, ambiente):
    driver.get("http://" + ambiente + ".mediconecta.com")
    time.sleep(3)

    if "Login" in driver.title:
        print ' Abriendo modal RecuperarPassword..'
        scroll("cphW_lnkRecuperarPassword", driver)
        driver.find_element_by_id("cphW_lnkRecuperarPassword").click()
        time.sleep(3)

        if "Nombre de Usuario" in driver.page_source:
            scroll("cphW_ucRecuperarPassword_txtUsuario", driver)
            driver.find_element_by_id("cphW_ucRecuperarPassword_txtUsuario").send_keys(email + Keys.RETURN)
            time.sleep(4)
            if "Te enviamos un correo" in driver.page_source:
                return "exitoso"
            elif "proporcionada no corresponde" in driver.page_source:
                return "fallido"
            else:
                return "inactivo"
        else:
            print ' No encontrado modal RecuperarPassword'
            sys.exit(-1)
    else:
        print ' Pagina no encontrada'
        sys.exit(-1)

    #if "Te enviamos un correo con un" in driver.page_source: #password recovery was successful
    #    return "Success"
    #elif "inactivo" in driver.page_source: #email inputted corresponds to inactive account
    #    return "Inactive"
    #return "Fail" #password recovery was not successful

#must happen after log in
def Editar_Mis_Datos(new_address, driver):
    #if "Mi Cuenta" in driver.page_source:
    #    driver.find_element_by_link_text("Mi Cuenta").click()
    #else:
    #    driver.find_element_by_link_text("My Account").click()

    scroll("lblUsuario", driver)
    driver.find_element_by_id("lblUsuario").click()
    driver.find_element_by_id("lbMiCuenta").click()
    time.sleep(1)

    if "Editar" in driver.page_source:
        driver.find_element_by_link_text("Editar").click()
    else:
        driver.find_element_by_link_text("Edit").click()

    #assert ("Editar" in driver.page_source), "Button de editar datos was not found."
    #scroll("cphW_ucmicuenta_btnEditarDatos", driver)
    #driver.find_element_by_id("cphW_ucmicuenta_btnEditarDatos").click()
    time.sleep(2)
    if "Mis datos" in driver.page_source:
        return True
    elif "Personal Information" in driver.page_source:
        return True
    else:
        print "boton Editar Datos no fue encontrado"
        sys.exit()

    #assert ("Mis Datos" in driver.page_source), "Editar no funciona"
    scroll("cphW_ucmicuenta_btnGuardarDatos", driver)
    #Editar direction
    driver.find_element_by_id("cphW_ucmicuenta_ucDatosEditar_txtDireccion").send_keys(new_address)
    driver.find_element_by_id("cphW_ucmicuenta_btnGuardarDatos").click() #save
    time.sleep(5)
    assert (new_address in driver.page_source), "Change wasn't made in editar datos"
    #remove direction added
    scroll("cphW_ucmicuenta_btnEditarDatos", driver)
    driver.find_element_by_id("cphW_ucmicuenta_btnEditarDatos").click()
    scroll("cphW_ucmicuenta_btnGuardarDatos", driver)
    driver.find_element_by_id("cphW_ucmicuenta_ucDatosEditar_txtDireccion").clear()
    driver.find_element_by_id("cphW_ucmicuenta_btnGuardarDatos").click()
    time.sleep(5)
    assert (new_address not in driver.page_source), "previous address wasn't deleted"

def Editar_Sexo(sexo, driver):
    #if "Mi Cuenta" in driver.page_source:
    #    driver.find_element_by_link_text("Mi Cuenta").click()
    #else:
    #    driver.find_element_by_link_text("My Account").click()
    #time.sleep(2)

    #scroll_top(driver)
    scroll("lblUsuario", driver)
    driver.find_element_by_id("lblUsuario").click()
    driver.find_element_by_id("lbMiCuenta").click()

    time.sleep(2)
    scroll("cphW_ucmicuenta_btnEditarDatos", driver)
    driver.find_element_by_id("cphW_ucmicuenta_btnEditarDatos").click()
    scroll("cphW_ucmicuenta_ucDatosEditar_ddlSexo", driver)
    driver.find_element_by_id("cphW_ucmicuenta_ucDatosEditar_ddlSexo").send_keys(sexo)
    scroll("cphW_ucmicuenta_btnGuardarDatos", driver)
    driver.find_element_by_id("cphW_ucmicuenta_btnGuardarDatos").click()
    Check_cambio_de_sexo(sexo, driver)

def Check_cambio_de_sexo(sexo, driver): #look if antecendentes gineco obstetricos in historias medicas
    scroll_top(driver)
    if u'HISTORIAS MÉDICAS' in driver.page_source:
        driver.find_element_by_link_text(u'HISTORIAS MÉDICAS').click()
    else:
        driver.find_element_by_link_text("HEALTH RECORD").click()
    time.sleep(2)

    if is_id_in_page("cphW_ucphr_liAntecedentesGinecoObstetricos", driver) == True:
        assert (sexo == "Femenino"), "Cambio de sexo no funciono"

def Cambiar_Idioma(driver): #check if idioma was actually edited
    #if "Mi Cuenta" in driver.page_source:
    #    driver.find_element_by_link_text("Mi Cuenta").click()
    #else:
    #    driver.find_element_by_link_text("My Account").click()
    #time.sleep(2)

    #scroll_top(driver)
    scroll("lblUsuario", driver)
    driver.find_element_by_id("lblUsuario").click()
    driver.find_element_by_id("lbMiCuenta").click()
    time.sleep(2)

    scroll("cphW_ucmicuenta_liLanguage", driver)
    driver.find_element_by_id("cphW_ucmicuenta_liLanguage").click()
    #if "Cambiar Idioma" in driver.page_source:
    #    driver.find_element_by_link_text("Cambiar Idioma").click()
    #else:
    #    driver.find_element_by_link_text("Change Language").click()

    #assert ("Cambiar Idioma" in driver.page_source), "Cambiar Idioma no es una option bajo Mi Cuenta"
    #driver.find_element_by_link_text("Cambiar Idioma").click()
    time.sleep(2)
    #change language to english
    assert ("cphW_ucmicuenta_ucSelectorIdioma_ddlIdiomas" in driver.page_source), "Botton de cambiar idiomas no funciona"
    idioma = Select(driver.find_element_by_id("cphW_ucmicuenta_ucSelectorIdioma_ddlIdiomas"))
    idioma.select_by_index(0)
    driver.find_element_by_id("cphW_ucmicuenta_btnGuardarIdioma").click()
    time.sleep(3)
    #check if language was changed
    #assert ("My Account" in driver.page_source), "Idioma no fue cambiado"
    #change language back to spanish

    if "Cambiar Idioma" in driver.page_source:
        driver.find_element_by_link_text("Cambiar Idioma").click()
    else:
        driver.find_element_by_link_text("Change Language").click()
    time.sleep(2)

    idioma = Select(driver.find_element_by_id("cphW_ucmicuenta_ucSelectorIdioma_ddlIdiomas"))
    idioma.select_by_index(1)
    driver.find_element_by_id("cphW_ucmicuenta_btnGuardarIdioma").click()

def Cambiar_Contrasena(password_old, password_new, driver):
    time.sleep(2)
    assert ("cphW_ucmicuenta_liLoginInformation" in driver.page_source), "Login information no es una option bajo Mi Cuenta"
    driver.find_element_by_id("cphW_ucmicuenta_liLoginInformation").click()
    time.sleep(2)
    assert ("cphW_ucmicuenta_liCambiarPassword" in driver.page_source), "Cambiar Password no es una option bajo Login information"
    driver.find_element_by_id("cphW_ucmicuenta_liCambiarPassword").click()
    time.sleep(3)
    assert ("cphW_ucmicuenta_ucCambiarPassword_txtPassword" in driver.page_source), "El botton de cambiar password no funciona"
    driver.find_element_by_id("cphW_ucmicuenta_ucCambiarPassword_txtPassword").send_keys(password_old)
    driver.find_element_by_id("cphW_ucmicuenta_ucCambiarPassword_txtNewPassword").send_keys(password_new)
    driver.find_element_by_id("cphW_ucmicuenta_ucCambiarPassword_txtConfirmaNewPassword").send_keys(password_new)
    driver.find_element_by_link_text("Guardar").click()
    time.sleep(5)
    if "fue modificada exitosamente" in driver.page_source: #password was changed to new
        return "Cambio de contrasena paso"
    if "errada" in driver.page_source: #old password was wrong
        return "Cambio de contrasena no paso"

def CitaODVSee(driver, ambiente):
    time.sleep(20)
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
        time.sleep(5)
        driver.find_element_by_id("cphW_uccitasondemand_btnOnDemandIntermedia").click()
    else:
        scroll("cphW_uccitasondemand_btnSolicitarCita", driver)
        driver.find_element_by_id("cphW_uccitasondemand_btnSolicitarCita").click()
    time.sleep(5)
    print " Solicitar cita --> OK"


    if "son personales y generan un historial" or "Medical consultations are personal and create a medical history" in driver.page_source:
        scroll("uniform-cphW_uccitasondemand_rblParaQuien_0", driver)
        driver.find_element_by_id("uniform-cphW_uccitasondemand_rblParaQuien_0").click()
        scroll("cphW_uccitasondemand_btnContinuarDep", driver)
        driver.find_element_by_id("cphW_uccitasondemand_btnContinuarDep").click()
        print " Seleccionar Paciente --> OK"



    if "firefox" in str(driver):
        if "Para continuar por favor instala nuestra" in driver.page_source:
            print " VSee no esta instalado en el equipo"
            print " Simulando instalacion VSee.."

            scroll("cphW_ucValidacionVC_btnDescargaVSee", driver)
            driver.find_element_by_id("cphW_ucValidacionVC_btnDescargaVSee").click()

            ConfiguracionVSee(driver, ambiente)

            print " Cita --> OK"


        elif "Si recibes este mensaje por favor acepta" or "If you get this message" in driver.page_source:
            scroll("cphW_ucValidacionVC_btnModalCita", driver)
            driver.find_element_by_id("cphW_ucValidacionVC_btnModalCita").click()

            print " Cita --> OK"

        else:
            print " Cita no realizada"


    else:

        if "Para continuar por favor instala nuestra" or "To continue please install our video-conference application" in driver.page_source:
            scroll("hab_ctl00$cphW$ucValidacionVC$btnDescargaVSee", driver)
            driver.find_element_by_id("hab_ctl00$cphW$ucValidacionVC$btnDescargaVSee").click()
            print " Comenzar Proceso ValidacionVC --> OK"
            time.sleep(3)

            ConfiguracionVSee(driver, ambiente)

            if "Si recibes este mensaje por favor acepta" or "If you get this message" in driver.page_source:
                scroll("cphW_ucValidacionVC_btnModalCita", driver)
                driver.find_element_by_id("cphW_ucValidacionVC_btnModalCita").click()


            if "" or "The expected wait time may" in driver.page_source:
                print "5"
                scroll("hab_ctl00$cphW$ucCita$ctl16", driver)
                driver.find_element_by_id("hab_ctl00$cphW$ucCita$ctl16").click()

            print " Cita --> OK"


        elif "Por favor espera mientras" or "Please wait while the doctor" in driver.page_source:
                scroll("cphW_ucCita_btnCitaFinalizarPpal", driver)
                driver.find_element_by_id("cphW_ucCita_btnCitaFinalizarPpal").click()

                #driver.back()

                if "Abandonar" or "Leave" in driver.page_source:
                    scroll("cphW_ucCita_btnAceptarFinalizar", driver)
                    driver.find_element_by_id("cphW_ucCita_btnAceptarFinalizar").click()

        else:
            print " Cita no realizada"

    ######if chrome external protocol appears, get rid of it... change_chrome_settings
    #assert ("Por favor espera mientras el Dr." in driver.page_source), "video conference did not begin"

def ConfiguracionVSee(driver, ambiente):
    if "Configura tu computadora" or "Setup your computer" in driver.page_source:
        scroll("cphW_hlIniciarConfiguracion", driver)
        driver.find_element_by_id("cphW_hlIniciarConfiguracion").click()
        print " Iniciar Configuracion --> OK"
        time.sleep(3)


    if "Sigue los pasos para instalar" or "Follow the steps to install" in driver.page_source:
        #driver.find_element_by_id("cphW_btnDescargar_Win").click()
        print " Descargar VSee --> OK"
        time.sleep(3)

    #assert ("Si ya instalaste" in driver.page_source), "Boton para continuar instalacion"
    #driver.find_element_by_id("cphNav_hlImgBtnContinuar").click()
    print " Finalizar Descarga VSee --> OK"
    driver.get("http://" + ambiente + ".mediconecta.com/Modulos/Descargas/Instalar")
    time.sleep(3)

    print " Finalizar Instalacion VSee --> OK"
    driver.get("http://" + ambiente + ".mediconecta.com/Modulos/Descargas/Ejecutar")
    time.sleep(5)


    if "Permisos y Pruebas" or "Permissions and Tests" in driver.page_source:
        scroll("cphW_btnDescargar", driver)
        driver.find_element_by_id("cphW_btnDescargar").click()
        print " Abriendo Modal VSee --> OK"
        time.sleep(5)

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
    time.sleep(5)
    print " Solicitar cita --> OK"


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

def Historia_Medica(driver):
    time.sleep(2)
    if u'HISTORIAS MÉDICAS' in driver.page_source:
        driver.find_element_by_link_text(u'HISTORIAS MÉDICAS').click()
    else:
        driver.find_element_by_link_text("HEALTH RECORD").click()
    time.sleep(2)
    assert ("tabResumen" in driver.page_source), "Historias medicas tab no funciona"

    alergies = ["cphW_ucphr_liAlergias","cphW_ucphr_ctl18_btnCrear","cphW_ucphr_ctl18_ucCreate_txtNombre","cphW_ucphr_ctl18_btnCrearAlergia",None]
    list_to_eliminate = ["cphW_ucphr_ctl18_rptTable_btnEliminar_0","cphW_ucphr_ctl18_btnEliminarModal"]
    testing_different_inputs(alergies,'SOMETHING RIGHT','',list_to_eliminate,None,driver)
    print " Alergia --> OK"
    time.sleep(2)

    ant_patol = ["cphW_ucphr_liPatologias","cphW_ucphr_ctl19_btnCrear","cphW_ucphr_ctl19_ucCreate_txtNombre","cphW_ucphr_ctl19_btnCrearAntecedentePatologico",None]
    list_to_eliminate = ["cphW_ucphr_ctl19_rptTable_btnEliminar_0","cphW_ucphr_ctl19_btnEliminarModal"]
    testing_different_inputs(ant_patol,'SOMETHING RIGHT','',list_to_eliminate,None,driver)
    print " Antecedentes Patologicos --> OK"
    time.sleep(2)

    ant_fam = ["cphW_ucphr_liAntecedentesFamiliares","cphW_ucphr_ctl20_btnCrear","cphW_ucphr_ctl20_ucCreate_txtNombre","cphW_ucphr_ctl20_btnCrearAntecedenteFamiliar",["cphW_ucphr_ctl20_ucCreate_ddlPariente"]]
    list_to_eliminate = ["cphW_ucphr_ctl20_rptTable_btnEliminar_0","cphW_ucphr_ctl20_btnEliminarModal"]
    testing_different_inputs(ant_fam,'SOMETHING RIGHT','',list_to_eliminate,"Abuela",driver)
    print " Antecedentes Familiares --> OK"
    time.sleep(2)

    dates_to_add = ["cphW_ucphr_ctl21_ucCreate_ucFecha_ddlDia","cphW_ucphr_ctl21_ucCreate_ucFecha_ddlMes","cphW_ucphr_ctl21_ucCreate_ucFecha_ddlAnno"]
    ant_qui = ["cphW_ucphr_liAntecedentesQuirurgicos","cphW_ucphr_ctl21_btnCrear","cphW_ucphr_ctl21_ucCreate_txtNombre","cphW_ucphr_ctl21_btnCrearAntecedenteQuirurgico", dates_to_add]
    list_to_eliminate = ["cphW_ucphr_ctl21_rptTable_btnEliminar_0","cphW_ucphr_ctl21_btnEliminarModal"]
    testing_different_inputs(ant_qui,'SOMETHING RIGHT','',list_to_eliminate,None,driver)
    print " Antecedentes Quirurgicos --> OK"
    time.sleep(2)

    ##ONLY FOR FEMALES
    if is_id_in_page("cphW_ucphr_liAntecedentesGinecoObstetricos",driver) == True:
        dates_to_add = ["cphW_ucphr_ctl22_ucCreate_ucFecha_ddlDia","cphW_ucphr_ctl22_ucCreate_ucFecha_ddlMes","cphW_ucphr_ctl22_ucCreate_ucFecha_ddlAnno"]
        ant_gin = ["cphW_ucphr_liAntecedentesGinecoObstetricos","cphW_ucphr_ctl22_btnCrear",None,"cphW_ucphr_ctl22_btnCrearAntecedenteGinecoObstetrico",dates_to_add]
        list_to_eliminate = ["cphW_ucphr_ctl22_rptTable_btnEliminar_0","cphW_ucphr_ctl22_btnEliminarModal"]
        testing_different_inputs(ant_gin,'SOMETHING RIGHT','',list_to_eliminate,None,driver)
        print " Antecedentes Gineco Obstetricos --> OK"
    time.sleep(2)

    dates_to_add = ["cphW_ucphr_ctl23_ucCreate_ucFecha_ddlDia","cphW_ucphr_ctl23_ucCreate_ucFecha_ddlMes","cphW_ucphr_ctl23_ucCreate_ucFecha_ddlAnno"]
    exam = ["cphW_ucphr_liExamenes","cphW_ucphr_ctl23_btnCrear","cphW_ucphr_ctl23_ucCreate_txtNombre","cphW_ucphr_ctl23_btnCrearExamen", dates_to_add]
    list_to_eliminate = ["cphW_ucphr_ctl23_rptTable_btnEliminar_0","cphW_ucphr_ctl23_btnEliminarModal"]
    testing_different_inputs(exam,'SOMETHING RIGHT','',list_to_eliminate, None,driver)
    print " Examenes --> OK"
    time.sleep(2)

    end_dates = ["cphW_ucphr_ctl24_ucCreate_ucFechaFin_ddlDia","cphW_ucphr_ctl24_ucCreate_ucFechaFin_ddlMes","cphW_ucphr_ctl24_ucCreate_ucFechaFin_ddlAnno"]
    dates_to_add = ["cphW_ucphr_ctl24_ucCreate_ucFecha_ddlDia","cphW_ucphr_ctl24_ucCreate_ucFecha_ddlMes","cphW_ucphr_ctl24_ucCreate_ucFecha_ddlAnno"]+end_dates
    list_to_eliminate = ["cphW_ucphr_ctl24_rptTable_btnEliminar_0","cphW_ucphr_ctl24_btnEliminarModal"]
    hospi = ["cphW_ucphr_liHospitalizaciones","cphW_ucphr_ctl24_btnCrear","cphW_ucphr_ctl24_ucCreate_txtNombre","cphW_ucphr_ctl24_btnCrearHospitalizacion",dates_to_add]
    testing_different_inputs(hospi,'SOMETHING RIGHT','something wrong',list_to_eliminate,None,driver)
    print " Hospitalizaciones --> OK"
    time.sleep(2)

    dates_to_add = ["cphW_ucphr_ctl25_ucCreate_ucFecha_ddlDia","cphW_ucphr_ctl25_ucCreate_ucFecha_ddlMes","cphW_ucphr_ctl25_ucCreate_ucFecha_ddlAnno"]
    vacu = ["cphW_ucphr_liVacunas","cphW_ucphr_ctl25_btnCrear","cphW_ucphr_ctl25_ucCreate_txtNombre","cphW_ucphr_ctl25_btnCrearVacuna",dates_to_add]
    list_to_eliminate = ["cphW_ucphr_ctl25_rptTable_btnEliminar_0","cphW_ucphr_ctl25_btnEliminarModal"]
    testing_different_inputs(vacu,'SOMETHING RIGHT','something wrong',list_to_eliminate, None,driver)
    print " Vacunas --> OK"
    time.sleep(2)

    dates_to_add = ["cphW_ucphr_ctl26_ucCreate_ucFecha_ddlDia","cphW_ucphr_ctl26_ucCreate_ucFecha_ddlMes","cphW_ucphr_ctl26_ucCreate_ucFecha_ddlAnno"]
    habits = ["cphW_ucphr_liAntecedentesPersonal","cphW_ucphr_ctl26_btnCrear",None,"cphW_ucphr_ctl26_btnCrearAntecedentePersonal",dates_to_add]
    list_to_eliminate = ["cphW_ucphr_ctl26_rptTable_btnEliminar_0","cphW_ucphr_ctl26_btnEliminarModal"]
    testing_different_inputs(habits,'SOMETHING RIGHT','something wrong',list_to_eliminate, None,driver)
    print " Habitos y Estilo de Vida --> OK"
    time.sleep(2)

    dates_to_add = ["cphW_ucphr_ctl27_ucCreate_ucFecha_ddlDia","cphW_ucphr_ctl27_ucCreate_ucFecha_ddlMes","cphW_ucphr_ctl27_ucCreate_ucFecha_ddlAnno"]
    meds = ["cphW_ucphr_liMedicamentos","cphW_ucphr_ctl27_btnCrear","cphW_ucphr_ctl27_ucCreate_txtNombre","cphW_ucphr_ctl27_btnCrearMedicamento",dates_to_add]
    list_to_eliminate = ["cphW_ucphr_ctl27_rptTable_btnEliminar_0","cphW_ucphr_ctl27_btnEliminarModal"]
    testing_different_inputs(meds,'SOMETHING RIGHT','something wrong',list_to_eliminate, None,driver)
    print " Medicamentos en Uso --> OK"

def testing_historia_medica(list_needed,input_needed, input_needed_2,driver):
    if u'HISTORIAS MÉDICAS' in driver.page_source:
        driver.find_element_by_link_text(u'HISTORIAS MÉDICAS').click()
    else:
        driver.find_element_by_link_text("HEALTH RECORD").click()
    time.sleep(1)

    scroll("cphW_ucphr_lihistoriamedica", driver)
    driver.find_element_by_id("cphW_ucphr_lihistoriamedica").click()
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

def finalizar_cita(driver):
    finishButton = "ctl00$cphW$ucCita$btnCitaFinalizarPpal"

def log_in_dr(email, pw, driver, ambiente):

    driver.get("http://" + ambiente + ".mediconecta.com/LoginD")
    time.sleep(3)

    assert ("Portal Mediconecta" in driver.title), "Pagina no encontrada"

    driver.find_element_by_id("cphW_txtUsuario").send_keys(email)
    driver.find_element_by_id("cphW_txtPassword").send_keys(pw + Keys.RETURN)


    if "Terminos" in driver.current_url:
        scroll("cphW_btnAceptar", driver)
        driver.find_element_by_id("cphW_btnAceptar").click()
        print " Aceptar Terminos --> OK"
        time.sleep(3)

    time.sleep(5)
    if "filapacientes" in driver.current_url:
        return "exitoso"
    if "no ha sido activada" in driver.page_source:
        return "inactivo"
    return "fallido"

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
        time.sleep(10)
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

def FillEncuesta(driver, option):
    time.sleep(5)

    assert ('cphW_respuestasRepeater_btnRespuesta_0' in driver.page_source), "No se encontraron los botones para la encuesta"

    if option == 5:
        print " Seleccion: Me Gusto Mucho"
        driver.find_element_by_id('cphW_respuestasRepeater_btnRespuesta_0').click()
    elif option == 4:
        print " Seleccion: Me Gusto"
        driver.find_element_by_id('cphW_respuestasRepeater_btnRespuesta_1').click()
    elif option == 3:
        print " Seleccion: Normal"
        driver.find_element_by_id('cphW_respuestasRepeater_btnRespuesta_2').click()
    elif option == 2:
        print " Seleccion: No Me Gusto"
        driver.find_element_by_id('cphW_respuestasRepeater_btnRespuesta_3').click()
    elif option == 1:
        print " Seleccion: No Me Gusto Nada"
        driver.find_element_by_id('cphW_respuestasRepeater_btnRespuesta_4').click()

    time.sleep(2)
    driver.find_element_by_id('cphW_btnFinalizar').click()

def programarCitaGeneral(driver):
    time.sleep(3)
    site = 'portal'

    if "PROGRAMAR CITA" in driver.page_source: #if login works
        site = 'hubsalud'
        lang = "spanish"
        print " Hub de Salud en Espanol"
    elif "SCHEDULE E-VISIT" in driver.page_source: #if login works
        site = 'hubsalud'
        lang = "english"
        print " Hub de Salud en Ingles"
    elif "Solicitud de Citas" in driver.page_source: #if login works
        print " Portal en Espanol"
        lang = "spanish"
    elif "e-visit" in driver.page_source: #if login works
        print " Portal en Ingles"
        lang = "english"


    if site == 'hubsalud':
        scroll("cphW_uccitasondemand_btnSolicitarCitaHub", driver)
        driver.find_element_by_id("cphW_uccitasondemand_btnSolicitarCitaHub").click()

        time.sleep(5)

        driver.find_element_by_id("cphW_uccitasondemand_btnOnDemandIntermedia").click()

        time.sleep(5)

        assert ("Cita con Medicina General" in driver.page_source) , "Not a Cita con Medicina General"


        print " Testing Fecha Empty"
        driver.find_element_by_id("cphW_uccitasagendadas_btnSolicitar").click()

        time.sleep(5)

        if lang == "english":
            assert ("Our apologies, an error" in driver.page_source), "No occurio un error"
        elif lang == "spanish":
            assert ("Disculpa, ha ocurrido" in driver.page_source), "No occurio un error"

        print " Testing Fecha Empty --> OK"

        driver.back()

        time.sleep(5)

        print " Testing Fecha Aceptable"
        scroll("cphW_uccitasondemand_btnSolicitarCitaHub", driver)
        driver.find_element_by_id("cphW_uccitasondemand_btnSolicitarCitaHub").click()

        time.sleep(5)

        driver.find_element_by_id("cphW_uccitasondemand_btnOnDemandIntermedia").click()

        time.sleep(5)

        assert (("Medicina General" in driver.page_source) or ("General Medicine" in driver.page_source)) , "Not a Cita con Medicina General"

        print " Seleccionando Fecha"

        fecha = "07/02/2017"
        fechaBox = driver.find_element_by_id("cphW_uccitasagendadas_txtFecha")
        fechaBox.send_keys(fecha + Keys.RETURN)

        print " Fecha Seleccionada --> OK"
        print " Solicitando la cita"

        driver.find_element_by_id("cphW_uccitasagendadas_btnSolicitar").click()

        print " Solicitando la cita --> OK"

        time.sleep(5)

        if ("Citas con Especialistas" in driver.page_source):
            site = "miscitas"
        else:
            site = "not miscitas"

        assert (site == "miscitas"), "Not redirected to MisCitas"
        print " Redireccionando a MisCitas --> OK"

        assert ("cphW_uclistadocita_rptTable_lblEspecialidad_0" in  driver.page_source and fecha in  driver.page_source), "Cita not added to Citas Programadas"
        print " Cita Programada --> OK"


    else:
        print "Not in hubsalud"

def programarCitaEspecial(driver, especialista):
    time.sleep(5)
    site = 'portal'

    if "PROGRAMAR CITA" in driver.page_source: #if login works
        site = 'hubsalud'
        lang = "spanish"
        print " Hub de Salud en Espanol"
    elif "SCHEDULE E-VISIT" in driver.page_source: #if login works
        site = 'hubsalud'
        lang = "english"
        print " Hub de Salud en Ingles"
    elif "Solicitud de Citas" in driver.page_source: #if login works
        print " Portal en Espanol"
        lang = "spanish"
    elif "e-visit" in driver.page_source: #if login works
        print " Portal en Ingles"
        lang = "english"



    if especialista == 'Nutrición':
        especialistaAssert = "Nutrici"
        nombreDeCita = "Cita con Nutrición"
        nombreDeCitaAssert = "Cita con Nutrici"
        ID = "cphW_ucespecialidades_btnNutrición"
        intermediaID = "cphW_ucespecialidades_btnIntermedioNutrición"

    elif especialista == u'Psicología':
        especialistaAssert = "Psicolog"
        nombreDeCita = u"Cita con Psicología"
        nombreDeCitaAssert = "Cita con Psicolog"
        ID = "cphW_ucespecialidades_btnPsicología"
        intermediaID = "cphW_ucespecialidades_btnIntermedioPsicología"

    elif especialista == u'Pediatría':
        especialistaAssert = "Pediatr"
        nombreDeCita = u"Cita con Pediatría"
        nombreDeCitaAssert = "Cita con Pediatr"
        ID = "cphW_ucespecialidades_btnPediatría"
        intermediaID = "cphW_ucespecialidades_btnIntermedioPediatría"


    if site == 'hubsalud':
        scroll(ID, driver)
        driver.find_element_by_id(ID).click()
        time.sleep(2)
        driver.find_element_by_id(intermediaID).click()
        time.sleep(5)

        assert (nombreDeCitaAssert in driver.page_source) , "Not a " + nombreDeCita

        print " Testing Fecha Empty"
        driver.find_element_by_id("cphW_uccitasagendadas_btnSolicitar").click()

        time.sleep(5)

        if lang == "english":
            assert ("Our apologies, an error" in driver.page_source), "No occurio un error"
        elif lang == "spanish":
            assert ("Disculpa, ha ocurrido" in driver.page_source), "No occurio un error"

        print " Testing Fecha Empty --> OK"

        driver.back()

        time.sleep(5)

        print " Testing Fecha Aceptable"

        scroll(ID, driver)
        driver.find_element_by_id(ID).click()
        time.sleep(2)
        driver.find_element_by_id(intermediaID).click()
        time.sleep(5)

        assert (nombreDeCitaAssert in driver.page_source) , "Not a " + nombreDeCita
        print " Seleccionando Fecha"

        fecha = "07/02/2017"
        fechaBox = driver.find_element_by_id("cphW_uccitasagendadas_txtFecha")
        fechaBox.send_keys(fecha + Keys.RETURN)

        print " Fecha Seleccionada --> OK"
        print " Solicitando la cita"

        driver.find_element_by_id("cphW_uccitasagendadas_btnSolicitar").click()

        print " Solicitando la cita --> OK"

        time.sleep(5)

        if ("Citas con Especialistas" in driver.page_source):
            site = "miscitas"
        else:
            site = "not miscitas"

        assert (site == "miscitas"), "Not redirected to MisCitas"
        print " Redireccionando a MisCitas --> OK"

        assert (especialistaAssert in  driver.page_source and fecha in  driver.page_source), "Cita not added to Citas Programadas"
        print " Cita Programada --> OK"

    else:
        print "Not in hubsalud"

def citaODTokboxEsp(driver, especialista):
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


    if especialista == 'Nutrición':
        especialistaAssert = "Nutrici"
        nombreDeCita = "Cita con Nutrición"
        nombreDeCitaAssert = "Cita con Nutrici"
        ID = "cphW_ucespecialidades_btnNutrición"
        intermediaID = "cphW_ucespecialidades_btnIntermedioNutrición"

    elif especialista == 'Psicología':
        especialistaAssert = "Psicolog"
        nombreDeCita = "Cita con Psicología"
        nombreDeCitaAssert = "Cita con Psicolog"
        ID = "cphW_ucespecialidades_btnPsicología"
        intermediaID = "cphW_ucespecialidades_btnIntermedioPsicología"

    if site == 'hubsalud':
        scroll(ID, driver)
        driver.find_element_by_id(ID).click()
        time.sleep(2)
        driver.find_element_by_id(intermediaID).click()
        time.sleep(5)

        if "son personales y generan un historial" or "Medical consultations are personal and create a medical history" in driver.page_source:
            scroll("uniform-cphW_uccitasondemand_rblParaQuien_0", driver)
            driver.find_element_by_id("uniform-cphW_uccitasondemand_rblParaQuien_0").click()
            scroll("cphW_uccitasondemand_btnContinuarDep", driver)
            driver.find_element_by_id("cphW_uccitasondemand_btnContinuarDep").click()
            print " Seleccionar Paciente --> OK"

            if "necesaria para que te pueda atender un Doctor" or "The setup is necessary to be able to talk to the Doctor" in driver.page_source:
                print " ValidacionVC.."
                #time.sleep(3)
                #if "Modulos/Cita/Cita" in driver.current_url:
                if "Tiempo de Espera Estimado" or "Estimated Wait Time" in driver.page_source:
                    print " Entrando a Sala de Espera.."
                    #time.sleep(3)

                else:
                    print " Cita no realizada1"
            else:
                print " Cita no realizada2"

        print " Paciente esperando ser atendido"

def atenderCitaProgramada(driver):
    time.sleep(2)
    misCitasButton = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-MisCitas', ' ' ))]")
    misCitasButton.click()
    time.sleep(3)
    assert ("Mis Citas" in driver.title), "Not in Mis Citas App"
    if "cphW_uclistadocita_rptTable_lnkCita_0" in driver.page_source:
        irButton = driver.find_element_by_id("cphW_uclistadocita_rptTable_lnkCita_0")
        irButton.click()
        time.sleep(5)
        assert ("Cita" in driver.title), "Paciente no entro en la sala de espera"
    else:
        print "No current cita"

def AppMisCitas(driver):
    misCitasButton = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-MisCitas', ' ' ))]")
    misCitasButton.click()
    time.sleep(2)
    assert ("Mis Citas" in driver.title), "Not in Mis Citas App"

    print " Solicitar Cita Button Test.."
    solicitarCitaButton = driver.find_element_by_id("cphW_uclistadocita_btnSolicitarCitaHub")
    solicitarCitaButton.click()
    time.sleep(2)
    assert ("Hub" in driver.title), "Not redirected to Health Hub"
    print " Solicitar Cita Button --> OK"

    time.sleep(2)

    misCitasButton = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-MisCitas', ' ' ))]")
    misCitasButton.click()
    time.sleep(2)
    assert ("Mis Citas" in driver.title), "Not in Mis Citas App"

    if "No hay citas registradas" not in driver.page_source:
        print " Buscar No Results.."
        buscar = driver.find_element_by_css_selector("#listado-Citas_filter .input-sm")
        buscar.send_keys("wrongwrongwrong")

        a = False
        try:
            driver.find_element_by_class_name("dataTables_empty")
            a = True
        except:
            pass

        assert (a), "The buscar input found something, even though it should not have"
        print " Buscar No Results --> OK"

        time.sleep(2)

        print " Buscar Con Resultados.."
        buscar = driver.find_element_by_css_selector("#listado-Citas_filter .input-sm")
        buscar.clear()
        buscar.send_keys("general")

        a = False
        try:
            driver.find_element_by_class_name("dataTables_empty")
            a = True
        except:
            pass

        assert (not a), "The buscar input did not find any results when it should have"
        print " Buscar Con Resultados --> OK"

    else:
        print "No hay citas registradas"

def OpcionesSinEspecialidades(driver):
    time.sleep(3)
    site = 'portal'

    if "PROGRAMAR CITA" in driver.page_source: #if login works
        site = 'hubsalud'
        lang = "spanish"
        print " Hub de Salud en Espanol"
    elif "SCHEDULE E-VISIT" in driver.page_source: #if login works
        site = 'hubsalud'
        lang = "english"
        print " Hub de Salud en Ingles"
    elif "Solicitud de Citas" in driver.page_source: #if login works
        print " Portal en Espanol"
        lang = "spanish"
    elif "e-visit" in driver.page_source: #if login works
        print " Portal en Ingles"
        lang = "english"


    if site == 'hubsalud':

        if "cphW_ucespecialidades_div-ActualizarHistoriaMedica" in driver.page_source:
            print "Testing Actualiza tu Historia Medica"
            scroll("cphW_ucespecialidades_div-ActualizarHistoriaMedica", driver)
            driver.find_element_by_id("cphW_ucespecialidades_div-ActualizarHistoriaMedica").click()

            time.sleep(5)

            driver.find_element_by_id("cphW_ucphr_liResumen").click()

            time.sleep(5)

            assert ("cphW_ucphr_ucResumenHistoriaMedica_Label1" in driver.page_source) , "Not on 'Historia Medica' page"
            print "Testing Actualiza tu Histora Medica --> OK"

            driver.back()
            time.sleep(5)

        if "cphW_ucespecialidades_div-RegistrarDependientes" in driver.page_source:
            print "Testing Registra a tus dependientes"

            scroll("cphW_ucespecialidades_div-RegistrarDependientes", driver)
            driver.find_element_by_id("cphW_ucespecialidades_div-RegistrarDependientes").click()

            time.sleep(5)
            assert("cphW_ucmicuenta_upListadoDependientePaciente" in driver.page_source), "Not on 'dependents' page"

            print "Testing Registrar un dependiente"
            scroll("cphW_ucmicuenta_ctl47_btnRegistrarConyuge", driver)
            driver.find_element_by_id("cphW_ucmicuenta_ctl47_btnRegistrarConyuge").click()
            time.sleep(5)
            if lang == "spanish":
                assert("Nombre" in driver.page_source and "Sexo" in driver.page_source), "Not on 'Crear Cónyuge' page"
            if lang == "english":
                assert("Name" in driver.page_source and "Sex" in driver.page_source), "Not on 'Crear Conuge' page"
            print "Testing Registrar un dependiente --> OK"
            print "Testing Registra a tus dependientes --> OK"
            driver.back()
            time.sleep(5)

            #filling out dependents form:
            '''
            #EMPTY, missing info
            print "Testing Missing Info"
            scroll("cphW_ucmicuenta_ctl47_btnCrearDependiente", driver)
            driver.find_element_by_id("cphW_ucmicuenta_ctl47_btnCrearDependiente").click()
            assert("Nombre" in driver.page_source and "Sexo" in driver.page_source)
            print "Testing Missing Info --> OK"

            #NOMBRE
            scroll("cphW_ucmicuenta_ctl47_ucCRU_ucDatos_txtNombre", driver)
            driver.find_element_by_id("cphW_ucmicuenta_ctl47_ucCRU_ucDatos_txtNombre").send_keys("Jenky")

            #APELLIDO
            scroll("cphW_ucmicuenta_ctl47_ucCRU_ucDatos_txtApellido", driver)
            driver.find_element_by_id("cphW_ucmicuenta_ctl47_ucCRU_ucDatos_txtApellido").send_keys("Johns")

            #PAIS ya esta llenado
            #NACIONALIDAD ya esta llenado

            #CEDULA
            scroll("cphW_ucmicuenta_ctl47_ucCRU_ucDatos_txtDocumentoId", driver)
            driver.find_element_by_id("cphW_ucmicuenta_ctl47_ucCRU_ucDatos_txtDocumentoId").send_keys("12345678")

            #FECHA DE NACIMIENTO (dia)
            scroll("cphW_ucmicuenta_ctl47_ucCRU_ucDatos_ucFecha_ddlDia", driver)


            #SEXO

            #RELACION ya esta llenado

            #TELEPHONO
            scroll("cphW_ucmicuenta_ctl47_ucCRU_ucDatos_txtTelefonoCelular", driver)
            driver.find_element_by_id("cphW_ucmicuenta_ctl47_ucCRU_ucDatos_txtTelefonoCelular").send_keys("12345678")
            '''
        if "cphW_ucespecialidades_div-ConsultarPrescripcionesContent" in driver.page_source:

            print "Testing Consulta tus prescripciones recientes"

            scroll("cphW_ucespecialidades_div-ConsultarPrescripcionesContent", driver)
            driver.find_element_by_id("cphW_ucespecialidades_div-ConsultarPrescripcionesContent").click()
            time.sleep(5)

            if u"Historias Médicas" in driver.page_source:
                print "Testing Consulta tus prescripciones recientes --> OK"
            else:
                assert(False), "Not on persciption page"

            driver.back()
            time.sleep(5)

        if "cphW_ucespecialidades_opcionTituloVisitarBlog" in driver.page_source:
            print "Testing Visite nuestro blog"

            scroll("cphW_ucespecialidades_opcionTituloVisitarBlog", driver)
            driver.find_element_by_id("cphW_ucespecialidades_opcionTituloVisitarBlog").click()
            time.sleep(5)

            driver.switch_to_window(driver.window_handles[1])
            if driver.current_url == "http://www.mediconecta.com/blog-salud-en-linea/":
                print "Testing Visite nuestro blog --> OK"
            else:
                print "Did not go to Mediconecta Blog"

            driver.switch_to_window(driver.window_handles[1])


    else:
        print "Not in hubsalud"


start = time.time()
main(sys.argv[1:])
print "Execution Time: " + str(int((time.time() - start))) + " seconds"
