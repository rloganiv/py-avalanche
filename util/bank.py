import random


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
    def __init__(self, deposits, reserves, loans, reserve_ratio):
        """Initialize bank agent."""
        self.deposits = deposits
        self.reserves = reserves
        self.loans = loans
        self.reserve_ratio = reserve_ratio
        self.interbank_balances = {}
        self.total_profit = 0
        self.state = 0

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

    def nft_loan_repayment(self, default_prob):
        """NFT pays back a loan, with chance of default."""
        rng = random.random()
        if rng < default_prob:
            self.loans += -1
        else:
            self.loans += -1
            self.reserves += 1

    def add_neighbor(self, neighbor):
        """Creates ability for bank to make interbank transactions with
        neighbor."""
        if neighbor not in self.interbank_balances:
            self.interbank_balances[neighbor] = 0
            neighbor.interbank_balances[self] = 0

    def borrow(self):
        """Bank borrows from a neighbor if possible."""
        for neighbor in self.interbank_balances:
            if neighbor.can_loan():
                self.reserves += 1
                neighbor.reserves += -1
                self.interbank_balances[neighbor] += -1
                neighbor.interbank_balances[self] += 1
                return
        self.state = 1

    def recall_interbank_loan(self):
        """Bank recalls outstanding interbank loans."""
        for neighbor in self.interbank_balances:
            if self.interbank_balances[neighbor] > 0:
                neighbor.interbank_balances[self] += 1
                self.interbank_balances[neighbor] += -1
                self.reserves += 1
                return
        self.state = 2

    def recall_nft_loans(self, default_rate):
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
        for neighbor in self.interbank_balances:
            del neighbor.interbank_balances[self]
        self.dead = True

