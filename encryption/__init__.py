from encryption.rsa import RSAProcessor, RSAKey


class CryptoManager(object):
    message: str = None
    encryptedData: bytes = None
    decryptedData: str = None
    key: RSAKey = None

    def clear(self):
        self.encryptedData = b''
        self.decryptedData = ''

    def load_file(self, file):
        self.clear()
        self.message = file.stream.read().decode('utf-8')

    def process(self):
        processor = RSAProcessor(self.key)
        if self.message:
            self.encryptedData = processor.encrypt(self.message)
        if self.encryptedData:
            self.decryptedData = processor.decrypt(self.encryptedData)

    def describe_encrypted(self):
        return ''.join('%02x ' % i for i in self.encryptedData)
