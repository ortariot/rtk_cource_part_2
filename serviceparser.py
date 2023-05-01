from __future__ import annotations
from abc import ABC, abstractmethod
from itertools import chain


class Context():

    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def load_data(self, data: dict) -> None:
        return self._strategy.do_algorithm(data)


class Strategy(ABC):

    @abstractmethod
    def do_algorithm(self, data: dict):
        pass


class ServiceStrategy(Strategy):

    def do_algorithm(self, data: dict) -> list[dict[str, str]]:
        data = data.get('services')
        return [{
            'name': item["name"],
            'code':item["code"]
        } for item in data]


class AccountServicesStrategy(Strategy):

    def do_algorithm(self, data: dict) -> list[dict[str, str]]:
        data = data.get('accountServices')
        return [{
            'name': item["serviceName"],
            'code':item["serviceCode"]
        } for item in data]


class Leaf():
    def add(self, leaf):
        raise NotImplementedError()

    def get_leaf(self, index):
        raise NotImplementedError()


class ServiceLeaf(Leaf):

    def __init__(self, tree_part: dict):
        self.name = tree_part.get('name')
        self.code = tree_part.get('code')

    def get_convolution(self) -> list[dict[str, str]]:
        return [{
            'name': self.name,
            'code': self.code
        }] if self.name and self.code else []


class SimpleProductLeaf(Leaf):
    def __init__(self, tree_part: dict):
        self.productName = tree_part.get('productName')
        self.productCode = tree_part.get('productCode')

    def get_convolution(self) -> list[dict[str, str]]:
        return [{
            'name': self.productName,
            'code': self.productCode
        }] if self.productName and self.productCode else []


class ServiceTreeStrategy(Leaf, Strategy):
    def __init__(self):
        self._leafs = []

    def add(self, obj: Leaf):
        if isinstance(obj, Leaf) and obj not in self._leafs:
            self._leafs.append(obj)

    def get_leaf(self, index) -> Leaf:
        return self._lefs[index]

    def get_convolution(self) -> list[dict[str, str]]:
        out = [leaf.get_convolution() for leaf in self._leafs]

        return list(chain.from_iterable(out))

    def parse_tree(self, tree: dict):
        if 'items' in tree:
            tree, = tree['items']

        part_tree = tree.get('children')

        for children in part_tree:
            is_root = bool(children.get('isRoot'))
            child_type = children.get('type')['keyName']

            if is_root and child_type == 'SIMPLE_PRODUCT':
                continue
            elif child_type == 'SERVICE':
                self.add(ServiceLeaf(children))
            elif child_type == 'SIMPLE_PRODUCT':
                self.add(SimpleProductLeaf(children))
            else:
                new_tree = ServiceTreeStrategy()
                new_tree.parse_tree(children)
                self.add(new_tree)

    def do_algorithm(self, data: dict) -> list[dict[str, str]]:
        self.parse_tree(data)
        return self.get_convolution()
