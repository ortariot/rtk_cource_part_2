import os
import json

from sqlalchemy.exc import IntegrityError

from serviceparser import (
    Context, ServiceStrategy,
    AccountServicesStrategy, ServiceTreeStrategy
)

from data_store_tools import DataStoreTools


class ServiceDataLoader():

    def __init__(self, path: str, URI: str):
        tools = DataStoreTools(URI)
        self.file_list = os.listdir(path)
        data: list = self.__load_data()

    def __load_data(self) -> list[dict[str, str]]:
        context = Context(ServiceStrategy())
        out = []
        for file_name in self.file_list:
            path = os.path.join('input', file_name)
            with open(path, encoding='utf-8') as file:
                data = json.load(file)
                if 'services' in data:
                    pass
                    context.strategy = ServiceStrategy()
                    res = context.load_data(data)
                elif 'accountServices' in data:
                    pass
                    context.strategy = AccountServicesStrategy()
                    res = context.load_data(data)
                else:
                    context.strategy = ServiceTreeStrategy()
                    res = context.load_data(data)
            out.extend(res)
        return out

    def to_data_dtore(self, data: list[dict[str, str]]):
        for item in data:
            try:
                service = tools.create_service(item['name'], item['code'])
                if service:
                    print(f"service {item['name']} was loaded")
            except IntegrityError as e:
                print((
                    f"Cannot load service with name - {item['name']} "
                    f"and code {item['code']} because: {e} "
                )
                )


if __name__ == '__main__':
    data_laoder = ServiceDataLoader('input', SQLALCHEMY_DATABASE_URI)
