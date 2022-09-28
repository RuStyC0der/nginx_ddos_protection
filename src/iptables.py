from abstract.abstractBlock import BanMethod

import iptc

class IptablesBlockMethod(BanMethod):

    custom_chain_name = 'nginx-ddos-protection-chain'

    # check or create chain
    def __init__(self):
        # use table filter
        table = iptc.Table(iptc.Table.FILTER)

        # return if chain exists
        for chain in table.chains:
            if chain.name == self.custom_chain_name:
                self.custom_chain = chain
                print("chain exists")
                return
        
        # create chain and add to chain input
        self.custom_chain = table.create_chain(self.custom_chain_name)
        input_chain = iptc.Chain(table, "INPUT")
        custom_chain_rule = iptc.Rule()
        custom_chain_rule.create_target(self.custom_chain_name)
        input_chain.insert_rule(custom_chain_rule)


    def ban(self, ip):
        rule = iptc.Rule()
        rule.src = ip
        rule.create_target("DROP")
        rule.final_check()
        self.custom_chain.append_rule(rule)


    def unban(self, ip):
        rule = iptc.Rule()
        rule.src = ip
        rule.create_target("DROP")
        rule.final_check()
        self.custom_chain.delete_rule(rule)

    def flush(self):
        self.custom_chain.flush()
    
    def cleanup(self):
        input_chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        custom_chain_rule = iptc.Rule()
        custom_chain_rule.create_target(self.custom_chain_name)
        input_chain.delete_rule(custom_chain_rule)

        self.flush()
        self.custom_chain.delete()

a = IptablesBlockMethod()
a.ban("192.168.1.2")
a.cleanup()