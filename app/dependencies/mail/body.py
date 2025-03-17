from ...settings import config

class Body():
    def email_verification(self, hash_email):
        validation_url = "http://localhost:3000/confirmar-email/" + hash_email

        html_body = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verificação de Email - Leiturece</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; border: 1px solid #e0e0e0;">
                <h1 style="color: #2c3e50; margin-bottom: 20px;">Bem-vindo a Leiturece!</h1>
                <p style="margin-bottom: 25px;">
                    Para verificar seu e-mail, por favor clique no botão abaixo:
                </p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{validation_url}"
                       style="background-color: #000000;
                              color: white;
                              padding: 12px 25px;
                              text-decoration: none;
                              border-radius: 5px;
                              display: inline-block;">
                        Verificar E-mail
                    </a>
                </div>
                <p style="color: #666; font-size: 0.9em; margin-top: 30px;">
                    Se você não solicitou esta verificação, por favor ignore este e-mail.
                </p>
                <p style="color: #666; font-size: 0.9em; margin-top: 30px;">
                    {hash_email}
                </p>
            </div>
        </body>
        </html>
        """

        text_body = f"""
        Para verficar o seu E-mail por favor acesse o link:
        {validation_url}
        Se você não solicitou esta verificação, por favor ignore este e-mail.
        """

        return html_body, text_body

body = Body()
