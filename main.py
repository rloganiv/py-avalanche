from util.bank import Bank
from util.event import Generator
import numpy as np

# Globals to be made args
reserve_ratio = .30
deposit_rate = .4
withdrawal_rate = .1
loan_rate = .4
repay_rate = .1
default_prob = .01
n_banks = 8
max_iter = 1000000

if __name__ == '__main__':
    # Setup
    iterations = 0
    bank_list = [Bank(1000, 310, 700, reserve_ratio, default_prob)
                 for i in xrange(n_banks)]

    # Circle topology
    for i, bank in enumerate(bank_list):
        bank.add_neighbor(bank_list[(i + 1) % n_banks])

    # Event generation
    event_dict = {
        'nft_deposit': deposit_rate,
        'nft_withdrawal': withdrawal_rate,
        'nft_loan_req': loan_rate,
        'nft_loan_repay': repay_rate
    }
    event_gen = Generator(event_dict)

    # Main loop
    while(n_banks > 0 and iterations < max_iter):
        # Generate event
        event = event_gen.draw_event()[0]
        bank = np.random.choice(bank_list)
        if event == 'nft_deposit':
            bank.nft_deposit()
        if event == 'nft_withdrawal':
            bank.nft_withdrawal()
        if event == 'nft_loan_req':
            bank.nft_loan_request()
        if event == 'nft_loan_repay':
            bank.nft_loan_repayment()
        bank.check_reserves()
        bank.check_solvency()
        bank.check_liquidity()
        if bank.dead:
            bank_list.remove(bank)
            n_banks += -1
            #TODO: Add avalanche tracker
            for neighbor in bank.interbank_balances:
                neighbor.check_reserves()
                neighbor.check_solvency()
                neighbor.check_liquidity()
        iterations += 1
    print "Model Done Running"
