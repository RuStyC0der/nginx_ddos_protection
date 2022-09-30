from abstract.abstractBlock import BanMethod

import iptc

class IptablesBlockMethod(BanMethod):
    """
    class that implemets iptables ip blocking logic
    """
    custom_chain_name = 'nginx-ddos-protection-chain'
    ip_datastore = set()

    def __init__(self):
        """
        on init we createing new empty chain inside "INPUT" table to hold all blocked users separately
        then we redirect all connections to custom chain
        init is an idempotent method
        """
        table = iptc.Table(iptc.Table.FILTER)

        # if chain exists bound it and load ips from it
        for chain in table.chains:
            if chain.name == self.custom_chain_name:
                self.custom_chain = chain
                self.export_chain_rules_to_datastore()
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



    def export_chain_rules_to_datastore(self):
        for rule in self.custom_chain.rules:
            self.ip_datastore.add(rule.src)

    def add_ip_to_datastore(self, ip):
        self.ip_datastore.add(ip)
    
    def remove_ip_from_datastore(self, ip):
        self.ip_datastore.discard(ip)
    
    def is_ip_in_datastore(self, ip):
        return ip in self.ip_datastore


    def ban(self, ip):
        """
        add drop rule with *ip*
        """
        if not self.is_ip_in_datastore(ip):
            rule = iptc.Rule()
            rule.src = ip
            rule.create_target("DROP")
            rule.final_check()
            self.custom_chain.append_rule(rule)

            self.add_ip_to_datastore(ip)


    def unban(self, ip):
        """
        delete drop rule with *ip*
        """
        if self.is_ip_in_datastore(ip):
            rule = iptc.Rule()
            rule.src = ip
            rule.create_target("DROP")
            rule.final_check()
            self.custom_chain.delete_rule(rule)

            self.remove_ip_from_datastore(ip)

    def flush(self):
        """
        clean blocked users chain
        """
        self.custom_chain.flush()
    
    def cleanup(self):
        """
        remove all chains and rules created by class
        """
        input_chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        custom_chain_rule = iptc.Rule()
        custom_chain_rule.create_target(self.custom_chain_name)
        input_chain.delete_rule(custom_chain_rule)

        self.flush()
        self.custom_chain.delete()

if __name__ == "__main__":
    # export XTABLES_LIBDIR=/usr/lib/xtables
    a = IptablesBlockMethod()
    a.cleanup()
    # a.ban('192.168.1.120')
    # a.ban('192.168.1.121')
    # a.ban('192.168.1.122')
    # a.ban('192.168.1.123')
