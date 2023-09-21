import os
import unittest
import libs.utils.logs as Logger

class Tests(unittest.TestCase):
    certificate = os.environ.get('certificate')
    webhook_discord = os.environ.get('webhookDiscord')

    def has_secret(self, secret):
        if secret is None:
            return False
        
        return True

    def certificate_structure(self):
        import libs.encryption.CertFileDescription as CertDescryptor
        
        try:
            certifacte_data = CertDescryptor.Decrypt(self.certificate)
            return isinstance(certifacte_data, dict)
        except Exception as ex:
            Logger.error(ex)
            return False

    def tests(self):
        # Certificate
        self.assertEqual(self.has_secret(self.certificate), True, "Please add GAME_CERT to secrets")
        self.assertEqual(self.certificate_structure(), True, "The certificate is not valid")
        
        # Discord Webhook
        self.assertEqual(self.has_secret(self.webhook_discord), True, "Please add DISCORD_WEBHOOK to secrets")
    
if __name__ == "__main__":
    unittest.main()
