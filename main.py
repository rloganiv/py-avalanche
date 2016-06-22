from util.bank import Bank, create_links
from util.event import Generator
from util.log import Log
import numpy as np
import time

# Globals to be made args
reserve_ratio = .30
deposit_rate = .4
withdrawal_rate = .1
loan_rate = .4
repay_rate = .1
default_prob = .01
n_banks = 8
max_iter = 1000000
topology = 'Complete'

if __name__ == '__main__':
    # Setup
    start_time = time.strftime('%Y-%d-%m_%H-%M-%S')
    simulation = 1

    master_head = ['simulation', 'time', 'bank']
    master_log = Log('output/master_' + start_time + '.csv', master_head)
    lifespan_head = ['simualation', 'bank', 'lifespan']
    lifespan_log = Log('output/lifespan_' + start_time + '.csv', lifespan_head)
    profit_head = ['simulation', 'total_profit']
    profit_log = Log('output/profit_' + start_time + '.csv', profit_head)
    avalanche_head = ['simulation', 'time', 'avalanche_size']
    avalanche_log = Log('output/avalanche_' + start_time + '.csv',
                        avalanche_head)
    settings_head = ['reserve_ratio', 'deposit_rate', 'withdrawal_rate',
                     'loan_rate', 'repay_rate', 'default_prob', 'n_banks']
    settings_log = Log('output/settings_' + start_time + '.csv', settings_head)

    settings_log.write_items([reserve_ratio, deposit_rate, withdrawal_rate,
                              loan_rate, repay_rate, default_prob, n_banks])
    iterations = 0
    time = 0
    period_remaining = 1

    bank_list = [Bank(1000, 310, 700, reserve_ratio, default_prob)
                 for i in xrange(n_banks)]
    create_links(bank_list, topology)
    live_list = bank_list

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
        event, delta_t = event_gen.draw_event()
        bank = np.random.choice(live_list)

        time += delta_t
        period_remaining += -delta_t
        while period_remaining <= 0:
            # TODO: Payout interest
            period_remaining += 1

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

        avalanche_count = 0
        for bank in live_list:
            if bank.dead:
                live_list.remove(bank)
                avalanche_count += 1
                n_banks += -1
        if avalanche_count > 1:
            avalanche_log.write_items([simulation, time, avalanche_count])
        iterations += 1

    # Shutdown
    master_log.close()
    lifespan_log.close()
    profit_log.close()
    print "Model Done Running"
