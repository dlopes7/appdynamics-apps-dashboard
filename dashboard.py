import json
import requests
from copy import deepcopy

WIDGETS_PER_LINE = 5
WIDTH = WIDGETS_PER_LINE * 200
HEIGTH = 1500


x_offset = 190
y_offset = 275

host = 'demo2.appdynamics.com'
port = '80'
user = 'admin'
password = 'password'
account = 'customer1'


ignore_list = ['MERX']


health_rules = {'SOA': 'Weblogic - Threads Hogging Count',
                'OSB': 'Weblogic - Threads Hogging Count',
                'WAS': 'Uso do Thread Pool do WebContainer',
                'DOTNET': 'Memory utilization is too high',
                'VIGNETTE': 'Weblogic - Threads Hogging Count',
                'JBOSS': 'JVM Heap utilization is too high'}

hr_default = health_rules['JBOSS']
apptype_default = 'WAS'

app_names = {
    'AUTO2_BPMBAM': {'type': 'OSB', 'name': 'Auto2<br>BPM'},
    'AUTO2_OSB': {'type': 'OSB', 'name': 'Auto2<br>OSB'},
    'AUTO2_SOA': {'type': 'OSB', 'name': 'Auto2<br>SOA'},
    'AUTO_OSB': {'type': 'OSB', 'name': 'Auto<br>OSB'},
    'AUTO_OSB12C': {'type': 'OSB', 'name': 'Auto<br>OSB12c'},
    'AUTO_SOA': {'type': 'OSB', 'name': 'Auto<br>SOA'},
    'AUTO_SOA12c': {'type': 'OSB', 'name': 'Auto<br>SOA12c'},
    'WASGIW': {'type': 'WAS', 'name': 'GIW'},
    'CAPS': {'type': 'WAS', 'name': 'CAPS'},
    'CORP_OSB12c': {'type': 'OSB', 'name': 'Corp<br>OSB12c'},
    'CORP_OSB': {'type': 'OSB', 'name': 'Corp<br>OSB'},
    'CORP_SOA': {'type': 'OSB', 'name': 'Corp<br>SOA'},
    'FENIX': {'type': 'WAS', 'name': 'Fenix'},
    'INNOVARE_BAM': {'type': 'OSB', 'name':  'Innovare<br>BAM'},
    'INNOVARE_BPM': {'type': 'OSB', 'name': 'Innovare<br>BPM'},
    'INNOVARE_OSB': {'type': 'OSB', 'name': 'Innovare<br>OSB'},
    'INNOVARE_OSBAPR': {'type': 'OSB', 'name': 'Innovare<br>OSBAPR'},
    'INNOVARE_SOA': {'type': 'OSB', 'name': 'Innovare<br>SOA'},
    'INNOVARE_WAS': {'type': 'WAS', 'name':  'Innovare<br>WAS'},
    'LINHA_VERDE': {'type': 'WAS', 'name': 'Linha<br>Verde'},
    'LINHA_VERDE_EMISSAO_RS': {'type': 'WAS', 'name':  'LV RS<br>Emissao'},
    'LINHA_VERDE_EMISSAO_RS_85': {'type': 'WAS', 'name': 'LV RS85<br>Emissao'},
    'LINHA_VERDE_SERVICOS_AUTO': {'type': 'WAS', 'name': 'LV Servicos<br>Auto'},
    'MULTICALCULO': {'type': 'WAS', 'name': 'Multi<br>Calculo'},
    'ORCAMENTO': {'type': 'WAS', 'name': 'Orçamento'},
    'PAYWARE': {'type': 'JBOSS', 'name': 'Payware'},
    'POL': {'type': 'WAS', 'name': 'POL'},
    'POL_DESCONTO_PADRAO': {'type': 'WAS', 'name': 'POL Desc<br>Padrão'},
    'POL_PRODUCAO_CONTROLADA': {'type': 'WAS', 'name': 'POL Prod<br>Controlada'},
    'PPWEB': {'type': 'WAS', 'name': 'PPWeb'},
    'PPWEB_CONTROLADA': {'type': 'WAS', 'name':  'PPWeb<br>Controlada'},
    'SIVJ': {'type': 'JBOSS', 'name': 'SIVJ'},
    'TMG': {'type': 'WAS', 'name': 'T+G'},
    'WAS85_CORP': {'type': 'WAS', 'name': 'WAS85<br>CORP'},
    'WASCORPEXT': {'type': 'WAS', 'name': 'WAS<br>CORPEXT'},
    'CLICK_DOTNET': {'type': 'DOTNET', 'name':  'Click'},
    'RECUPERA_DOTNET': {'type': 'DOTNET', 'name': 'Recupera'},
    'SAUDE_APOLLO_DOTNET': {'type': 'DOTNET', 'name':  'Apollo'},
    'VIGNETTE_PORTAL_CLIENTE_PRD': {'type': 'VIGNETTE', 'name':  'Portal Cliente'},
    'VIGNETTE_PORTAL_NOVOCOL_PRD': {'type': 'VIGNETTE', 'name':  'Portal NovoCol'},
    'VIGNETTE_NOVO_INST': {'type': 'VIGNETTE', 'name':  'Portal<br>Novo Inst'},
    'VIGNETTE_CRIARCONTAWS_PRD': {'type': 'VIGNETTE', 'name':  'Portal<br>CriarConta'},
    'VIGNETTE_PORTAL_PORTONET_PRD': {'type': 'VIGNETTE', 'name':  'Portal<br>PortoNet'},
    'VIGNETTE_PORTAL_PRESTADOR_PRD': {'type': 'VIGNETTE', 'name':  'Portal<br>Prestador'},
    'ACIONAMENTO_WEB_DOTNET': {'type': 'DOTNET', 'name': 'Acionamento Web'},
    'WEBSYSIN_DOTNET': {'type': 'DOTNET', 'name':  'WEBSYSIN'}
}


