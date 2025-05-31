import smtplib
from  email.message import EmailMessage
import os

def enviar_email(arquivo_excel):
    EMAIL_REMETENTE = 'ryanoliveiramosc.com.098@gmail.com'
    EMAIL_DESTINATARIO = 'email-destinatario'
    SENHA_APP = 'senha_sua (boa sorte para conseguir a sua)'

    # Criar a mensagem de e-mail
    mensagem = EmailMessage()
    mensagem['Subject'] = 'Relatório Automático'
    mensagem['From'] = EMAIL_REMETENTE
    mensagem['To'] = EMAIL_DESTINATARIO
    mensagem.set_content('Olá Senhor meu chefe,\n\nSegue o relatório gerado automaticamente de produtos com estoque baixo.\n\nAtt,\nRyan')

    # Adiciona o anexo
    with open(arquivo_excel, 'rb') as file:
        conteudo = file.read()
        nome_arquivo_no_email = os.path.basename(arquivo_excel) 

        mensagem.add_attachment(conteudo, maintype='application', subtype='octet-stream', filename=nome_arquivo_no_email)

    # Enviar o e-mail
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(mensagem)
            print('✅ E-mail enviado com sucesso!')
    except Exception as e:
        print(f'❌ Falha ao enviar e-mail: {e}')
