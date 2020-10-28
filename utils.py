import logging
import csv

logging.basicConfig(level=logging.WARNING)


def prepara_dettaglio(model, full=False):
    print('<table>')
    for campo in prepara_lista_campi(model, full):
        print(
f'''<tr>
<td class="bold">{{% trans "{campo}" %}}</td>
<td class="">{{{{{model._meta.verbose_name}.{campo}}}}}</td>
</tr>''')
    print('</table>')

def prepara_th(model, full=False):
    for campo in prepara_lista_campi(model, full):
        print(f'''<th scope="col">{{% trans "{campo.title()}" %}}</th>''')


def list_creator():
    b = []
    while True:
        a = input('Inserisci parola')
        if a.lower() == 'basta':
            print(b)
            break
        elif a not in b:
            b.append(a)
            print('aggiunta alla lista')


def prepara_lista_campi(modello, full=False):
    """
    Dato un modello ne ritorna una lista di tutti i campi in formato stringa
    """

    return [field.name for field in modello._meta.get_fields()]

def prepara_form(modello, full=False):
    lista_campi = prepara_lista_campi(modello)
    print('''<form method="post" enctype="multipart/form-data">''')
    for campo in lista_campi:
        print(f'''<div class="row">
    <div class="col-12 blocco-campo">
        <label for="form_{campo}" class="col-form-label">{{{{ form.{campo}.help_text }}}}</label>
        {{% render_field form.{campo} id='form_{campo}' class='form-control' %}}
    </div>
</div>''')
    print('''<div class="col-12 blocco-campo">
                <input type="submit" value="Invia" role="button">
            </div>
        </form>''')


def resize_image(img):
    from PIL import Image
    with Image.open(img) as img:
        img = Image.open(img.convert('RGB'))
        resolution = 720
        width = img.size[0]
        height = img.size[1]
        if width > height and width > resolution:
            wpercent = (resolution/float(width))
            hsize = int((float(height)*float(wpercent)))
            img = img.resize((resolution, hsize), Image.ANTIALIAS)
            img.save(img, format='jpeg', optimize=True, progressive=False, quality=70)
        if width <= height and height > resolution :
            wpercent = (resolution/float(height))
            hsize = int((float(width)*float(wpercent)))
            img = img.resize((hsize, resolution), Image.ANTIALIAS)
            img.save(img, format='jpeg', optimize=True, progressive=False, quality=70)
        else:
            img.save(img, format='jpeg', optimize=True, progressive=False, quality=70)


def send_testmail(v=True):
    from django.core.mail import send_mail
    from django.conf import settings
    import socket
    hostname = socket.gethostname()
    if v:
        print('About to send a test email with settings:')
        print(f'''
    HOSTNAME: {hostname}
    TLS: {settings.EMAIL_USE_TLS}
    SSL: {settings.EMAIL_USE_SSL}
    EMAIL HOST: {settings.EMAIL_HOST}
    EMAIL PORT: {settings.EMAIL_PORT}
    EMAIL HOST_USER: {settings.EMAIL_HOST_USER}
    EMAIL HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD}
    ''')
    send_mail(
        'This is a test email',
        f'''Here is a test message. 
HOSTNAME: {hostname}
TLS: {settings.EMAIL_USE_TLS}
SSL: {settings.EMAIL_USE_SSL}
EMAIL HOST: {settings.EMAIL_HOST}
EMAIL PORT: {settings.EMAIL_PORT}
EMAIL HOST_USER: {settings.EMAIL_HOST_USER}
EMAIL HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD}
''',
        'test_mail@flowsy.io',
        ['romanin@exeadvisor.com'],
        fail_silently=False,
    )
    print('The test email has been successfully sent')