def get_applications(host, port, user, password, account):
    url = 'http://{}:{}/controller/rest/applications'.format(host, port)
    auth = ('{}@{}'.format(user, account), password)
    params = {'output': 'json'}

    print('Getting apps', url)
    r = requests.get(url, auth=auth, params=params)
    return sorted(r.json(), key=lambda k: k['name'])


def create_widgets_labels(APPS, widget_template):
    print('Creating Labels')
    widgets = []
    start_x = 0
    start_y = 90
    current_y = start_y

    counter = 0
    for application in APPS:
        if application['name'] not in ignore_list:
            try:
                app = '<div>{}</div>'.format(
                    app_names[application['name']]['name'])
                app_type = '{}'.format(app_names[application['name']]['type'])
            except KeyError:
                app = '<div>{}</div>'.format(
                    application['name'][:20])
                app_type = 'Default'
                print('ERRO aplicacao nao mapeada:',
                      application['name'], 'usando NOME:', app, 'TYPE', app_type)

            # if app_type in techs:
            # print('Creating label for', app, end=' ')
            new_widget = widget_template
            line_position = counter % WIDGETS_PER_LINE

            if line_position == 0 and counter >= WIDGETS_PER_LINE:
                current_y += y_offset

            # new_widget['width'] = len(app) * 10
            new_widget['y'] = current_y

            new_widget['x'] = start_x + line_position * x_offset

            # new_widget['x'] = base_x + ((130 - len(app) * 10) / 2)

            # print('@', new_widget['x'], new_widget['y'])

            new_widget["text"] = app

            widgets.append(new_widget.copy())
            counter += 1
    return widgets


def create_widgets_hrs(APPS, widget_template):
    print('Creating Health Rule Widgets')
    global HEIGTH

    widgets = []
    start_x = 20
    start_y = 190
    current_y = start_y

    counter = 0
    line_counter = 1
    for application in APPS:
        if application['name'] not in ignore_list:
            app = application['name']
            try:
                hr = health_rules[app_names[application['name']]['type']]
                app_type = '{}'.format(app_names[application['name']]['type'])
            except KeyError:
                hr = hr_default
                app_type = apptype_default
                print('ERRO, aplicacao nao mapeada',
                      app, 'usando HR:', hr, 'TYPE:',  app_type)

            # if app_type in techs:
            # app_id = application['id']
            # print('Creating widget for', app, end=' ')
            new_widget = widget_template
            line_position = counter % WIDGETS_PER_LINE

            if line_position == 0 and counter >= WIDGETS_PER_LINE:
                line_counter += 1
                current_y += y_offset

            new_widget['x'] = start_x + line_position * x_offset
            new_widget['y'] = current_y

            # print('@', new_widget['x'], new_widget['y'])

            new_widget["applicationReference"]["applicationName"] = app
            new_widget["applicationReference"]["entityName"] = app

            for entity in new_widget['entityReferences']:
                entity["applicationName"] = app
                entity['entityName'] = hr

            # rint(new_widget['applicationReference'])
            widgets.append(deepcopy(new_widget))
            counter += 1
    HEIGTH = line_counter * 330
    return widgets


def create_widgets_labeltypes(APPS, widget_template):
    print('Creating Labels Types')
    widgets = []
    start_x = 40
    start_y = 260
    current_y = start_y

    counter = 0
    for application in APPS:
        if application['name'] not in ignore_list:
            try:
                app_type = '{}'.format(app_names[application['name']]['type'])
            except KeyError:
                app_type = apptype_default
                print('ERRO, aplicacao nao mapeada',
                      application['name'], 'usando TYPE:', app_type)

            # if app_type in techs:
            new_widget = widget_template
            line_position = counter % WIDGETS_PER_LINE

            if line_position == 0 and counter >= WIDGETS_PER_LINE:
                current_y += y_offset

            new_widget['y'] = current_y
            new_widget['x'] = start_x + line_position * x_offset

            new_widget["text"] = app_type

            widgets.append(new_widget.copy())
            counter += 1
    return widgets


def process(dash):

    new_dash = dash
    new_widgets = []
    APPS = get_applications(host, port, user, password, account)

    for widget in new_dash['widgetTemplates']:
        if widget['widgetType'] == 'HealthListWidget':
            new_widgets += create_widgets_hrs(APPS, widget)

        if widget['widgetType'] == 'TextWidget':
            if widget["text"] == '<div>AUTO<br>OSB</div>':
                new_widgets += create_widgets_labels(APPS, widget)

            if widget["text"] == 'SOA':
                new_widgets += create_widgets_labeltypes(APPS, widget)

            if widget["text"] == "" or widget["text"] == "Visão Geral Sistemas Porto Seguro":
                widget["width"] = WIDTH
                new_widgets.append(widget)

            else:
                new_widgets.append(widget)

        if widget['widgetType'] == 'ImageWidget':
            new_widgets.append(widget)

    new_dash['widgetTemplates'] = new_widgets
    new_dash['height'] = HEIGTH
    new_dash['width'] = WIDTH

    # print(json.dumps(new_dash, indent=4, sort_keys=True))
    with open('new_dash_{}.json'.format(host), 'w') as outfile:
        json.dump(new_dash, outfile, indent=4, sort_keys=True)


def main():
    with open('dashboard.json') as json_data:
        d = json.load(json_data)
        process(deepcopy(d))


if __name__ == '__main__':
    main()
