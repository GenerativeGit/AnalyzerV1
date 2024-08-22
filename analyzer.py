class Analyzer:
    # Initialization Function
    def __init__(self, language, source):
        self.language = language
        self.source   = source

        self.__verify()
        self.__format()

    # Internal Functions
    def __fail(self, message):
        raise BaseException(message)

    def __verify(self):
        if not self.language in Analyzer.SupportedLanguages():
            self.__fail('Analyzer: Language Not Supported')

        if str.count(self.source, '\n') > 810:
            self.__fail('Analyzer: > 810 nSLOC')

    def __format(self):
        self.__formattedSource = self.source.replace('\n', '\\n')

    def __post(self):
        headers = {'Content-Type': 'application/json'}
        data = {'pastedCode': self.__formattedSource}

        from requests import post
        response = post(
            url='https://auditz.ai/api/analyze-contract',
            headers=headers,
            json=data
        )

        if not response.status_code == 200:
            print(response.status_code)
            self.__fail('Analyzer: Not Valid Response')

        return response.text

    # External Functions
    def analyze(self):
        data = self.__post()

        return data

    # Static Methods
    @staticmethod
    def SupportedLanguages():
        return [
            'Solidity',
            'Vyper',
            'Rust',
            'C++',
            'Undefined'
        ]

    @staticmethod
    def typeConvMarkdown(analysis: str):
        from json import loads
        data = loads(analysis)

        markdown = str()

        for line in data:
            markdown += f"## {line['title']}\n"

            for answer in line['answers']:
                markdown += f"{answer}\n\n"

        return markdown.strip()