class Bank(object):
    """A bank agent.

    Attributes:
        reserve_tgt (float): Target ratio of reserves bank must hold in order to
            be willing to lend.
        reserve_min (float): Minimum ratio of reserves bank must hold. If
            reserve ratio falls beneath this number then bank will borrow from
            neighbors until reserve ratio is again greater than or equal to
            this number.
        deposits (int): Number of deposits bank is currently holding.
        reserves (int): Number of deposits currently in bank's reserves.
        loans (int): Number of outstanding loans bank currently holds.
        profit (float): The accumulated amount of money made through the bank's
            lending activites, or lost through the bank's borrowing activities.
        neighbors (list): A list of a bank's neighbors. Entries must be tuples
            whose first element is another Bank object, and second element is
            the number of loans the bank has made to its neighbor (note: is
            negative if bank is indebted).
    """
    def __init__(self, reserve_tgt, reserve_min, deposits, reserves, loans,
                profit, neighbors):
        """Initialize bank agent.

        Args:
            see class attributes
        """
        self.reserve_tgt = reserve_tgt
        self.reserve_min = reserve_min
        self.deposits = deposits
        self.reserves = reserves
        self.loans = loans
        self.profit = profit
        self.neighbors = neighbors
        self.check_solvency()

    def nft_deposit(self):
        """NFT makes a deposit with bank."""
        self.reserves += 1
        self.deposits += 1

    def nft_withdrawal(self):
        """NFT withdraws deposit from bank."""
        # If no deposits, do nothing
        if self.deposits == 0:
            pass
        # If there is sufficient money in reserves then refund deposit
        elif self.reserves - 1 > self.reserve_min * self.deposits:
            self.deposits += -1
            self.reserves += -1
        # Otherwise borrow and then refund deposit
        else:
            self.borrow()
            self.deposits += -1
            self.reserves += -1
        # TODO: Determine how to handle consequences if borrowing is
        # unsuccessful; just refund from reserves? If so should borrwing be
        # handled periodically instead of as an event response?

    def check_solvency(self):
        """Determines whether bank is solvent.

        Returns:
            True if solvent, False if otherwise.
        """
        capital = self.reserves + self.loans - self.deposits +
            self.intrabank_loans()
        if capital <= 0:
            self.die()
            return False
        else:
            return True

    #TODO: Implement
    def borrow(self):
        """Borrow money from neighbors (if possible)."""
        pass

    #TODO: Implement
    def die(self):
        """Handle defaults, bank network alterations, etc. that occur when bank
        becomes insolvent."""
        pass
