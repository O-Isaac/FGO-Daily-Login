import os
import libs.utils.logs as Logger
import libs.encryption.CertFileDescription as CertFileDescryption
import libs.game.Client as Game
import libs.utils.region as Region

def main():
    certificate = os.environ.get('certificate')
    
    if (certificate is None):
        Logger.error("certificate secret is not present please add the secret.")
        exit(1)

    certificates = certificate.split(",")

    for cert in certificates:
        cert_data: dict = CertFileDescryption.Decrypt(cert)
        
        userCreateServer = cert_data.get('userCreateServer')
        userId = cert_data.get('userId')
        authKey = cert_data.get('authKey')
        secretKey = cert_data.get('secretKey')
        region = Region.fromUserCreateServer(userCreateServer)
        Game.Login(userId, authKey, secretKey, region)

if __name__ == "__main__":
    main()