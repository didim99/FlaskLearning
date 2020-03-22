from encryption.rsa import RSAProcessor, RSAKey


class CryptoManager(object):
    fileName: str = None
    message: str = None
    encryptedData: bytes = None
    decryptedData: str = None
    key: RSAKey = None

    def load_file(self):
        pass

    def process(self):
        processor = RSAProcessor(self.key)
        if self.message:
            self.encryptedData = processor.encrypt(self.message)
        if self.encryptedData:
            self.decryptedData = processor.decrypt(self.encryptedData)
