from abstract.abstractBlock import BanMethod

import iptc

class IptablesBlockMethod(BanMethod):
    """
    class that implemets iptables ip blocking logic
    """
    custom_chain_name = 'nginx-ddos-protection-chain'

    
    def __init__(self):
        """
        on init we createing new empty chain inside "INPUT" table to hold all blocked users separately
        then we redirect all connections to custom chain
        init is an idempotent method
        """
        table = iptc.Table(iptc.Table.FILTER)

        # do nothing if chain exists
        for chain in table.chains:
            if chain.name == self.custom_chain_name:
                self.custom_chain = chain
                return
        
        # create and configure chain
        self.custom_chain = table.create_chain(self.custom_chain_name)
        custom_chain_return_rule = iptc.Rule()
        custom_chain_return_rule.create_target("RETURN")
        self.custom_chain.append_rule(custom_chain_return_rule)

        # add link to chain "input" 
        input_chain = iptc.Chain(table, "INPUT")
        custom_chain_redirect_rule = iptc.Rule()
        custom_chain_redirect_rule.create_target(self.custom_chain_name)
        input_chain.insert_rule(custom_chain_redirect_rule)


    def ban(self, ip):
        """
        add drop rule with *ip*
        """
        rule = iptc.Rule()
        rule.src = ip
        rule.create_target("DROP")
        rule.final_check()
        self.custom_chain.append_rule(rule)


    def unban(self, ip):
        """
        delete drop rule with *ip*
        """
        rule = iptc.Rule()
        rule.src = ip
        rule.create_target("DROP")
        rule.final_check()
        self.custom_chain.delete_rule(rule)

    def flush(self):
        """
        clean blocked users chain
        """
        self.custom_chain.flush()
    
    def cleanup(self):
        """
        move all chains and rules created by class
        """
        input_chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        custom_chain_rule = iptc.Rule()
        custom_chain_rule.create_target(self.custom_chain_name)
        input_chain.delete_rule(custom_chain_rule)

        self.flush()
        self.custom_chain.delete()

if __name__ == "__main__":
    a = IptablesBlockMethod()
