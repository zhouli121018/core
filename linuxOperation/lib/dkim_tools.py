# coding=utf-8
import dns.resolver

dns.resolver.get_default_resolver().cache = dns.resolver.LRUCache()


def try_query(qname, rdtype):
    try:
        rs = []
        answers = dns.resolver.query(qname, rdtype)
        for a in answers:
            if rdtype == 'mx':
                rs.append(a.exchange.to_text())
            elif rdtype in ['txt', 'cname']:
                rs.append(a.to_text())
            else:
                rs.append(a)
        return rs
    except dns.exception.DNSException:
        return []


def is_find_key(lists, key):
    if isinstance(lists, list):
        for l in lists:
            if l.find(key) != -1:
                return True
    return False


def valid_domain(domain, rdtype, record='', dkim_selector='umail'):
    """
    检测域名记录
    :param domain: 域名
    :param rdtype: 检测类型 mx, spf, dkim
    :param record: 数据库的记录
    :return:
    """
    if rdtype == 'spf':
        t_record = try_query(domain, 'txt')
        return is_find_key(t_record, record)
    if rdtype == 'mx':
        t_record = try_query(domain, 'mx')
        return record in t_record or '{}.'.format(record) in t_record
    if rdtype == 'dkim':
        t_record = try_query('{}._domainkey.{}'.format(dkim_selector, domain), 'txt')
        #print "t_record is ",t_record
        return t_record[0][1:-1] == record if t_record else False
    if rdtype == 'cname':
        t_record = try_query(domain, 'cname')
        return t_record[0].find(record) != -1 if t_record else False


def generate_rsa(pkey='', bits=1024):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    from Crypto.PublicKey import RSA
    if pkey:
        new_key = RSA.importKey(pkey.strip())
    else:
        new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    assert public_key != private_key
    return private_key, public_key


if __name__ == "__main__":
    dkim_selector='umail'
    domain="u-mail.work"
    print "valid_domain:  ",valid_domain(domain, 'dkim', '', 'umail')
    print "dkim", try_query('{}._domainkey.{}'.format(dkim_selector, domain), 'txt')
    print "spf", try_query(domain, 'txt')
    print "mx", try_query(domain, 'mx')
