import random
from itertools import combinations


class Bank(object):
    """A bank agent.

    Attributes:
        deposits (int): Number of deposits bank is currently holding.
        reserves (int): Number of deposits currently in bank's reserves.
        loans (int): Number of outstanding loans bank currently holds.
        profit (float): The accumulated amount of money made through the bank's
            lending activites, or lost through the bank's borrowing activities.
        interbank_balances (dict): A dictionary whose keys are other banks, and
            the associated value is the amount of outstanding loans that have
            been made to that bank.
        reserve_ratio (float): Ratio of deposits bank must have on hand.
    """
    def __init__(self, deposits, reserves, loans, reserve_ratio, default_prob):
        """Initialize bank agent."""
        self.deposits = deposits
        self.reserves = reserves
        self.loans = loans
        self.reserve_ratio = reserve_ratio
        self.interbank_balances = {}
        self.total_profit = 0
        self.state = 0
        self.default_prob = default_prob
        self.is_borrowing = False
        self.dead = False

    def can_loan(self):
        """True if bank has liquid assets available for investment."""
        if self.reserves > self.reserve_ratio * self.deposits:
            return True
        else:
            return False

    def needs_cash(self):
        """True if bank needs liquid assets to satisfy reserve requirement."""
        if self.reserves < self.reserve_ratio * self.deposits:
            return True
        else:
            return False

    def nft_deposit(self):
        """NFT makes a deposit with bank."""
        self.deposits += 1
        self.reserves += 1

    def nft_withdrawal(self):
        """NFT withdraws deposit from bank."""
        # If no deposits, do nothing
        if self.deposits == 0:
            pass

        # If there is sufficient money in reserves then refund deposit
        elif self.reserves > 0:
            self.deposits += -1
            self.reserves += -1

    def nft_loan_request(self):
        """NFT requests a loan.

        Returns:
            True if loan accepted, False if loan denied.
        """
        if self.can_loan():
            self.reserves += -1
            self.loans += 1

    def nft_loan_repayment(self):
        """NFT pays back a loan, with chance of default."""
        rng = random.random()
        if rng < self.default_prob:
            self.loans += -1
        else:
            self.loans += -1
            self.reserves += 1

    def add_neighbor(self, neighbor):
        """Creates ability for bank to make interbank transactions with
        neighbor."""
        if neighbor not in self.interbank_balances:
            self.interbank_balances[neighbor] = 0
            neighbor.add_neighbor(self)

    def borrow(self):
        """Bank borrows from a neighbor if possible."""
        self.is_borrowing = True
        for neighbor in self.interbank_balances:
            if neighbor.can_loan() and not neighbor.is_borrowing:
                self.reserves += 1
                neighbor.reserves += -1
                self.interbank_balances[neighbor] += -1
                neighbor.interbank_balances[self] += 1
                neighbor.check_reserves()
                neighbor.check_solvency()
                neighbor.check_liquidity()
                self.is_borrowing = False
                return
        self.is_borrowing = False
        self.state = 1

    def recall_interbank_loan(self):
        """Bank recalls outstanding interbank loans."""
        for neighbor in self.interbank_balances:
            if self.interbank_balances[neighbor] > 0:
                neighbor.interbank_balances[self] += 1
                self.interbank_balances[neighbor] += -1
                self.reserves += 1
                neighbor.check_reserves()
                neighbor.check_solvency()
                neighbor.check_liquidity()
                return
        self.state = 2

    def recall_nft_loans(self):
        """Bank recalls outstanding NFT loan."""
        if self.loans > 0:
            self.nft_loan_repayment()
        else:
            self.state = 3

    def check_reserves(self):
        """Bank checks if it has enough reserves. If it does not then it tries
        to recover assets until it does."""
        while self.needs_cash():
            if self.state == 0:
                self.borrow()
            elif self.state == 1:
                self.recall_interbank_loan()
            elif self.state == 2:
                self.recall_nft_loans()
            elif self.state == 3:
                break
            else:
                raise ValueError('Bank in state: %s' % self.state)

    def check_solvency(self):
        """Determines whether bank is solvent. If it is not it dies."""
        capital = self.reserves + self.loans - self.deposits + \
            sum(self.interbank_balances.itervalues())
        if capital <= 0:
            self.die()

    def check_liquidity(self):
        """Checks whether bank has liquid assets. If it does not it dies."""
        if self.reserves <= 0:
            self.die()

    def die(self):
        """Removes bank from network, and sets dead flag to True."""
        for neighbor in self.interbank_balances.copy():
            del neighbor.interbank_balances[self]
            del self.interbank_balances[neighbor]
        self.dead = True


def create_links(bank_list, topology=None):
    """Creates links between banks according to specified topology.

    args:
        bank_list = A list of banks to link together.
        topology = One of: None, 'Circle', 'Complete', or 'Star'
    """
    if topology == 'Circle':
        for i, bank in enumerate(bank_list):
            bank.add_neighbor(bank_list[(i + 1) % len(bank_list)])

    if topology == 'Star':
        for bank in bank_list[1:]:
            bank.add_neighbor(bank_list[0])

    if topology == 'Complete':
        for bank_1, bank_2 in combinations(bank_list, 2):
            bank_1.add_neighbor(bank_2)

