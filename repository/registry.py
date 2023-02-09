class RepositoriesRegistry:
    def __init__(self, cargos, flights, users, customers, rockets, tokens):
        self.cargos_repo = cargos
        self.flights_repo = flights
        self.users_repo = users
        self.customers_repo = customers
        self.rockets_repo = rockets
        self.tokens_repo = tokens
