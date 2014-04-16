
from dtk import mail

def write_to_file(data, outfile):
    with open(outfile, 'w') as fp:
        fp.write(data)

def send_alert(sender, recipients, depdate, retdate):
    print 'Dates available! %s -> %s' % (depdate, retdate)
    emailer = mail.Email(sender, recipients,
                         'FLIGHTS AVAILABLE %s to %s' % (depdate, retdate),
                         'Check out the free flights at Virgin')
    emailer.send()

